# -*- coding: utf-8 -*-
"""Урок 16 — «Проект Модуля 2: Экспедиция в пещеры» (КТП: Консольный Roguelike).

Итоговый проект модуля — синтез тем уроков 9–15: словари, матрицы, функции,
циклы. Хронометраж 45 минут:
  * stage_1_theory    (7 мин) — архитектура roguelike: карта-матрица, игрок,
    инвентарь, цикл хода;
  * stage_2_simulator (8 мин) — пещерный радар: карта из кода ученика
    рисуется сеткой (SimCanvas, режим Б);
  * stage_3_practice  (15 мин) — 3 задачи: функция печати карты, перемещение
    по команде, сбор кристаллов в инвентарь-словарь;
  * stage_4_boss      (10 мин) — полный проход пещеры 5x5: заряд, шаги,
    кристаллы, победа над тьмой;
  * stage_5_quiz      (5 мин) — 5 вопросов, оценка 2–5, чекпоинт в профиле.
"""

import ast

from levels.base_level import BaseLevel


def _node(nid, kind, text):
    return {"id": nid, "kind": kind, "text": text}


class Level16(BaseLevel):
    """Экспедиция в пещеры: консольный roguelike из всего Модуля 2."""

    LEVEL_NUMBER = 16

    #: Эталонная карта пещеры для симулятора ('#' стена, '.' грот,
    #: '@' ровер, '*' кристалл, 'E' выход).
    SAMPLE = [["#", "#", "#", "#"],
              ["#", "@", ".", "*"],
              ["#", "#", ".", "E"],
              ["#", "#", "#", "#"]]

    def __init__(self):
        BaseLevel.__init__(self, {
            "number": 16,
            "title": u"Проект Модуля 2: Экспедиция в пещеры",
            "theme": u"Консольный Roguelike: синтез циклов, списков, словарей, "
                     u"матриц и функций",
            "goal": u"Провести ровер через пещеру: карта 5x5, заряд батареи, "
                    u"сбор кристаллов в инвентарь, выход к шлюзу",
            "xp_reward": 150,
        })
        self.stage_minutes = (7, 8, 15, 10, 5)

        # ------------------------------- этап 1: теория + блок-схема
        self.theory = (
            u"⛏ ПРОЕКТ МОДУЛЯ 2! ПЕЩЕРЫ НОВА-ТЕРРЫ ЖДУТ РОВЕР.\n\n"
            u"CONSOLE ROGUELIKE собирается из четырёх блоков, которые ты уже "
            u"знаешь:\n\n"
            u"1) КАРТА — матрица kart[y][x]: '#' скала, '.' грот, '*' "
            u"кристалл, 'E' выход, '@' ровер;\n"
            u"2) СОСТОЯНИЕ — словарь sost = {\"y\": 0, \"x\": 0, \"zaryad\": "
            u"10, \"kristally\": 0};\n"
            u"3) ФУНКЦИИ — pechat_karty(kart) печатает строки циклом for, "
            u"hod(sost, komanda) меняет координаты;\n"
            u"4) ИГРОВОЙ ЦИКЛ — for komanda in plan: делаем ход, тратим "
            u"заряд, собираем кристаллы.\n\n"
            u"Правила экспедиции: каждый ход стоит 1 заряд; шаг на '*' "
            u"превращается в '+'1 кристалл; шаг на 'E' — победа; в стену "
            u"'#' идти нельзя (условие if kart[ny][nx] != '#').\n\n"
            u"Команда задаётся текстом: vverh, vniz, vlevo, vpravo — и "
            u"обрабатывается каскадом if/elif. Так из кубиков уроков 9–15 "
            u"строится настоящая игра!")
        self.flowchart = {
            "nodes": [
                _node("start", "start", u"Старт: sost = {y,x,zaryad}"),
                _node("l", "process", u"komanda = следующая из plan"),
                _node("c1", "condition", u"kart[ny][nx] == '#' ?"),
                _node("sk", "process", u"shag: y,x izmeneny, zaryad - 1"),
                _node("c2", "condition", u"kletka == '*' ?"),
                _node("kr", "process", u"kristally += 1"),
                _node("c3", "condition", u"kletka == 'E' ?"),
                _node("w", "io", u"print('ПОБЕДА')"),
                _node("e", "end", u"Конец: отчёт экспедиции"),
            ],
            "edges": [("start", "l"), ("l", "c1"), ("c1", "sk"),
                      ("sk", "c2"), ("c2", "kr"), ("kr", "c3"),
                      ("c2", "c3"), ("c3", "w"), ("w", "e"),
                      ("c1", "l"), ("c3", "l")],
        }

        # --------------------------------------- этап 2: симулятор
        self.simulator = {
            "mode": "memory",
            "variables": {u"kart": u"list: list (4x4)",
                          u"sost": u"dict: 4",
                          u"sost['zaryad']": u"int: 10"},
            "lists": [u"# # # #", u"# @ . *", u"# # . E", u"# # # #"],
            "title": u"Пещерный радар",
        }

        # ---------------------------------------- этап 3: практика
        self.tasks = [
            {
                "prompt": u"Функция карты: напиши pechat_karty(kart), которая "
                          u"циклом for печатает каждую строку матрицы. "
                          u"Вызови её для kart = [['#','.'],['*','E']] и "
                          u"получи ровно 2 строки вывода: ['#', '.'] и "
                          u"['*', 'E'].",
                "starter": u"",
                "hint": u"def pechat_karty(kart):\n"
                        u"    for stroka in kart:\n"
                        u"        print(stroka)\n"
                        u"kart = [['#', '.'], ['*', 'E']]\n"
                        u"pechat_karty(kart)",
                "expect_print": [u"['#', '.']", u"['*', 'E']"],
                "prints_in_order": True,
                "expect_print_count": 2,
                "forbidden": [u"while"],
            },
            {
                "prompt": u"Шаг ровера: состояние sost = {\"y\": 1, \"x\": 1}. "
                          u"Команда vlevo уменьшает x на 1 (sost[\"x\"] -= 1 "
                          u"или sost[\"x\"] = sost[\"x\"] - 1). Выполни шаг и "
                          u"напечатай новые координаты двумя строками: y "
                          u"(ответ 1) и x (ответ 0).",
                "starter": u'sost = {"y": 1, "x": 1}\n',
                "hint": u'sost["x"] = sost["x"] - 1\n'
                        u'print(sost["y"])\nprint(sost["x"])',
                "expect_print": [u"1", u"0"],
                "prints_in_order": True,
                "expect_print_count": 2,
                "assert_vars": {"sost": {"y": 1, "x": 0}},
                "forbidden": [u"while"],
            },
            {
                "prompt": u"Сбор кристаллов: inventory = []. Циклом for "
                          u"пройди по списку клеток ['.', '*', '*', '.'] и "
                          u"каждый '*' добавляй в inventory методом append. "
                          u"В конце напечатай длину собранного инвентаря. "
                          u"Ожидаемый вывод: 2.",
                "starter": u"kletki = ['.', '*', '*', '.']\ninventory = []\n",
                "hint": u"for k in kletki:\n"
                        u"    if k == '*':\n"
                        u"        inventory.append(k)\n"
                        u"print(len(inventory))",
                "expect_print": [u"2"],
                "expect_print_count": 1,
                "assert_vars": {"inventory": ["*", "*"]},
                "forbidden": [u"while", u"count("],
            },
        ]

        # ------------------------------------------ этап 4: босс
        self.boss = {
            "title": u"Полный проход пещеры «Мгла»",
            "mode": "console",
            "desc": u"БОСС: собери весь проект roguelike в одном скрипте. "
                    u"Карта kart = [['#','#','#','#','#'], ['#','@','.','*',"
                    u"'#'], ['#','#','.','.','#'], ['#','*','.','E','#'], "
                    u"['#','#','#','#','#']]. Ровер стартует в клетке '@'.\n"
                    u"Маршрут свободен: (1,1) -> (1,2) -> (1,3 'кристалл') "
                    u"-> (2,3) -> (3,3 'выход E') — все 4 шага проходимы.\n"
                    u"План хода (цикл for по плану ['vpravo','vpravo',"
                    u"'vniz','vpravo']): на каждом шаге трать 1 заряд "
                    u"(zaryad -= 1), а если целевая клетка '*' — собирай "
                    u"кристалл (kristally += 1). Выведи РОВНО 4 строки:\n"
                    u"1) ШАГ: 1 (номер первого шага);\n"
                    u"2) ШАГ: 4 (последний номер шага после всего цикла);\n"
                    u"3) ЗАРЯД: 7 (было 10, минус 4 успешных шага);\n"
                    u"4) КРИСТАЛЛЫ: 1 (на пути встретился ровно один '*').\n"
                    u"Реализуй счётчики циклом — ручные константы не примут!",
            "starter": u"kart = [['#', '#', '#', '#', '#'], "
                       u"['#', '@', '.', '*', '#'], ['#', '#', '.', '.', "
                       u"'#'], ['#', '*', '.', 'E', '#'], ['#', '#', '#', "
                       u"'#', '#']]\nplan = ['vpravo', 'vpravo', 'vniz', "
                       u"'vpravo']\nzaryad = 10\nkristally = 0\n",
            "expect_print": [u"ШАГ: 1", u"ШАГ: 4", u"ЗАРЯД: 7",
                             u"КРИСТАЛЛЫ: 1"],
            "expect_print_count": 4,
            "prints_in_order": True,
            "assert_vars": {},
            "forbidden": [u"while"],
        }

        # ------------------------------------------- этап 5: тест
        self.quiz = [
            {
                "q": u"Чем удобна карта-матрица kart[y][x] в roguelike?",
                "options": [u"клетка доступна по двум координатам сразу",
                            u"она занимает меньше памяти, чем строка",
                            u"в ней нет циклов",
                            u"она заменяет словарь"],
                "answer": 0,
            },
            {
                "q": u"Где хранят состояние игрока (заряд, позиции, кристаллы)?",
                "options": [u"в словаре sost с именованными ключами",
                            u"в одном числе",
                            u"в комментарии",
                            u"в имени файла"],
                "answer": 0,
            },
            {
                "q": u"Зачем игровой цикл делают функцией hod(sost, komanda)?",
                "options": [u"чтобы один код хода вызывался для любой команды",
                            u"функции ускоряют Python",
                            u"без функций запретен for",
                            u"это случайность"],
                "answer": 0,
            },
            {
                "q": u"Как проверить, что ровер не идёт в стену '#'?",
                "options": [u"if kart[ny][nx] != '#': сделать шаг",
                            u"if kart == '#':",
                            u"print('#')",
                            u"kart.remove('#')"],
                "answer": 0,
            },
            {
                "q": u"Что произойдёт, если забыть тратить zaryad в цикле?",
                "options": [u"экспедиция станет бесконечно долгой — ресурс "
                            u"потеряет смысл",
                            u"Python выдаст SyntaxError",
                            u"карта исчезнет",
                            u"ничего страшного"],
                "answer": 0,
            },
        ]

    # ----------------------------------------------------- этап 2: симулятор
    def get_simulator_spec(self):
        """Живой пещерный радар: первая матрица из кода ученика."""
        code = getattr(self, "_student_code", "") or ""
        matrix = self._scan_matrix(code) or [list(r) for r in self.SAMPLE]
        rows = []
        cells = {u"kart": u"list: %dx%d" % (len(matrix),
                                            len(matrix[0]) if matrix else 0)}
        crystals = 0
        for y, row in enumerate(matrix[:6]):
            if not isinstance(row, list):
                continue
            line = u" ".join(str(c)[:3] for c in row[:12])
            crystals += sum(1 for c in row if str(c) == "'*'" or c == "*")
            rows.append(line)
            cells[u"kart[%d]" % y] = str(row)[:22]
        cells[u"kristally"] = u"int: %d" % crystals
        return {
            "mode": "memory",
            "variables": cells,
            "lists": rows,
            "title": u"Пещерный радар (%d рядов)" % len(matrix),
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
            feedback = u"✅ Модуль экспедиции собран! " + feedback
        else:
            feedback += (u"\n💡 Собери вместе блоки проекта: матрица карты, "
                         u"словарь состояния, цикл хода.")
        return ok, feedback

    # --------------------------------------------------------- этап 4: босс
    def check_console_boss(self, sandbox, source):
        ok, feedback = BaseLevel.check_console_boss(self, sandbox, source)
        if ok:
            feedback = (u"🏆 БОСС ПОВЕРЖЕН: пещера «Мгла» пройдена, кристаллы "
                        u"в инвентаре, ровер у шлюза! Модуль 2 закрыт. "
                        + feedback)
        return ok, feedback
