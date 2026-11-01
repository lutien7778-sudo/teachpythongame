# -*- coding: utf-8 -*-
"""Урок 10 — «Складской терминал» (Модуль 2, КТП: Списки — инвентарь базы).

Хронометраж 45 минут:
  * stage_1_theory    (7 мин) — коллекция list, нумерация с нуля,
    отрицательные индексы, функция len();
  * stage_2_simulator (8 мин) — складской радар: список ученика
    превращается в цепочку ячеек с индексами (SimCanvas, режим Б);
  * stage_3_practice  (15 мин) — 3 задачи: чтение по индексу,
    последний баллон через -1, подсчёт позиций len();
  * stage_4_boss      (10 мин) — полная инвентаризация склада;
  * stage_5_quiz      (5 мин) — 5 вопросов, оценка 2–5, чекпоинт в профиле.
"""

import ast

from levels.base_level import BaseLevel


def _node(nid, kind, text):
    return {"id": nid, "kind": kind, "text": text}


class Level10(BaseLevel):
    """Склад Нова-Терры: списки, индексы и длина."""

    LEVEL_NUMBER = 10

    #: Эталонный инвентарь склада для симулятора и легенды.
    SKLAD = [u"кислород", u"вода", u"пайки", u"фильтры", u"канаты"]

    def __init__(self):
        BaseLevel.__init__(self, {
            "number": 10,
            "title": u"Складской терминал",
            "theme": u"Списки list: элементы, индексы с нуля, "
                     u"отрицательные индексы, функция len()",
            "goal": u"Провести инвентаризацию контейнеров жизнеобеспечения "
                    u"базы: читать позиции по номеру и считать склад",
            "xp_reward": 80,
        })
        self.stage_minutes = (7, 8, 15, 10, 5)

        # ------------------------------- этап 1: теория + блок-схема
        self.theory = (
            u"📦 СКЛАДСКОЙ ТЕРМИНАЛ ОЖИД! ГРУЗЫ ХРАНИМ СПИСКАМИ.\n\n"
            u"Переменная — одна ячейка памяти. Когда грузов много, берём "
            u"СПИСОК (list) — колонку пронумерованных ячеек:\n\n"
            u"   sklad = [\"кислород\", \"вода\", \"пайки\", \"фильтры\"]\n\n"
            u"НУМЕРАЦИЯ НАЧИНАЕТСЯ С НУЛЯ (как в космической инструкции):\n"
            u"   sklad[0] -> \"кислород\"   (первый груз)\n"
            u"   sklad[1] -> \"вода\"\n"
            u"   sklad[3] -> \"фильтры\"    (четвёртый груз!)\n\n"
            u"ОТРИЦАТЕЛЬНЫЕ ИНДЕКСЫ считают с конца:\n"
            u"   sklad[-1] -> \"фильтры\"    (последний)\n"
            u"   sklad[-2] -> \"пайки\"      (предпоследний)\n\n"
            u"len(sklad) -> 4 — ДЛИНА списка, то есть количество ячеек.\n"
            u"Последний элемент всегда имеет индекс len(sklad) - 1.\n\n"
            u"Важно: индекс 4 в списке из 4 элементов — это ошибка IndexError!"
            u" Терминал разрешает доступ только к существующим ячейкам.\n\n"
            u"Список можно менять по индексу: sklad[1] = \"конденсат\".")
        self.flowchart = {
            "nodes": [
                _node("start", "start", u"Старт: карточка груза"),
                _node("r", "io", u"read() -> index"),
                _node("c", "condition", u"index < len(sklad)?"),
                _node("ok", "process", u"print(sklad[index])"),
                _node("err", "process", u"print('Нет такой ячейки')"),
                _node("e", "end", u"Конец: учёт ведётся"),
            ],
            "edges": [("start", "r"), ("r", "c"), ("c", "ok"),
                      ("c", "err"), ("ok", "e"), ("err", "e")],
        }

        # --------------------------------------- этап 2: симулятор
        self.simulator = {
            "mode": "memory",
            "variables": {u"sklad": u"list: 5", u"index": u"int: 0"},
            "lists": [u"[0] кислород", u"[1] вода", u"[2] пайки",
                      u"[3] фильтры", u"[4] канаты"],
            "matrices": [],
            "title": u"Складской радар: ячейки и индексы",
        }

        # ---------------------------------------- этап 3: практика
        self.tasks = [
            {
                "prompt": u"Создай список sklad = [\"кислород\", \"вода\", "
                          u"\"пайки\", \"фильтры\", \"канаты\"] и выведи "
                          u"элементы с индексами 0 и 2 каждой строкой через "
                          u"print(). Порядок вывода важен!",
                "starter": u"# список контейнеров жизнеобеспечения\n",
                "hint": u'sklad = ["кислород", "вода", "пайки", "фильтры",'
                        u' "канаты"]\n'
                        u"print(sklad[0])\n"
                        u"print(sklad[2])",
                "expect_print": [u"кислород", u"пайки"],
                "prints_in_order": True,
                "expect_print_count": 2,
                "assert_vars": {"sklad": [u"кислород", u"вода", u"пайки",
                                          u"фильтры", u"канаты"]},
            },
            {
                "prompt": u"Инженер просит ПОСЛЕДНИЙ контейнер со склада. "
                          u"Не читай его руками! Возьми element = sklad[-1] "
                          u"по отрицательному индексу и напечатай его.",
                "starter": u'sklad = ["кислород", "вода", "пайки", "фильтры",'
                           u' "канаты"]\n',
                "hint": u"element = sklad[-1]\nprint(element)",
                "expect_print": [u"канаты"],
                "expect_print_count": 1,
                "assert_vars": {"element": u"канаты"},
                "forbidden": [u"sklad[4]", u"sklad[5-1]"],
            },
            {
                "prompt": u"Сколько ячеек на складе? Посчитай длину списка "
                          u"функцией len() в переменную pozicii и выведи её. "
                          u"Затем замени вторую позицию (индекс 1) на "
                          u"\"конденсат\" — список должен стать ровным.",
                "starter": u'sklad = ["кислород", "вода", "пайки", "фильтры",'
                           u' "канаты"]\n',
                "hint": u"pozicii = len(sklad)\nprint(pozicii)\n"
                        u'sklad[1] = "конденсат"',
                "expect_print": [u"5"],
                "expect_print_count": 1,
                "assert_vars": {"pozicii": 5,
                                "sklad": [u"кислород", u"конденсат", u"пайки",
                                          u"фильтры", u"канаты"]},
            },
        ]

        # ------------------------------------------ этап 4: босс
        self.boss = {
            "title": u"Полная инвентаризация склада «Омега»",
            "mode": "console",
            "desc": u"БОСС: ревизия орбитального транспорта! Выведи ровно "
                    u"10 строк в таком порядке: сначала длина склада "
                    u"print(len(sklad)), затем ВСЕ элементы списка по порядку "
                    u"(каждый своей строкой), затем ПЕРВЫЙ элемент через "
                    u"индекс 0 и ПОСЛЕДНИЙ через индекс -1. "
                    u"Список: [\"кислород\", \"вода\", \"пайки\", \"фильтры\", "
                    u"\"канаты\", \"запчасти\", \"мед-набор\"]. "
                    u"Подсказка: цикл for element in sklad:",
            "starter": u'sklad = ["кислород", "вода", "пайки", "фильтры",'
                       u' "канаты", "запчасти", "мед-набор"]\n',
            "expect_print": [u"7", u"кислород", u"мед-набор"],
            "expect_print_count": 10,
            "prints_in_order": True,
            "inputs": [],
        }

        # ------------------------------------------- этап 5: тест
        self.quiz = [
            {
                "q": u"С какого номера начинается нумерация элементов списка?",
                "options": [u"с 0", u"с 1", u"с -1", u"нумерации нет"],
                "answer": 0,
            },
            {
                "q": u"Что вернёт a[-1] для любого непустого списка a?",
                "options": [u"последний элемент", u"первый элемент",
                            u"ошибку", u"длину списка"],
                "answer": 0,
            },
            {
                "q": u"Чему равно len([1, 2, 3])?",
                "options": [u"3", u"2", u"6", u"1"],
                "answer": 0,
            },
            {
                "q": u"Какой индекс обращается ко ВТОРОМУ элементу списка?",
                "options": [u"1", u"2", u"0", u"-2"],
                "answer": 0,
            },
            {
                "q": u"Почему a[5] для списка из 5 элементов даёт IndexError?",
                "options": [u"максимальный индекс такого списка — 4",
                            u"индексы нельзя писать цифрой",
                            u"списки поддерживают только 10 элементов",
                            u"нужно писать a(5)"],
                "answer": 0,
            },
        ]

    # ----------------------------------------------------- этап 2: симулятор
    def get_simulator_spec(self):
        """Живой складской радар: список из кода ученика по ячейкам."""
        code = getattr(self, "_student_code", "") or ""
        items = self._scan_lists(code) or self.SKLAD
        cells = {}
        for i, val in enumerate(items):
            cells[u"[%d]" % i] = unicode_cut(val)
        cells[u"len"] = u"int: %d" % len(items)
        return {
            "mode": "memory",
            "variables": cells,
            "lists": [u"%s -> [%d]" % (unicode_cut(v), i)
                      for i, v in enumerate(items)],
            "title": u"Складской радар: %d ячеек" % len(items),
        }

    def set_student_code(self, code):
        """GUI сообщает уровню текущий код редактора для живого радара."""
        self._student_code = code or ""

    @staticmethod
    def _scan_lists(code):
        """Найти первый литеральный список в коде ученика."""
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return []
        for node in ast.walk(tree):
            if isinstance(node, ast.List):
                out = []
                for elt in node.elts:
                    try:
                        out.append(repr(ast.literal_eval(elt)).strip("'\""))
                    except Exception:
                        out.append(u"…")
                return out[:12]
        return []

    # ---------------------------------------------------- этап 3: автопроверка
    def check_task(self, sandbox, source, index):
        task = self.get_task(index)
        if not task:
            return False, u"Задача не задана."
        ok, feedback = BaseLevel.check_task(task, sandbox, source)
        if ok:
            feedback = u"✅ Ячейка склада подтверждена! " + feedback
        elif u"IndexError" in feedback:
            feedback += (u"\n💡 Совет: первый элемент — это [0], а не [1]. "
                         u"Максимальный индекс = len(sklad) - 1.")
        return ok, feedback

    # --------------------------------------------------------- этап 4: босс
    def check_console_boss(self, sandbox, source):
        ok, feedback = BaseLevel.check_console_boss(self, sandbox, source)
        if ok:
            feedback = (u"🏆 БОСС ПОВЕРЖЕН: ревизия склада «Омега» закрыта — "
                        u"все 7 контейнеров сверены с манифестом! " + feedback)
        return ok, feedback


def unicode_cut(text, limit=18):
    """Короткая подпись значения для ячеек канвы."""
    s = str(text)
    return s if len(s) <= limit else s[:limit - 1] + u"…"
