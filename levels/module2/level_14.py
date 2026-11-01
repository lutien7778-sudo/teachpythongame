# -*- coding: utf-8 -*-
"""Урок 14 — «Топография кратера» (Модуль 2, КТП: Двумерные структуры).

Хронометраж 45 минут:
  * stage_1_theory    (7 мин) — вложенные списки matrix[y][x], двойной цикл for,
    символьная карта сектора (# стена, . пол, @ ровер);
  * stage_2_simulator (8 мин) — радар кратера: матрица из кода ученика
    рисуется сеткой ячеек (SimCanvas, режим Б);
  * stage_3_practice  (15 мин) — 3 задачи: чтение клетки, расстановка стен,
    обход карты двойным циклом;
  * stage_4_boss      (10 мин) — полное сканирование кратера и отчёт;
  * stage_5_quiz      (5 мин) — 5 вопросов, оценка 2–5, чекпоинт в профиле.
"""

import ast

from levels.base_level import BaseLevel


def _node(nid, kind, text):
    return {"id": nid, "kind": kind, "text": text}


class Level14(BaseLevel):
    """Топографическая служба Нова-Терры: двумерные таблицы."""

    LEVEL_NUMBER = 14

    #: Эталонная карта 3x3 для симулятора.
    SAMPLE = [["#", "#", "#"], ["#", "@", "."], ["#", "#", "#"]]

    def __init__(self):
        BaseLevel.__init__(self, {
            "number": 14,
            "title": u"Топография кратера",
            "theme": u"Двумерные структуры: вложенные списки matrix[y][x], "
                     u"вложенные циклы for, символьная карта",
            "goal": u"Построить карту сектора кратера и научится читать её "
                    u"по строкам и столбцам",
            "xp_reward": 100,
        })
        self.stage_minutes = (7, 8, 15, 10, 5)

        # ------------------------------- этап 1: теория + блок-схема
        self.theory = (
            u"🌋 СОСТАВЛЯЕМ КАРТУ КРАТЕРА! ВСЁ ДВИЖЕНИЕ — ПО СЕТКЕ.\n\n"
            u"СПИСОК СПИСКОВ (матрица) — это таблица: снаружи список СТРОК, "
            u"внутри каждой строки — список КЛЕТОК:\n\n"
            u"   kart = [ ['#', '#'],\n"
            u"           ['.', '@'] ]\n\n"
            u"Чтобы взять клетку, нужен ДВОЙНОЙ индекс: сначала номер строки "
            u"y, потом номер столбца x:\n\n"
            u'   print(kart[1][0])     # "." — вторая строка, первый столбец\n\n'
            u"ОБХОД ВЕСЬ КАРТЫ — вложенный цикл for: внешний бежит по "
            u"СТРОКАМ, внутренний — по КЛЕТКАМ строки:\n\n"
            u"   for stroka in kart:\n"
            u"       for kletka in stroka:\n"
            u"           print(kletka, end='')\n"
            u"       print()          # перевод строки после ряда\n\n"
            u"Обозначения карты Нова-Терры: '#' — скала (не пройти), "
            u"'.' — грунт (проходимо), '@' — наш ровер. Ровер ставится в "
            u"карту так же просто: kart[y][x] = '@'.")
        self.flowchart = {
            "nodes": [
                _node("start", "start", u"Старт: kart = карта кратера"),
                _node("fy", "process", u"stroka = следующая строка"),
                _node("fx", "process", u"kletka = следующая клетка"),
                _node("c", "condition", u"kletka == '#' ?"),
                _node("w", "process", u"print('#')  // скала"),
                _node("g", "process", u"print('.')  // грунт"),
                _node("n", "io", u"print() // конец ряда"),
                _node("e", "end", u"Конец: карта снята"),
            ],
            "edges": [("start", "fy"), ("fy", "fx"), ("fx", "c"),
                      ("c", "w"), ("c", "g"), ("w", "fx"), ("g", "fx"),
                      ("fx", "n"), ("n", "fy"), ("fy", "e")],
        }

        # --------------------------------------- этап 2: симулятор
        self.simulator = {
            "mode": "memory",
            "variables": {u"kart": u"list: list (3x3)",
                          u"kart[0]": u"['#', '#', '#']",
                          u"kart[1][1]": u"'@'"},
            "lists": [u"# # #", u"# @ .", u"# # #"],
            "title": u"Радар кратера",
        }

        # ---------------------------------------- этап 3: практика
        self.tasks = [
            {
                "prompt": u"Чтение клетки: дана карта kart = [['#', '.'], "
                          u"['.', '@']]. Напечатай символ со 2-й строки, "
                          u"1-го столбца (это kart[1][0]). Ожидаемый вывод: '.'",
                "starter": u"kart = [['#', '.'], ['.', '@']]\n",
                "hint": u"print(kart[1][0])",
                "expect_print": [u"."],
                "expect_print_count": 1,
                "forbidden": [u"while"],
            },
            {
                "prompt": u"Стена: в карте kart = [['.', '.', '.'], "
                          u"['.', '.', '.']] построй скалу — замени все три "
                          u"клетки ПЕРВОЙ строки на '#' (три присваивания "
                          u"вида kart[0][x] = '#') и напечатай первую строку. "
                          u"Ожидаемый вывод: ['#', '#', '#']",
                "starter": u"kart = [['.', '.', '.'], ['.', '.', '.']]\n",
                "hint": u"kart[0][0] = '#'\nkart[0][1] = '#'\n"
                        u"kart[0][2] = '#'\nprint(kart[0])",
                "expect_print": [u"['#', '#', '#']"],
                "expect_print_count": 1,
                "assert_vars": {"kart": [["#", "#", "#"], [".", ".", "."]]},
                "forbidden": [u"while"],
            },
            {
                "prompt": u"Обход двойным циклом: карта kart = [['a', 'b'], "
                          u"['c', 'd']]. Выведи КАЖДУЮ клетку отдельной "
                          u"строкой в порядке a, b, c, d (внешний for по "
                          u"stroka, внутренний for po kletke). Ровно 4 строки.",
                "starter": u"kart = [['a', 'b'], ['c', 'd']]\n",
                "hint": u"for stroka in kart:\n"
                        u"    for kletka in stroka:\n"
                        u"        print(kletka)",
                "expect_print": [u"a", u"b", u"c", u"d"],
                "prints_in_order": True,
                "expect_print_count": 4,
                "forbidden": [u"while"],
            },
        ]

        # ------------------------------------------ этап 4: босс
        self.boss = {
            "title": u"Полное сканирование кратера «Триглав»",
            "mode": "console",
            "desc": u"БОСС: топографы примут только полный снимок. Карта "
                    u"kart = [['#', '#', '#'], ['#', '@', '.'], "
                    u"['#', '#', '#']]. Задача:\n"
                    u"1) найди позицию ровера '@': посчитай y (номер строки) и "
                    u"x (номер столбца) ДВОЙНЫМ циклом for со счётчиками;\n"
                    u"2) напечатай СНАЧАЛА строку «СКАН: старт» — это строка "
                    u"№1;\n"
                    u"3) затем двойным обходом карты напечатай каждую КЛЕТКУ "
                    u"отдельной строкой (9 строк подряд: #, #, #, #, @, ., "
                    u"#, #, #);\n"
                    u"4) последней — строка «РОВЕР: 1 1» — координаты y и x "
                    u"через пробел. Итого ровно 11 строк вывода!",
            "starter": u"kart = [['#', '#', '#'], ['#', '@', '.'], ['#', '#', '#']]\n",
            "expect_print": [u"СКАН: старт", u"#", u"@", u".",
                             u"РОВЕР: 1 1"],
            "expect_print_count": 11,
            "prints_in_order": True,
            "assert_vars": {},
            "forbidden": [u"while", u"index("],
        }

        # ------------------------------------------- этап 5: тест
        self.quiz = [
            {
                "q": u"Как записать элемент 2-й строки, 3-го столбца матрицы m?",
                "options": [u"m[1][2]", u"m[2][1]", u"m[1, 2]", u"m(2)(3)"],
                "answer": 0,
            },
            {
                "q": u"Что хранит вложенный список [['#','.'],['.','@']]?",
                "options": [u"2 строки по 2 клетки — таблицу",
                            u"один длинный список",
                            u"словарь",
                            u"ничего"],
                "answer": 0,
            },
            {
                "q": u"Сколько всего клеток в матрице 3x4?",
                "options": [u"12", u"7", u"34", u"4"],
                "answer": 0,
            },
            {
                "q": u"Зачем во внешнем цикле печатают пустой print()?",
                "options": [u"чтобы переносить строку после каждого ряда карты",
                            u"для ускорения",
                            u"так требует Python",
                            u"он ничего не делает"],
                "answer": 0,
            },
            {
                "q": u"Что напечатает print(m[0]) для m = [['a','b'],['c','d']]?",
                "options": [u"['a', 'b'] — всю первую строку",
                            u"'a'", u"'b'", u"ошибку"],
                "answer": 0,
            },
        ]

    # ----------------------------------------------------- этап 2: симулятор
    def get_simulator_spec(self):
        """Живой радар: первая матрица (список списков) из кода ученика."""
        code = getattr(self, "_student_code", "") or ""
        matrix = self._scan_matrix(code) or [list(r) for r in self.SAMPLE]
        rows = []
        cells = {u"kart": u"list: %dx%d" % (len(matrix),
                                            len(matrix[0]) if matrix else 0)}
        for y, row in enumerate(matrix[:6]):
            if not isinstance(row, list):
                continue
            rows.append(u" ".join(str(c)[:3] for c in row[:12]))
            cells[u"kart[%d]" % y] = str(row)[:22]
        return {
            "mode": "memory",
            "variables": cells,
            "lists": rows,
            "title": u"Радар кратера (%d рядов)" % len(matrix),
        }

    def set_student_code(self, code):
        """GUI сообщает уровню текущий код редактора для живого радара."""
        self._student_code = code or ""

    @staticmethod
    def _scan_matrix(code):
        """Первый литеральный список списков из кода ученика."""
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return []
        for node in ast.walk(tree):
            if isinstance(node, ast.List) and node.elts:
                rows = []
                for elt in node.elts:
                    try:
                        v = ast.literal_eval(elt)
                    except Exception:
                        v = None
                    if isinstance(v, list):
                        rows.append(v)
                if rows:
                    return rows
        return []

    # ---------------------------------------------------- этап 3: автопроверка
    def check_task(self, sandbox, source, index):
        task = self.get_task(index)
        if not task:
            return False, u"Задача не задана."
        ok, feedback = BaseLevel.check_task(task, sandbox, source)
        if ok:
            feedback = u"✅ Топосъёмка принята! " + feedback
        else:
            feedback += (u"\n💡 Помни порядок индексов: сначала СТРОКА y, "
                         u"потом СТОЛБЕЦ x — kart[y][x].")
        return ok, feedback

    # --------------------------------------------------------- этап 4: босс
    def check_console_boss(self, sandbox, source):
        ok, feedback = BaseLevel.check_console_boss(self, sandbox, source)
        if ok:
            feedback = (u"🏆 БОСС ПОВЕРЖЕН: кратер «Триглав» нанесён на карту, "
                        u"ровер найден! " + feedback)
        return ok, feedback
