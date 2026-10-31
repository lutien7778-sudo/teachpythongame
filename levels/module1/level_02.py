# -*- coding: utf-8 -*-
"""Урок 2 — «Регистрация колониста» (Модуль 1, КТП: Память программы и ввод данных).

Хронометраж 45 минут:
  * stage_1_theory    (7 мин) — переменные как ячейки памяти, поток
    «Вход -> Память -> Выход», read() (учебная замена input()), f-строки;
  * stage_2_simulator (8 мин) — живой симулятор ячеек памяти: код ученика
    раскладывается на вход/память/выход (SimCanvas, режим Б);
  * stage_3_practice  (15 мин) — 3 задачи с автопроверкой значений переменных;
  * stage_4_boss      (10 мин) — калибровка скафандра: имя + числовые параметры;
  * stage_5_quiz      (5 мин) — 5 вопросов, оценка 2–5, чекпоинт в профиле.

Для ввода данных используется учебная функция ``read()`` — безопасная замена
``input()``: в GUI она открывает модальное окно ввода (эмуляция stdin).
"""

import ast

from levels.base_level import BaseLevel


def _node(nid, kind, text):
    return {"id": nid, "kind": kind, "text": text}


class Level02(BaseLevel):
    """Реестр колонистов: переменные-ячейки, ввод данных, f-строки."""

    LEVEL_NUMBER = 2

    def __init__(self):
        BaseLevel.__init__(self, {
            "number": 2,
            "title": u"Регистрация колониста",
            "theme": u"Память программы и ввод данных. Переменные, read(), "
                     u"f-строки",
            "goal": u"Завести карточку колониста в памяти базы: считать данные "
                    u"с пульта, сохранить их в переменные и вывести f-строкой",
            "xp_reward": 70,
        })
        self.stage_minutes = (7, 8, 15, 10, 5)

        # ------------------------------- этап 1: теория + блок-схема
        self.theory = (
            u"🧑‍🚀 СТАНЦИЯ РЕГИСТРАЦИИ КОЛОНИСТОВ ОТКРЫТА!\n\n"
            u"Программа — это конвейер из трёх частей:\n"
            u"   ВХОД  ->  ПАМЯТЬ  ->  ВЫХОД\n"
            u"Данные входят через read() (в этой игре — умный заменитель "
            u"input(): он открывает окошко пульта управления), хранятся в "
            u"ПЕРЕМЕННЫХ и выходят на экран через print().\n\n"
            u"ПЕРЕМЕННАЯ — это именованная ЯЧЕЙКА ПАМЯТИ. Знак = означает "
            u"«положить значение в ячейку»:\n"
            u"    imya = read(\"Как тебя зовут? \")   # ячейка imya пополнилась\n"
            u"    otryad = \"Альфа\"                   # строка в кавычках\n\n"
            u"Ячейку можно пополнять снова — старое значение стирается:\n"
            u"    kislorod = 20\n"
            u"    kislorod = 25      # теперь в ячейке 25\n\n"
            u"F-СТРОКА собирает текст прямо из ячеек — ставь букву f перед "
            u"кавычками, а переменные — в фигурные скобки {}:\n"
            u'    print(f"Колонист {imya}, отряд {otryad} зарегистрирован")\n\n'
            u"Проверь себя: если imya = 'Аня', то f\"Привет, {imya}!\" превратится"
            u" в строку «Привет, Аня!».")
        self.flowchart = {
            "nodes": [
                _node("start", "start", u"Старт: пульт регистрации"),
                _node("in", "io", u"imya = read('Имя')"),
                _node("mem", "process", u"otryad = 'Альфа'"),
                _node("cond", "condition", u"imya пустая?"),
                _node("yes", "process", u"imya = 'Безымянный'"),
                _node("out", "io", u"print(f'Карточка: {imya}')"),
                _node("end", "end", u"Конец: колонист в реестре"),
            ],
            "edges": [("start", "in"), ("in", "mem"), ("mem", "cond"),
                      ("cond", "yes", u"True"), ("cond", "out", u"False"),
                      ("yes", "out"), ("out", "end")],
        }

        # --------------------------------------- этап 2: симулятор
        self.simulator = {
            "mode": "memory",
            "variables": {u"imya": u"?", u"otryad": u"Альфа",
                          u"kislorod": 20},
            "lists": [u"ВХОД: read()", u"ПАМЯТЬ: imya, otryad",
                      u"ВЫХОД: print(f'...')"],
            "title": u"Ячейки памяти станции регистрации",
        }

        # ---------------------------------------- этап 3: практика
        self.tasks = [
            {
                "prompt": u"Создай две ячейки памяти: imya сохрани в неё своё "
                          u"имя колониста (строку), a klass — строку «Инженер». "
                          u"Выведи их через print().",
                "starter": u"# Шаг 1: imya = ...\n# Шаг 2: klass = ...\n"
                           u"# Шаг 3: print(...)\n",
                "hint": u"imya = \"Аня\"\nklass = \"Инженер\"\nprint(imya, klass)",
                "expect_vars": {"klass": u"Инженер"},
                "forbidden": ["input("],
            },
            {
                "prompt": u"Счётчик кислорода: создай ячейку kislorod = 20, "
                          u"затем ПОПОЛНИ её до 25 (та же переменная!) и выведи "
                          u"f-строкой «O2 в баллоне: 25».",
                "starter": u"",
                "hint": u"kislorod = 20\nkislorod = 25\n"
                        u'print(f\"O2 в баллоне: {kislorod}\")',
                "expect_print": [u"O2 в баллоне: 25"],
                "assert_vars": {"kislorod": 25},
                "forbidden": ["input("],
            },
            {
                "prompt": u"Живой ввод: считай имя с пульта командой "
                          u"imya = read(\"Имя колониста: \") и выведи "
                          u"f-строкой «Колонист <имя> внесён в реестр».",
                "starter": u"imya = read(\"Имя колониста: \")\n",
                "hint": u"В окошке пульта впиши любое имя. Вывод: "
                        u'print(f\"Колонист {imya} внесён в реестр\")',
                "inputs": [u"Нейла"],
                "expect_print": [u"Колонист Нейла внесён в реестр"],
                "assert_vars": {"imya": u"Нейла"},
                "forbidden": ["input("],
            },
        ]

        # ------------------------------------------ этап 4: босс
        self.boss = {
            "title": u"Калибровка скафандра «Странник-7»",
            "mode": "console",
            "desc": u"БОСС: бортовой ИИ не примет незакалиброванный скафандр! "
                    u"Считай позывной с пульта read(), заполни ячейки "
                    u"kislorod = 21 и temperature = 36.6 и собери вывод "
                    u"f-строками: «Калибровка: <позывной>», «O2: 21%», "
                    u"«T: 36.6°C». Три строки — строго в этом порядке.\n\n"
                    u"Заготовка кода уже в редакторе — дополни её!",
            "starter": u"pozyvnoy = read(\"Позывной колониcта: \")\n"
                       u"kislorod = 21\n"
                       u"temperature = 36.6\n\n"
                       u'# ниже — три print(f"...") по образцу брифинга\n',
            "inputs": [u"Вега"],
            "expect_print": [u"Калибровка: Вега", u"O2: 21%", u"T: 36.6°C"],
            "prints_in_order": True,
            "assert_vars": {"kislorod": 21, "temperature": 36.6,
                            "pozyvnoy": u"Вега"},
            "forbidden": ["input("],
        }

        # ------------------------------------------- этап 5: тест
        self.quiz = [
            {
                "q": u"Что такое переменная в Python?",
                "options": [u"именованная ячейка памяти для хранения значения",
                            u"номер строки в программе",
                            u"команда вывода на экран",
                            u"название файла игры"],
                "answer": 0,
            },
            {
                "q": u"Что делает запись x = 10?",
                "options": [u"кладёт значение 10 в ячейку x",
                            u"сравнивает x с 10",
                            u"печатает 10",
                            u"удаляет x из памяти"],
                "answer": 0,
            },
            {
                "q": u"Для чего в этой игре нужна функция read()?",
                "options": [u"для ВВОДА: получает строку, которую набрал "
                            u"пользователь в окне пульта",
                            u"для удаления переменной",
                            u"для запуска циклов",
                            u"для сохранения файла"],
                "answer": 0,
            },
            {
                "q": u"Что выведет код: imya = \"Аня\"; print(f\"Привет, "
                     u"{imya}!\")?",
                "options": [u"Привет, Аня!", u"Привет, {imya}!",
                            u"Привет, imya!", u"Ошибку"],
                "answer": 0,
            },
            {
                "q": u"Какой правильный порядок этапов потока данных?",
                "options": [u"Вход -> Память -> Выход",
                            u"Выход -> Память -> Вход",
                            u"Память -> Вход -> Выход",
                            u"Вход -> Выход -> Память"],
                "answer": 0,
            },
        ]

    # ----------------------------------------------------- этап 2: симулятор
    def get_simulator_spec(self):
        """Живые ячейки памяти: присваивания и read() из кода ученика."""
        code = getattr(self, "_student_code", "") or ""
        cells, flow = self._scan(code)
        if not cells:
            cells = {u"imya": u"<пусто>", u"otryad": u"Альфа"}
            flow = [u"ВХОД: добавь read()", u"ПАМЯТЬ: создай переменную =",
                    u"ВЫХОД: print(f'...')"]
        return {
            "mode": "memory",
            "variables": cells,
            "lists": flow,
            "title": u"Память программы: ВХОД -> ПАМЯТЬ -> ВЫХОД",
        }

    def set_student_code(self, code):
        """GUI сообщает уровню текущий код редактора для симулятора ячеек."""
        self._student_code = code or ""

    @classmethod
    def _scan(cls, code):
        cells, flow = {}, []
        for raw in code.splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            try:
                tree = ast.parse(line)
            except SyntaxError:
                continue
            stmt = tree.body[0] if tree.body else None
            if isinstance(stmt, ast.Assign) and stmt.targets:
                t = stmt.targets[0]
                if isinstance(t, ast.Name):
                    cells[t.id] = cls._value_text(stmt.value)
                    flow.append(u"• память: %s = %s" % (t.id, cells[t.id]))
            elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call) \
                    and isinstance(stmt.value.func, ast.Name) \
                    and stmt.value.func.id == "print":
                flow.append(u"▶ выход: print(...)")
            elif "read" in line:
                flow.append(u"▶ вход: read()")
        return cells, flow[:9]

    @staticmethod
    def _value_text(node):
        try:
            value = ast.literal_eval(node)
            return repr(value)[:20]
        except Exception:
            if isinstance(node, ast.Call):
                f = node.func
                name = getattr(f, "id", "") or getattr(f, "attr", "")
                return u"%s(...) — данные с пульта" % name
            return "…"

    # ---------------------------------------------------- этап 3: автопроверка
    def check_task(self, sandbox, source, index):
        task = self.get_task(index)
        if not task:
            return False, u"Задача не задана."
        ok, feedback = BaseLevel.check_task(task, sandbox, source)
        if ok:
            feedback = u"✅ Карточка колониста принята реестром! " + feedback
        elif not task.get("inputs") and \
                (u"read()" in str(task.get("prompt", ""))
                 or u"read(" in (source or "")):
            feedback += (u"\n💡 В этой задаче данные вводит сам инженер: "
                         u"нажми «Запустить», набери имя в окне пульта и "
                         u"только потом «Проверить задачу».")
        return ok, feedback

    # --------------------------------------------------------- этап 4: босс
    def check_console_boss(self, sandbox, source):
        ok, feedback = BaseLevel.check_console_boss(self, sandbox, source)
        if ok:
            feedback = (u"🏆 БОСС ПОВЕРЖЕН: скафандр «Странник-7» "
                        u"откалиброван, допуск к поверхности получен!")
        return ok, feedback
