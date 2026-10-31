# -*- coding: utf-8 -*-
"""sandbox.py — безопасная песочница выполнения кода ученика.

``CodeSandbox`` запускает код через ``exec()`` в изолированном словаре имён и:

* перехватывает ``print()`` и отправляет вывод в GUI-терминал (callback);
* строит AST-защиту от бесконечных циклов: каждый цикл получает счётчик,
  при превышении лимита (по умолчанию 1000 итераций) выбрасывается
  ``SandboxLoopLimit`` с понятным русским сообщением;
* переводит типовые ошибки (``SyntaxError``, ``IndentationError``,
  ``NameError``, ``TypeError``, ``ZeroDivisionError``, ``IndexError``,
  ``ValueError``, ``AttributeError``, ``KeyError``) на человеческий русский
  язык с подсказкой «что исправить».

Запрещённые конструкции (импорт os/sys/subprocess, open, eval, exec, input)
отклоняются на этапе проверки AST — урок не сможет сломать игру.
"""

import ast
import builtins
import time
import traceback

DEFAULT_ITERATION_LIMIT = 1000
DEFAULT_TIMEOUT_SEC = 5.0

#: Модули, которые ученику трогать нельзя.
FORBIDDEN_MODULES = {"os", "sys", "subprocess", "shutil", "socket", "ctypes", "pathlib"}

#: Недоступные встроенные функции (файлы/интерактив/метапрограммирование).
FORBIDDEN_BUILTINS = {"open", "input", "eval", "exec", "compile", "__import__",
                      "globals", "locals", "exit", "quit"}

RU_TYPE_NAMES = {
    "int": "целое число (int)",
    "float": "дробное число (float)",
    "str": "строка (str)",
    "bool": "логическое значение (bool)",
    "list": "список (list)",
    "tuple": "кортеж (tuple)",
    "dict": "словарь (dict)",
    "set": "множество (set)",
    "NoneType": "ничего (None)",
    "function": "функция",
}


class SandboxLoopLimit(Exception):
    """Служебное исключение: цикл крутится слишком долго."""

    _suppress_tb = True


class SandboxTimeout(Exception):
    """Служебное исключение: превышено время выполнения."""

    _suppress_tb = True


def ru_type_name(value):
    t = type(value)
    name = getattr(t, "__name__", str(t))
    if name in RU_TYPE_NAMES:
        return RU_TYPE_NAMES[name]
    try:
        base = t.__bases__[0].__name__
    except (AttributeError, IndexError):
        base = name
    return RU_TYPE_NAMES.get(base, name)


def _safe_str(obj):
    """repr без вызова пользовательского __repr__ во внешнем коде."""
    try:
        return repr(obj)
    except Exception:
        return "<нечитаемый объект>"


def _printify(obj):
    """Как настоящий print(): str() для верхнего уровня, repr внутри контейнеров.

    Вложенные элементы контейнеров (list/dict/tuple/set) форматируются через
    _safe_str — так вывод песочницы совпадает с выводом обычного Python
    (print('Нова', 1+1) -> 'Нова 2'), но не даёт пользовательскому __repr__
    выполнить произвольный код вне контроля песочницы.
    """
    if isinstance(obj, str):
        return obj
    if isinstance(obj, BaseException):
        try:
            return str(obj)
        except Exception:
            return "<нечитаемое исключение>"
    if isinstance(obj, (list, tuple, set, frozenset, dict)):
        # стандартный repr контейнера сам вызывает repr элементов
        try:
            return repr(obj)
        except Exception:
            return "<нечитаемый контейнер>"
    try:
        return str(obj)
    except Exception:
        return _safe_str(obj)


# --------------------------------------------------------------------------
#  AST-трансформер: защита от бесконечных циклов
# --------------------------------------------------------------------------
class _LoopGuardTransformer(ast.NodeTransformer):
    """Оборачивает каждый for/while в счётчик итераций."""

    def __init__(self, limit):
        self.limit = int(limit)
        self._ctr = 0

    def _new_counter(self):
        self._ctr += 1
        return "__nova_loop_ctr_%d" % self._ctr

    @staticmethod
    def _is_guard_raise(node):
        if not isinstance(node, ast.Raise):
            return False
        exc = node.exc
        name = ""
        if isinstance(exc, ast.Call) and isinstance(exc.func, ast.Name):
            name = exc.func.id
        elif isinstance(exc, ast.Name):
            name = exc.id
        return name == "SandboxLoopLimit"

    @staticmethod
    def _set_coords(node, ln, col):
        """Проставить координаты узлу (Python 3.8+: fix_missing_locations
        пропускает узлы с lineno=None, поэтому задаём их явно)."""
        node.lineno = ln
        node.col_offset = col
        if hasattr(node, "end_lineno"):
            node.end_lineno = ln
            node.end_col_offset = col

    def _instrument_loop(self, node):
        """Добавить в тело цикла счётчик итераций и проверку лимита."""
        ctr = self._new_counter()
        incr = ast.parse("%s += 1" % ctr).body[0]
        chk = ast.parse(
            "raise SandboxLoopLimit('%s', %d)" % (ctr, self.limit)
        ).body[0]
        test = ast.parse("%s > %d" % (ctr, self.limit)).body[0].value
        guard = ast.If(test=test, body=[chk], orelse=[])
        ln = getattr(node, "lineno", 1) or 1
        col = getattr(node, "col_offset", 0) or 0
        for n in (guard, chk):
            if getattr(n, "lineno", None) is None:
                self._set_coords(n, ln, col)

        body = list(node.body)
        # уже обёрнуто? (защита от повторного прохода) — не оборачиваем дважды
        if not (body and self._is_guard_raise(body[-1])):
            # инициализация счётчика как первое выражение тела:
            # (__nova_ctr := 0) — допустимо и в stmt-, и в expr-контексте
            # (walrus оператор, Python 3.8+); затем инкремент и проверка.
            init_expr = ast.parse("(%s := 0)" % ctr).body[0].value
            first = body[0] if body else None
            body = [ast.Expr(value=init_expr)] + body + [incr, guard]
            if first is not None:
                self._set_coords(body[0], getattr(first, "lineno", ln) or ln,
                                 getattr(first, "col_offset", col) or col)
            node.body = body
        return node

    def visit_Module(self, node):
        """Обойти все циклы дерева (включая вложенные) и вернуть тот же Module.

        Важно: возвращаем исходный узел Module, а не новый Module внутри
        другого Module — иначе NodeTransformer построит недопустимое дерево
        и compile() упадёт с «required field "lineno" missing from stmt».
        """
        for i, stmt in enumerate(list(node.body)):
            new = self.visit(stmt)
            if new is not None and new is not stmt:
                node.body[i] = new
        # инициализация счётчиков вынесена в walrus-выражения внутри тел,
        # поэтому дополнительных операторов на уровне модуля не нужно
        ast.fix_missing_locations(node)
        return node

    def visit_For(self, node):
        self.generic_visit(node)          # сначала обработаем вложенные циклы
        return self._instrument_loop(node)

    def visit_AsyncFor(self, node):
        self.generic_visit(node)
        return self._instrument_loop(node)

    def visit_While(self, node):
        self.generic_visit(node)
        return self._instrument_loop(node)


class _ForbiddenFinder(ast.NodeVisitor):
    """Собирает запрещённые импорты и вызовы."""

    def __init__(self):
        self.problems = []

    @staticmethod
    def _root(name):
        return name.split(".")[0] if name else ""

    def visit_Import(self, node):
        for alias in node.names:
            if self._root(alias.name) in FORBIDDEN_MODULES:
                self.problems.append(
                    "Нельзя импортировать модуль '%s' — он может навредить игре."
                    % alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if self._root(node.module or "") in FORBIDDEN_MODULES:
            self.problems.append(
                "Нельзя импортировать модуль '%s' — он может навредить игре."
                % node.module)
        self.generic_visit(node)

    def visit_Call(self, node):
        f = node.func
        fname = ""
        if isinstance(f, ast.Name):
            fname = f.id
        elif isinstance(f, ast.Attribute):
            fname = f.attr
        if fname in FORBIDDEN_BUILTINS:
            self.problems.append(
                "Функция '%s()' недоступна в песочнице урока. "
                "Используй print() для вывода." % fname)
        self.generic_visit(node)


def protect_source(source, iteration_limit=DEFAULT_ITERATION_LIMIT):
    """Вернуть (безопасный_код_для_exec, список_нарушений).

    Сначала проверяются запрещённые конструкции, затем циклы обматываются
    счётчиками итераций. Синтаксические ошибки возвращаются в ``problems``.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise  # пусть переводом занимается run()
    finder = _ForbiddenFinder()
    finder.visit(tree)
    if finder.problems:
        return source, finder.problems
    guarded = _LoopGuardTransformer(iteration_limit).visit(tree)
    try:
        code = compile(guarded, "<ученик>", "exec")
    except SyntaxError as e:
        return source, ["Ошибка синтаксиса после защиты циклов: %s" % e.msg]
    return code, []


# --------------------------------------------------------------------------
#  Перевод ошибок на русский
# --------------------------------------------------------------------------
def translate_exception(exc):
    """Возвращает список строк: 'Что пошло не так' + подсказки."""
    lines = []
    if getattr(exc, "__traceback__", None) is not None:
        tb_lines = traceback.format_exception(type(exc), exc, exc.__traceback__)
    else:
        tb_lines = traceback.format_exception_only(type(exc), exc)
    where = ""
    for ln in tb_lines:
        s = ln.rstrip("\n")
        if s.startswith("Traceback") or "SandboxLoopLimit" in s \
                or "protect_source" in s or "_loop_guard" in s:
            continue
        if s.lstrip().startswith('File "<'):
            where = s
            continue
        if s.strip():
            lines.append(s)

    text = " ".join(lines)
    en = str(exc)

    if isinstance(exc, SandboxLoopLimit):
        return [u"[ЦИКЛ ЗАВИС] Твой цикл выполнил больше 1000 итераций и был "
                u"остановлен защитой песочницы.",
                u"→ Проверь условие цикла while: оно должно когда-нибудь стать "
                u"False. Проверь range(): правильные ли границы?",
                u"Контекст: " + (where or en)]

    if isinstance(exc, IndentationError):
        return [u"[ОТСТУП] Неправильные отступы в строке %s: %s"
                % (getattr(exc, "lineno", "?"), exc.msg),
                u"→ Выровняй код пробелами (4 пробела на один уровень вложенности). "
                u"Не смешивай табы и пробелы.",
                u"Контекст: " + (where or en)]

    if isinstance(exc, SyntaxError):
        return [u"[СИНТАКСИС] Не понимаю эту запись в строке %s: %s"
                % (getattr(exc, "lineno", "?"), exc.msg),
                u"→ Частые причины: забытая скобка ')' или двоеточие ':' в конце, "
                u"кавычка закрыта не той же чертой, слово написано с ошибкой.",
                u"Контекст: " + (where or en)]

    if isinstance(exc, NameError):
        m = _re_between(en, "name '(.+?)'", "' is not defined")
        hint = (u"→ Имя '%s' нигде не создано. Проверь опечатку или создай "
                u"переменную до использования." % m) if m else \
               u"→ Проверь опечатку: сначала создай переменную, потом используй."
        return [u"[НЕИЗВЕСТНОЕ ИМЯ] В программе нет переменной или функции с таким именем. "
                u"(строка ~%s)" % _line_of(where), hint,
                u"Контекст: " + (where or en)]

    if isinstance(exc, TypeError):
        return [u"[НЕСОВМЕСТИМЫЕ ТИПЫ] " + en,
                u"→ Python не умеет складывать разные типы. Пример: \"5\" + 3 "
                u"не сработает, а int(\"5\") + 3 — сработает. "
                u"Проверь, что функция получает данные нужного типа.",
                u"Контекст: " + (where or en)]

    if isinstance(exc, ZeroDivisionError):
        return [u"[ДЕЛЕНИЕ НА НОЛЬ] Нельзя делить на 0 (строка ~%s)." % _line_of(where),
                u"→ Добавь проверку: if знаменатель != 0.",
                u"Контекст: " + (where or en)]

    if isinstance(exc, IndexError):
        return [u"[ВЫХОД ЗА ГРАНИЦУ СПИСКА] Обращаешься к элемента, которого нет (строка ~%s)."
                % _line_of(where),
                u"→ Индексы списка начинаются с 0. У списка из 3 элементов "
                u"последний индекс — 2. Используй len(spisok), чтобы узнать размер.",
                u"Контекст: " + (where or en)]

    if isinstance(exc, KeyError):
        key = en.strip("'\"")
        return [u"[НЕТ ТАКОГО КЛЮЧА] В словаре отсутствует ключ %r (строка ~%s)."
                % (key, _line_of(where)),
                u"→ Проверь написание ключа или используй slovar.get(key, 0).",
                u"Контекст: " + (where or en)]

    if isinstance(exc, ValueError):
        return [u"[НЕПРАВИЛЬНОЕ ЗНАЧЕНИЕ] " + en,
                u"→ Функция получила данные неподходящего формата. Например, "
                u"int(\"привет\") вызовет такую ошибку.",
                u"Контекст: " + (where or en)]

    if isinstance(exc, AttributeError):
        m = _re_between(en, "'(.+?)' object has no attribute", None)
        obj = m.split("'")[0].strip() if m else ""
        hint = u"→ У объекта типа %s нет такого метода/поля. Проверь название " \
               u"и обратись к справке языка." % (obj or "этого типа")
        return [u"[НЕТ ТАКОГО МЕТОДА] " + en, hint,
                u"Контекст: " + (where or en)]

    if isinstance(exc, MemoryError):
        return [u"[ПАМЯТЬ КОНЧИЛАСЬ] Программа заняла всю память. "
                u"→ Скорее всего, список растёт бесконечно внутри цикла.",
                u"Контекст: " + (where or en)]

    if isinstance(exc, RecursionError):
        return [u"[РЕКУРСИЯ ЗАЦИКЛИЛАСЬ] Функция вызывает саму себя слишком глубоко. "
                u"→ Добавь условие выхода из рекурсии (базовый случай).",
                u"Контекст: " + (where or en)]

    return [u"[ОШИБКА %s] %s" % (type(exc).__name__, en),
            u"Контекст: " + (where or en)]


def _re_between(text, left, right):
    import re
    if not text or not left:
        return ""
    pattern = left + r"(.+?)" + (right or "")
    m = re.search(pattern, text)
    return m.group(1) if m else ""


def _line_of(where):
    import re
    m = re.search(r"<[^>]*>?", where or "")
    num = re.findall(r"line (\d+)", where or "")
    return num[0] if num else "?"


# --------------------------------------------------------------------------
#  Песочница
# --------------------------------------------------------------------------
class CodeSandbox:
    """Безопасный запуск кода ученика с перехватом print()."""

    def __init__(self, output_callback=None, iteration_limit=DEFAULT_ITERATION_LIMIT,
                 timeout_sec=DEFAULT_TIMEOUT_SEC):
        #: callable(str) — приём каждой строки вывода в терминал GUI
        self.output = output_callback or (lambda s: None)
        self.iteration_limit = int(iteration_limit)
        self.timeout_sec = float(timeout_sec)
        self.globals = self._make_globals()
        self.last_error = None
        self.last_exception = None
        self.runs = 0

    # ------------------------------------------------------------ окружение
    def _make_globals(self):
        g = {}
        safe_names = [n for n in dir(builtins)
                      if n not in FORBIDDEN_BUILTINS and not n.startswith("__")]
        for name in safe_names:
            g[name] = getattr(builtins, name)
        # разрешённые «опасные» вещи нужны для учебных задач
        g["__import__"] = self._restricted_import
        g["print"] = self._print_hook
        g["SandboxLoopLimit"] = SandboxLoopLimit
        g["math"] = __import__("math")
        g["random"] = __import__("random")
        g["time"] = time
        return g

    @staticmethod
    def _restricted_import(name, globals=None, locals=None, fromlist=(), level=0):
        root = name.split(".")[0]
        if root in FORBIDDEN_MODULES:
            raise ImportError(u"Модуль '%s' заблокирован песочницей. "
                              u"Разрешены: math, random, time." % name)
        if root not in {"math", "random", "time", "json", "string", "itertools",
                        "functools", "collections", "datetime", "fractions"}:
            raise ImportError(u"Модуль '%s' недоступен на этом уроке. "
                              u"Разрешены: math, random, time." % name)
        return __import__(name, globals, locals, fromlist, level)

    # -------------------------------------------------------------- ввод/вывод
    def _print_hook(self, *args, **kwargs):
        sep = kwargs.get("sep", " ") if kwargs else " "
        end = kwargs.get("end", "\n") if kwargs else "\n"
        file = kwargs.get("file", None) if kwargs else None
        if file is not None:
            raise OSError(u"В песочнице print(...) можно вызывать только "
                          u"в терминал игры — параметр file запрещён.")
        text = sep.join(_printify(a) for a in args) + end
        if not text:
            return
        lines = text.split("\n")
        if lines[-1] == "":
            lines.pop()  # завершающий перевод строки — не пустая «строка вывода»
        for line in lines:
            self.output(line)

    def feed_input(self, *values):
        """Подготовить ответы для учебной функции read() (эмуляция input())."""
        self._inputs = [str(v) for v in values]
        self.globals["read"] = self._read_hook

    def _read_hook(self, prompt=""):
        queue = getattr(self, "_inputs", [])
        if queue:
            val = queue.pop(0)
            self.output(u"%s%s" % (prompt, val))
            return val
        raise EOFError(u"Данных для read() не осталось. Передай значения через "
                       u"sandbox.feed_input(...).")

    def set_random_seed(self, seed):
        self.globals["random"].seed(seed)

    def inject(self, **names):
        """Передать в код ученика объекты (actor, canvas_api, check...)."""
        self.globals.update(names)
        self.globals["read"] = self._read_hook

    # ------------------------------------------------------------- запуск
    def run(self, source):
        """Выполнить код. Возвращает True, если ошибок нет."""
        self.runs += 1
        self.last_error = None
        self.last_exception = None
        try:
            compiled, problems = protect_source(source, self.iteration_limit)
        except SyntaxError as e:
            self._report(e)
            return False
        if problems:
            for p in problems:
                self.output(u"[ЗАПРЕЩЕНО] " + p)
            self.last_error = u"[ЗАПРЕЩЕНО] " + problems[0]
            self.last_exception = ValueError(problems[0])
            return False
        if isinstance(compiled, str):
            try:
                compiled = compile(compiled, "<ученик>", "exec")
            except SyntaxError as e:
                self._report(e)
                return False
        start = time.time()
        try:
            exec(compiled, self.globals, self.globals)
            return True
        except (SandboxLoopLimit, SandboxTimeout) as e:
            self._report(e)
            return False
        except KeyboardInterrupt:
            self.output(u"[ОСТАНОВЛЕНО] Выполнение прервано.")
            return False
        except BaseException as e:  # noqa: BLE001 — показываем всё, кроме SystemExit
            if isinstance(e, (SystemExit,)):
                self.output(u"[ЗАПРЕЩЕНО] Программа не может завершить игру.")
                return False
            self._report(e)
            return False
        finally:
            dur = time.time() - start
            if dur > self.timeout_sec:
                self.output(u"[ВРЕМЯ] Код выполнялся %.1f сек — проверь циклы." % dur)

    def _report(self, exc):
        # last_error — человекочитаемое русское сообщение (совместимо со str());
        # last_exception — оригинальный объект исключения для отладки.
        self.last_error = u" | ".join(translate_exception(exc))
        self.last_exception = exc
        for line in translate_exception(exc):
            self.output(line)

    # ----------------------------------------------------- автопроверки задач
    def capture_print(self, source):
        """Выполнить код и вернуть список строк, выведенных print()."""
        collected = []
        old = self.output
        self.output = lambda s: collected.append(s)
        ok = self.run(source)
        self.output = old
        return ok, collected

    def eval_expr(self, expr):
        """Вычислить выражение в среде песочницы (для автопроверки задач)."""
        try:
            return True, eval(expr, self.globals, self.globals)
        except BaseException as e:  # noqa: BLE001
            return False, translate_exception(e)[0]
