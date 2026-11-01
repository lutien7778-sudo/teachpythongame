# -*- coding: utf-8 -*-
"""Урок 12 — «Лаборатория анализа» (Модуль 2, КТП: Алгоритмы на списках).

Хронометраж 45 минут:
  * stage_1_theory    (7 мин) — линейный поиск, ручной поиск максимума и
    минимума через цикл for (без встроенных max()/min()), фильтрация;
  * stage_2_simulator (8 мин) — осциллограф лаборатории: список батарей из
    кода ученика рисуется матрицей ячеек (SimCanvas, режим Б);
  * stage_3_practice  (15 мин) — 3 задачи: линейный поиск дефекта, максимум
    партии вручную, фильтрация бракованных элементов в новый список;
  * stage_4_boss      (10 мин) — аттестация всей партии аккумуляторов;
  * stage_5_quiz      (5 мин) — 5 вопросов, оценка 2–5, чекpoинт в профиле.
"""

import ast

from levels.base_level import BaseLevel


def _node(nid, kind, text):
    return {"id": nid, "kind": kind, "text": text}


class Level12(BaseLevel):
    """Лаборатория Нова-Терры: алгоритмы поиска и фильтрации на списках."""

    LEVEL_NUMBER = 12

    #: Эталонная партия аккумуляторов (ёмкость мА·ч) для симулятора.
    PARTIYA = [820, 910, 45, 760, 930, 12, 880]

    def __init__(self):
        BaseLevel.__init__(self, {
            "number": 12,
            "title": u"Лаборатория анализа",
            "theme": u"Алгоритмы на списках: линейный поиск, ручной поиск "
                     u"максимума/минимума циклом for, фильтрация",
            "goal": u"Найти лучший и бракованный аккумулятор партии без "
                    u"функций max()/min() — только циклом и условием",
            "xp_reward": 90,
        })
        self.stage_minutes = (7, 8, 15, 10, 5)

        # ------------------------------- этап 1: теория + блок-схема
        self.theory = (
            u"🔬 ЛАБОРАТОРИЯ ПРИНЯЛА ПАРТИЮ АККУМУЛЯТОРОВ! ИЩЕМ ЗАКОНОМЕРНОСТИ.\n\n"
            u"ЛИНЕЙНЫЙ ПОИСК — самая честная стратегия: идем по списку с начала "
            u"и сравниваем каждый элемент с искомым:\n\n"
            u"   for element in partiya:\n"
            u"       if element == 45:\n"
            u'           print("Брак найден!")\n\n'
            u"РУЧНОЙ ПОИСК МАКСИМУМА (без max()). Берем гипотезу — первый "
            u"элемент — и улучшаем её на каждом шаге:\n\n"
            u"   maksimum = partiya[0]\n"
            u"   for e in partiya:\n"
            u"       if e > maksimum:\n"
            u"           maksimum = e\n\n"
            u"МИНИМУМ ищется зеркально: minimum = partiya[0], сравнение e < "
            u"minimum. Почему нельзя начать с 0? Потому что вся партия может "
            u"быть больше нуля — и тогда ответ будет неверным!\n\n"
            u"ФИЛЬТРАЦИЯ — переносим в НОВЫЙ список только годные элементы:\n\n"
            u"   good = []\n"
            u"   for e in partiya:\n"
            u"       if e >= 100:\n"
            u"           good.append(e)\n\n"
            u"Индекс элемента даёт enumerate(): for i, e in enumerate(sklad) — "
            u"так узнают, НА КАКОЙ позиции лежит брак.")
        self.flowchart = {
            "nodes": [
                _node("start", "start", u"Старт: hypothesis = a[0]"),
                _node("f", "process", u"e = следующий из a"),
                _node("c", "condition", u"e > maksimum?"),
                _node("u", "process", u"maksimum = e"),
                _node("k", "condition", u"Ряд кончился?"),
                _node("p", "io", u"print(maksimum)"),
                _node("e", "end", u"Конец: рекорд известен"),
            ],
            "edges": [("start", "f"), ("f", "c"), ("c", "u"),
                      ("u", "k"), ("c", "k"), ("k", "f"),
                      ("k", "p"), ("p", "e")],
        }

        # --------------------------------------- этап 2: симулятор
        self.simulator = {
            "mode": "memory",
            "variables": {u"partiya": u"list: 7", u"maksimum": u"int: 820"},
            "lists": [u"[0] 820", u"[1] 910", u"[2] 45 <- брак",
                      u"[3] 760", u"[4] 930 <- рекорд", u"[5] 12 <- брак",
                      u"[6] 880"],
            "title": u"Осциллограф партии",
        }

        # ---------------------------------------- этап 3: практика
        self.tasks = [
            {
                "prompt": u"Линейный поиск: дан список temperatura = [12, -3, "
                          u"7, -8, 4]. Пройди его циклом for и напечатай "
                          u"каждое ОТРИЦАТЕЛЬНОЕ значение (условие e < 0). "
                          u"Ожидаемый вывод: две строки -3 и -8.",
                "starter": u"temperatura = [12, -3, 7, -8, 4]\n",
                "hint": u"for t in temperatura:\n"
                        u"    if t < 0:\n"
                        u"        print(t)",
                "expect_print": [u"-3", u"-8"],
                "prints_in_order": True,
                "expect_print_count": 2,
                "forbidden": [u"max(", u"min("],
            },
            {
                "prompt": u"Ручной максимум: найди наибольшую ёмкость партии "
                          u"partiya = [820, 910, 45, 760, 930] БЕЗ функций "
                          u"max()/min(). Гипотеза maksimum = partiya[0], далее "
                          u"в цикле for при e > maksimum обновляй её и в конце "
                          u"напечатай.",
                "starter": u"partiya = [820, 910, 45, 760, 930]\n",
                "hint": u"maksimum = partiya[0]\n"
                        u"for e in partiya:\n"
                        u"    if e > maksimum:\n"
                        u"        maksimum = e\n"
                        u"print(maksimum)",
                "expect_print": [u"930"],
                "expect_print_count": 1,
                "assert_vars": {"maksimum": 930},
                "forbidden": [u"max(", u"sorted("],
            },
            {
                "prompt": u"Фильтрация брака: годным считается аккумулятор не "
                          u"меньше 100 мА·ч. Из lista = [820, 45, 910, 12, "
                          u"760] собери ЦИКЛОМ новый список good (через "
                          u".append()) и напечатай его одной строкой.",
                "starter": u"lista = [820, 45, 910, 12, 760]\ngood = []\n",
                "hint": u"for e in lista:\n"
                        u"    if e >= 100:\n"
                        u"        good.append(e)\n"
                        u"print(good)",
                "expect_print": [u"[820, 910, 760]"],
                "expect_print_count": 1,
                "assert_vars": {"good": [820, 910, 760]},
                "forbidden": [u"filter(", u"max(", u"min("],
            },
        ]

        # ------------------------------------------ этап 4: босс
        self.boss = {
            "title": u"Аттестация главной партии реактора",
            "mode": "console",
            "desc": u"БОСС: лаборатория должна выдать сертификат на партию "
                    u"partiya = [820, 910, 45, 760, 930, 12, 880]. ОДНИМ "
                    u"циклом for найди вручную минимум и максимум (без "
                    u"max/min/sorted!) и выведи ровно 4 строки в порядке:\n"
                    u"«Минимум: 12», «Максимум: 930», «Разброс: 918» "
                    u"(это maksimum - minimum), затем «СЕРТИФИКАТ ВЫДАН». "
                    u"Перепутаешь знак сравнения — партию завернут!",
            "starter": u"partiya = [820, 910, 45, 760, 930, 12, 880]\n",
            "expect_print": [u"Минимум: 12", u"Максимум: 930",
                             u"Разброс: 918", u"СЕРТИФИКАТ ВЫДАН"],
            "expect_print_count": 4,
            "prints_in_order": True,
            "assert_vars": {},
            "forbidden": [u"max(", u"min(", u"sorted("],
        }

        # ------------------------------------------- этап 5: тест
        self.quiz = [
            {
                "q": u"Что делает линейный поиск?",
                "options": [u"перебирает элементы по одному до совпадения",
                            u"делит список пополам",
                            u"сортирует список",
                            u"читает последний элемент"],
                "answer": 0,
            },
            {
                "q": u"С чего правильно начинать ручной поиск максимума?",
                "options": [u"с первого элемента списка a[0]",
                            u"с нуля",
                            u"с самого большого числа",
                            u"с середины списка"],
                "answer": 0,
            },
            {
                "q": u"Почему hypothesis minimum = 0 опасна?",
                "options": [u"все элементы могут быть больше 0 и ответ "
                            u"останется ложным",
                            u"0 — запрещённое число",
                            u"Python не умеет сравнивать с 0",
                            u"опасности нет"],
                "answer": 0,
            },
            {
                "q": u"Зачем при фильтрации создают НОВЫЙ пустой список?",
                "options": [u"чтобы не ломать исходные данные цеха",
                            u"старый список занимает память",
                            u"иначе не работает for",
                            u"это требование Python"],
                "answer": 0,
            },
            {
                "q": u"Что даст enumerate(lista)?",
                "options": [u"пары (индекс, элемент) на каждом шаге цикла",
                            u"только индексы",
                            u"отсортированный список",
                            u"длину списка"],
                "answer": 0,
            },
        ]

    # ----------------------------------------------------- этап 2: симулятор
    def get_simulator_spec(self):
        """Живой осциллограф: числовой список из кода ученика."""
        code = getattr(self, "_student_code", "") or ""
        nums = self._scan_numbers(code) or list(self.PARTIYA)
        cells = {}
        rows = []
        for i, v in enumerate(nums[:10]):
            tag = u" ← брак" if isinstance(v, (int, float)) and v < 100 else u""
            cells[u"[%d]" % i] = cut(v) + tag
            rows.append(u"[%d] = %s%s" % (i, v, tag))
        hi = max((v for v in nums if isinstance(v, (int, float))), default=None)
        lo = min((v for v in nums if isinstance(v, (int, float))), default=None)
        if hi is not None:
            cells[u"максимум"] = u"int: %s" % hi
            cells[u"минимум"] = u"int: %s" % lo
        return {
            "mode": "memory",
            "variables": cells,
            "lists": rows[:10],
            "title": u"Осциллограф партии (%d шт)" % len(nums),
        }

    def set_student_code(self, code):
        """GUI сообщает уровню текущий код редактора для живого графика."""
        self._student_code = code or ""

    @staticmethod
    def _scan_numbers(code):
        """Первый список целых чисел из кода ученика (для осциллографа)."""
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return []
        for node in ast.walk(tree):
            if isinstance(node, ast.List):
                vals = []
                for elt in node.elts:
                    try:
                        v = ast.literal_eval(elt)
                    except Exception:
                        v = None
                    if isinstance(v, (int, float)):
                        vals.append(v)
                if len(vals) >= 2:
                    return vals
        return []

    # ---------------------------------------------------- этап 3: автопроверка
    def check_task(self, sandbox, source, index):
        task = self.get_task(index)
        if not task:
            return False, u"Задача не задана."
        ok, feedback = BaseLevel.check_task(task, sandbox, source)
        if ok:
            feedback = u"✅ Анализ партии принят! " + feedback
        elif u"maksimum" in str(task.get("prompt", "")):
            feedback += (u"\n💡 Совет: бери гипотезу a[0] и обнови её только "
                         u"когда встретишь больший элемент.")
        return ok, feedback

    # --------------------------------------------------------- этап 4: босс
    def check_console_boss(self, sandbox, source):
        ok, feedback = BaseLevel.check_console_boss(self, sandbox, source)
        if ok:
            feedback = (u"🏆 БОСС ПОВЕРЖЕН: сертификат выдан — разброс партии "
                        u"12..930 мА·ч рассчитан вручную одним циклом! "
                        + feedback)
        return ok, feedback


def cut(text, limit=14):
    """Короткая подпись значения для ячеек канвы."""
    s = str(text)
    return s if len(s) <= limit else s[:limit - 1] + u"…"
