# -*- coding: utf-8 -*-
"""Урок 1 — «Посадка Ковчега» (Модуль 1, КТП: Исполнитель и алгоритм).

Хронометраж 45 минут:
  * stage_1_theory  (7 мин)  — брифинг + блок-схема: что такое алгоритм,
    Исполнитель, порядок команд сверху вниз, print(), комментарий #;
  * stage_2_simulator (8 мин) — интерактивная лента конвейера команд: код
    ученика раскладывается по блокам (исполняемые / отключённые #);
  * stage_3_practice (15 мин) — 3 задачи с автопроверкой вывода print();
  * stage_4_boss   (10 мин) — аварийные сбои гасятся комментариями #;
  * stage_5_quiz    (5 мин) — 5 вопросов, оценка 2–5, чекпоинт в профиле.
"""

import ast

from levels.base_level import BaseLevel


def _node(nid, kind, text):
    return {"id": nid, "kind": kind, "text": text}


class Level01(BaseLevel):
    """Первый контакт: посадка спасательного Ковчега на Нова-Терру."""

    LEVEL_NUMBER = 1

    def __init__(self):
        BaseLevel.__init__(self, {
            "number": 1,
            "title": u"Посадка Ковчега",
            "theme": u"Исполнитель и алгоритм. Порядок команд сверху вниз. "
                     u"Команда print(). Отключение команд комментарием #",
            "goal": u"Запустить компьютер посадки: вывести первые команды "
                    u"Исполнителю и отключить аварийные сбои комментариями",
            "xp_reward": 60,
        })
        self.stage_minutes = (7, 8, 15, 10, 5)

        # ------------------------------- этап 1: теория + блок-схема
        self.theory = (
            u"🛬 КАПСУЛА «КОВЧЕГ» ВХОДИТ В АТМОСФЕРУ НОВА-ТЕРРЫ!\n\n"
            u"Компьютер капсулы — верный, но очень буквальный ИСПОЛНИТЕЛЬ. "
            u"Он не додумывает: он выполняет команды СТРОГО СВЕРХУ ВНИЗ, одну "
            u"за другой. Точная последовательность команд, ведущая к цели, "
            u"называется АЛГОРИТМОМ.\n\n"
            u"Язык общения с Исполнителем — Python. Его базовая команда — "
            u"print(): она выводит текст или число в терминал базы:\n"
            u"    print(\"Нова-Терра, приём!\")\n"
            u"Текст всегда берётся в кавычки, числа — нет.\n\n"
            u"Если команда вызывает аварийный сбой, её нужно ОТКЛЮЧИТЬ: "
            u"поставь в начало строки решётку # — Исполнитель превратит строку "
            u"в КОММЕНТАРИЙ и пропустит её:\n"
            u"    print(\"Питание включено\")\n"
            u"    # print(\"АВАРИЙНЫЙ СБОЙ\")   <- эта команда молчит\n\n"
            u"Проверь себя: программа из трёх строк, где средняя закомментирована, "
            u"выведет ровно две строки — верхнюю и нижнюю.")
        self.flowchart = {
            "nodes": [
                _node("start", "start", u"Старт: вход в атмосферу"),
                _node("power", "process", u"Включить питание"),
                _node("cmd1", "io", u"print('Гасители: ОГОНЬ')"),
                _node("cmd2", "process", u"# print('СБОЙ') — молчит"),
                _node("land", "io", u"print('Мягкая посадка!')"),
                _node("end", "end", u"Конец: база №0 открыта"),
            ],
            "edges": [("start", "power"), ("power", "cmd1"), ("cmd1", "cmd2"),
                      ("cmd2", "land"), ("land", "end")],
        }

        # --------------------------------------- этап 2: симулятор
        self.simulator = {
            "mode": "memory",
            "variables": {u"Исполнитель": u"Python",
                          u"принцип": u"сверху вниз"},
            "lists": [u"▶ print(Гасители)", u"✖ # print(СБОЙ)",
                      u"▶ print(Посадка)"],
            "title": u"Конвейер команд Исполнителя",
        }

        # ---------------------------------------- этап 3: практика
        self.tasks = [
            {
                "prompt": u"Отправь Исполнителю первую команду: выведи фразу "
                          u"«Нова-Терра, приём!»",
                "starter": u"# Шаг 1: напиши команду print() ниже этой строки\n",
                "hint": u"Текст берётся в кавычки: print(\"Нова-Терра, приём!\")",
                "expect_print": [u"Нова-Терра, приём!"],
            },
            {
                "prompt": u"Алгоритм из двух шагов: выведи сначала «Проверка "
                          u"двигателей», затем «Двигатели в норме» — двумя "
                          u"print() в правильном порядке.",
                "starter": u"",
                "hint": u"Каждая команда — новая строка. Исполнитель читает "
                        u"сверху вниз: первым пиши print(\"Проверка двигателей\").",
                "expect_print": [u"Проверка двигателей", u"Двигатели в норме"],
                "prints_in_order": True,
            },
            {
                "prompt": u"Вторая команда стартера вызывает аварийный сбой. "
                          u"ОТКЛЮЧИ её комментарием # (не удаляй!), чтобы "
                          u"печаталась только первая строка.",
                "starter": u"print(\"Система цела\")\nprint(\"АВАРИЙНЫЙ СБОЙ\")\n",
                "hint": u"Поставь # в самое начало второй строки: "
                        u"#print(\"АВАРИЙНЫЙ СБОЙ\")",
                "expect_print": [u"Система цела"],
                "forbidden_print": [u"СБОЙ"],
                "require_comment": True,
                "comment_keywords": [u"сбой"],
            },
        ]

        # ------------------------------------------ этап 4: босс
        self.boss = {
            "title": u"Аварийные сбои гасителя тяги",
            "mode": "console",
            "desc": u"БОСС: система стартовала в режиме паники! Отключи "
                    u"комментариями # все три сбоя (строки со словом «СБОЙ» "
                    u"обязаны остаться в коде!), оставь рабочие команды и "
                    u"выведи последним «ПОСАДКА ЗАВЕРШЕНА». Слово «СБОЙ» в "
                    u"выводе быть не должно.",
            "starter": u"print(\"Гасители тяги: активны\")\n"
                       u"print(\"СБОЙ 1: перегрев\")\n"
                       u"print(\"СБОЙ 2: разгерметизация\")\n"
                       u"print(\"СБОЙ 3: навигация\")\n"
                       u"print(\"ПОСАДКА ЗАВЕРШЕНА\")\n",
            "expect_print": [u"Гасители тяги: активны", u"ПОСАДКА ЗАВЕРШЕНА"],
            "forbidden_print": [u"СБОЙ"],
            "require_comment": True,
            "comment_keywords": [u"сбой"],
        }

        # ------------------------------------------- этап 5: тест
        self.quiz = [
            {
                "q": u"Что такое алгоритм?",
                "options": [u"точная последовательность команд, ведущая к цели",
                            u"случайный набор действий",
                            u"название языка программирования",
                            u"ошибка в программе"],
                "answer": 0,
            },
            {
                "q": u"Как Исполнитель Python выполняет строки программы?",
                "options": [u"строго сверху вниз, одну за другой",
                            u"в случайном порядке",
                            u"снизу вверх",
                            u"все строки одновременно"],
                "answer": 0,
            },
            {
                "q": u"Что делает команда print(\"База\")?",
                "options": [u"выводит на экран слово База",
                            u"сохраняет файл",
                            u"стирает данные",
                            u"рисует картинку"],
                "answer": 0,
            },
            {
                "q": u"Зачем нужен символ # в начале строки?",
                "options": [u"превращает строку в комментарий — Исполнитель её "
                            u"пропускает",
                            u"умножает число на 2",
                            u"обозначает ошибку в коде",
                            u"ускоряет программу"],
                "answer": 0,
            },
            {
                "q": u"Программа: print(\"А\"), затем #print(\"Б\"), затем "
                     u"print(\"В\"). Что выведется?",
                "options": [u"А и В", u"А, Б и В", u"только Б", u"ничего"],
                "answer": 0,
            },
        ]

    # ----------------------------------------------------- этап 2: симулятор
    def get_simulator_spec(self):
        """Живая лента конвейера: каждый код ученика раскладывается на блоки."""
        code = getattr(self, "_student_code", "") or ""
        blocks, comments = self._split_lines(code)
        if not blocks and not comments:
            blocks = [("other", u"— редактор пуст: напиши print() —")]
        tape = [(u"▶ " + t if k == "print" else u"• " + t) for k, t in blocks]
        tape += [(u"✖ %s (отключена)" % t) for t in comments]
        return {
            "mode": "memory",
            "variables": {u"Исполнитель": u"Python",
                          u"шагов в ленте": len(tape),
                          u"отключено #": len(comments)},
            "lists": tape,
            "title": u"Конвейер команд Исполнителя (сверху вниз)",
        }

    def set_student_code(self, code):
        """GUI сообщает уровню текущий код редактора для живой ленты."""
        self._student_code = code or ""

    @staticmethod
    def _split_lines(code):
        """Разобрать код на исполняемые блоки и комментарии."""
        blocks, comments = [], []
        for raw in code.splitlines():
            line = raw.strip()
            if not line:
                continue
            if line.startswith("#"):
                comments.append(line[:24])
                continue
            try:
                tree = ast.parse(line)
            except SyntaxError:
                blocks.append(("other", line[:24]))
                continue
            stmt = tree.body[0] if tree.body else None
            if (isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call)
                    and isinstance(stmt.value.func, ast.Name)
                    and stmt.value.func.id == "print"):
                args = ", ".join(Level01._arg_text(a) for a in stmt.value.args)
                blocks.append(("print", ("print(%s)" % args)[:24]))
            else:
                blocks.append(("other", line[:24]))
        return blocks, comments

    @staticmethod
    def _arg_text(node):
        try:
            return repr(ast.literal_eval(node))
        except Exception:
            return "…"

    # ---------------------------------------------------- этап 3: автопроверка
    def check_task(self, sandbox, source, index):
        task = self.get_task(index)
        if not task:
            return False, u"Задача не задана."
        ok, feedback = BaseLevel.check_task(task, sandbox, source)
        if ok:
            feedback = u"✅ Алгоритм принят Исполнителем! " + feedback
        return ok, feedback

    # --------------------------------------------------------- этап 4: босс
    def check_console_boss(self, sandbox, source):
        ok, feedback = BaseLevel.check_console_boss(self, sandbox, source)
        if ok:
            feedback = (u"🏆 БОСС ПОВЕРЖЕН: гасители в норме, Ковчег "
                        u"приземлился! Все сбои отключены комментариями #.")
        return ok, feedback
