# -*- coding: utf-8 -*-
"""Урок 9 — «Гидропонные теплицы» (Модуль 2, КТП: Цикл со счётчиком и перебор).

Хронометраж 45 минут:
  * stage_1_theory    (7 мин) — цикл for, функция range(start, stop, step),
    отличие цикла со счётчиком (for) от цикла с предусловием (while);
  * stage_2_simulator (8 мин) — живой конвейер теплицы: код ученика
    превращается в грядки-ячейки памяти (SimCanvas, режим Б);
  * stage_3_practice  (15 мин) — 3 задачи: полив грядок по номерам,
    обратный отсчёт прогрева генератора, шаг range();
  * stage_4_boss      (10 мин) — аварийный обход всех 24 секторов купола;
  * stage_5_quiz      (5 мин) — 5 вопросов, оценка 2–5, чекпоинт в профиле.
"""

import ast

from levels.base_level import BaseLevel


def _node(nid, kind, text):
    return {"id": nid, "kind": kind, "text": text}


class Level09(BaseLevel):
    """Гидропоника Нова-Терры: цикл for и семейство range()."""

    LEVEL_NUMBER = 9

    def __init__(self):
        BaseLevel.__init__(self, {
            "number": 9,
            "title": u"Гидропонные теплицы",
            "theme": u"Цикл со счётчиком. Оператор for, функция "
                     u"range(start, stop, step), отличие for от while",
            "goal": u"Настроить автополив 10 грядок теплицы циклом for и "
                    u"запустить обратный отсчёт прогрева генератора",
            "xp_reward": 80,
        })
        self.stage_minutes = (7, 8, 15, 10, 5)

        # ------------------------------- этап 1: теория + блок-схема
        self.theory = (
            u"🌱 КУПОЛ «ДЕЛЬТА» ЗАСЕЯН! ГРЯДКИ НУЖНО ПОЛИТЬ ПО ПОРЯДКУ!\n\n"
            u"Исполнитель НЕ ЛЮБИТ повторять одну команду руками 10 раз. "
            u"Для перебора по порядку служит ЦИКЛ С СЧЁТЧИКОМ — for:\n\n"
            u"   for i in range(10):\n"
            u"       print(i)\n\n"
            u"Тело цикла (4 пробела!) выполняется столько раз, сколько "
            u"элементов отдаёт range(). Счётчик i сам принимает значения "
            u"0, 1, 2, ... — нам не нужно увеличивать его вручную.\n\n"
            u"СЕМЕЙСТВО range():\n"
            u"   range(5)        -> 0 1 2 3 4        (от 0, до 5 НЕ включая)\n"
            u"   range(1, 6)     -> 1 2 3 4 5        (старт включён, стоп нет)\n"
            u"   range(0, 20, 5) -> 0 5 10 15        (шаг = 5)\n"
            u"   range(5, 0, -1) -> 5 4 3 2 1        (ОТРИЦАТЕЛЬНЫЙ шаг — назад!)\n\n"
            u"ЧЕМ for ОТЛИЧАЕТСЯ ОТ while:\n"
            u"   while — исполнитель САМ проверяет условие и САМ меняет счётчик "
            u"(лёгко забыть += 1 и зациклиться);\n"
            u"   for   — счётчик выдаёт готовый ряд значений, цикл всегда "
            u"ЗАВЕРШИТСЯ, когда ряд закончится.\n\n"
            u"Правило безопасности Nova-Terra: если нужно пройтись по всем "
            u"объектам базы — бери for + range().")
        self.flowchart = {
            "nodes": [
                _node("start", "start", u"Старт: система полива"),
                _node("r", "process", u"i = следующий из range(1, 11)"),
                _node("d", "condition", u"Ряд range() не пуст?"),
                _node("w", "process", u"gryadka[i] = 'полита'"),
                _node("p", "io", u"print(f\"Грядка {i}: полив\")"),
                _node("e", "end", u"Конец: 10 грядок залиты"),
            ],
            "edges": [("start", "r"), ("r", "d"), ("d", "w"), ("w", "p"),
                      ("p", "r"), ("d", "e")],
        }

        # --------------------------------------- этап 2: симулятор
        self.simulator = {
            "mode": "memory",
            "variables": {u"i": u"int: 0", u"voda": u"int: 100",
                          u"polito": u"int: 0"},
            "lists": [u"range(10)     -> 0 1 2 3 4 5 6 7 8 9",
                      u"range(1, 11)  -> 1 2 3 4 5 6 7 8 9 10",
                      u"range(0, 21, 5)-> 0 5 10 15 20",
                      u"range(3, 0, -1)-> 3 2 1"],
            "title": u"Пульт теплицы: счётчик ряда полива",
        }

        # ---------------------------------------- этап 3: практика
        self.tasks = [
            {
                "prompt": u"Автополив: у тебя 10 грядок с 1-й по 10-ю. "
                          u"Циклом for и range() выведи для каждой строку "
                          u"«Грядка N: полив» (N — номер от 1 до 10). "
                          u"Используй f-строку.",
                "starter": u"# 10 грядок: нумерация с 1\n",
                "hint": u"for i in range(1, 11):\n"
                        u'    print(f"Грядка {i}: полив")',
                "expect_print": [u"Грядка 1: полив", u"Грядка 10: полив"],
                "expect_print_count": 10,
                "prints_in_order": True,
                "forbidden": ["while"],
            },
            {
                "prompt": u"Прогрев генератора: запусти обратный отсчёт "
                          u"ОТ 5 ДО 1 циклом for с отрицательным шагом "
                          u"range(5, 0, -1) — печатай каждое число, а после "
                          u"цикла выведи «ПРОГРЕВ ОК». Итого 6 строк.",
                "starter": u"# обратный отсчёт: 5 4 3 2 1\n",
                "hint": u"for i in range(5, 0, -1):\n"
                        u"    print(i)\n"
                        u'print("ПРОГРЕВ ОК")',
                "expect_print": [u"5", u"1", u"ПРОГРЕВ ОК"],
                "expect_print_count": 6,
                "prints_in_order": True,
            },
            {
                "prompt": u"Шаг датчиков: в ряду 20 метров датчики стоят "
                          u"каждые 5 м (0, 5, 10, 15). Пройди их циклом "
                          u"for + range(0, 20, 5) и напечатай каждый метр "
                          u"отдельной строкой. В конце посчитай переменную "
                          u"kolichestvo — сколько точек пройдено (через += 1 "
                          u"внутри цикла) и выведи её.",
                "starter": u"kolichestvo = 0\n",
                "hint": u"kolichestvo = 0\n"
                        u"for m in range(0, 20, 5):\n"
                        u"    print(m)\n"
                        u"    kolichestvo += 1\n"
                        u"print(kolichestvo)",
                "expect_print": [u"0", u"5", u"10", u"15", u"4"],
                "expect_print_count": 5,
                "assert_vars": {"kolichestvo": 4},
            },
        ]

        # ------------------------------------------ этап 4: босс
        self.boss = {
            "title": u"Аварийный обход купола «Дельта»",
            "mode": "console",
            "desc": u"БОСС: прорвало трубу хладагента! Нужно ПОВТОРИТЬ "
                    u"штатный протокол — обойти циклом for ВСЕ 24 сектора "
                    u"купольной теплицы (номера 1..24) и напечатать ровно "
                    u"25 строк: сначала 24 строки вида «Сектор N: норма», "
                    u"затем одна строка «КУПОЛ ЗАЩИЩЕН». Никаких while — "
                    u"только for + range()!",
            "starter": u"# обход секторов 1..24\n",
            "expect_print": [u"Сектор 1: норма", u"Сектор 24: норма",
                             u"КУПОЛ ЗАЩИЩЕН"],
            "expect_print_count": 25,
            "prints_in_order": True,
            "forbidden": ["while"],
        }

        # ------------------------------------------- этап 5: тест
        self.quiz = [
            {
                "q": u"Какие числа выдаёт range(5)?",
                "options": [u"0 1 2 3 4", u"1 2 3 4 5", u"0 1 2 3 4 5",
                            u"5 5 5 5 5"],
                "answer": 0,
            },
            {
                "q": u"Сколько раз выполнится тело цикла for i in range(2, 8)?",
                "options": [u"6 раз", u"8 раз", u"2 раза", u"7 раз"],
                "answer": 0,
            },
            {
                "q": u"Что делает range(10, 0, -2)?",
                "options": [u"10 8 6 4 2", u"10 9 8 ... 1",
                            u"0 2 4 6 8 10", u"бесконечный цикл"],
                "answer": 0,
            },
            {
                "q": u"Главное отличие for от while:",
                "options": [u"for перебирает готовый ряд значений и всегда "
                            u"завершается, while требует условия и ручной "
                            u"смены счётчика",
                            u"for работает только с числами меньше 10",
                            u"while быстрее, чем for",
                            u"различий нет"],
                "answer": 0,
            },
            {
                "q": u"Зачем после заголовка for ставить 4 пробела?",
                "options": [u"это тело цикла — повторяемые команды",
                            u"так красивее",
                            u"чтобы закрыть программу",
                            u"пробелы не нужны"],
                "answer": 0,
            },
        ]

    # ----------------------------------------------------- этап 2: симулятор
    def get_simulator_spec(self):
        """Живой пульт: переменные кода ученика + развёртка его range()."""
        code = getattr(self, "_student_code", "") or ""
        cells = self._scan(code)
        if not cells:
            cells = {u"i": u"int: ? (счётчик ряда)",
                     u"polito": u"int: 0"}
        rows = self._ranges(code) or [u"range(10) -> 0..9",
                                      u"range(1, 11) -> 1..10"]
        return {
            "mode": "memory",
            "variables": cells,
            "lists": rows,
            "title": u"Пульт теплицы: ряды range()",
        }

    def set_student_code(self, code):
        """GUI сообщает уровню текущий код редактора для живого пульта."""
        self._student_code = code or ""

    @staticmethod
    def _scan(code):
        cells = {}
        for raw in code.splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            try:
                tree = ast.parse(line)
            except SyntaxError:
                continue
            stmt = tree.body[0] if tree.body else None
            if isinstance(stmt, ast.Assign) and isinstance(stmt.targets[0],
                                                           ast.Name):
                name = stmt.targets[0].id
                try:
                    value = ast.literal_eval(stmt.value)
                    cells[name] = u"%s: %s" % (type(value).__name__,
                                               repr(value))[:22]
                except Exception:
                    cells[name] = u"вычисляется…"
            elif isinstance(stmt, ast.For) and isinstance(stmt.target,
                                                          ast.Name):
                cells[stmt.target.id] = u"счётчик for"
        return cells

    @staticmethod
    def _ranges(code):
        """Развернуть все вызовы range(...) из кода ученика в читаемые ряды."""
        out = []
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return out
        for node in ast.walk(tree):
            if (isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Name)
                    and node.func.id == "range"):
                try:
                    args = [ast.literal_eval(a) for a in node.args]
                except Exception:
                    continue
                seq = list(range(*args))
                shown = seq[:8]
                tail = u" …" if len(seq) > 8 else u""
                kw = u", ".join(repr(a) for a in args)
                out.append(u"range(%s) -> %s%s [%d шт]"
                           % (kw, shown, tail, len(seq)))
            if len(out) >= 4:
                break
        return out

    # ---------------------------------------------------- этап 3: автопроверка
    def check_task(self, sandbox, source, index):
        task = self.get_task(index)
        if not task:
            return False, u"Задача не задана."
        ok, feedback = BaseLevel.check_task(task, sandbox, source)
        if ok:
            feedback = u"✅ Полив секции настроен! " + feedback
        elif u"range" in feedback or u"ровно" in feedback:
            feedback += (u"\n💡 Совет: range(stop) начинается с 0; "
                         u"range(start, stop) не включает stop.")
        return ok, feedback

    # --------------------------------------------------------- этап 4: босс
    def check_console_boss(self, sandbox, source):
        ok, feedback = BaseLevel.check_console_boss(self, sandbox, source)
        if ok:
            feedback = (u"🏆 БОСС ПОВЕРЖЕН: все 24 сектора купола «Дельта» "
                        u"обойдены циклом for, течь локализована! " + feedback)
        return ok, feedback
