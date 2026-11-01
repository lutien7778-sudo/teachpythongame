# -*- coding: utf-8 -*-
"""Урок 15 — «Инженерная библиотека» (Модуль 2, КТП: Функции).

Хронометраж 45 минут:
  * stage_1_theory    (7 мин) — принцип DRY, ключевые слова def и return,
    параметры и аргументы функции;
  * stage_2_simulator (8 мин) — инженерный калькулятор: вызовы func(...) из
    кода ученика разворачиваются в вычисления (SimCanvas, режим Б);
  * stage_3_practice  (15 мин) — 3 задачи: функция расхода воды, расчёт
    кислорода с return, запас хода планетохода;
  * stage_4_boss      (10 мин) — проект инструктажа экспедиции функциями;
  * stage_5_quiz      (5 мин) — 5 вопросов, оценка 2–5, чекпоинт в профиле.
"""

import ast

from levels.base_level import BaseLevel


def _node(nid, kind, text):
    return {"id": nid, "kind": kind, "text": text}


class Level15(BaseLevel):
    """Инженерная библиотека Нова-Терры: свои функции-помощники."""

    LEVEL_NUMBER = 15

    #: Эталонные вызовы для симулятора.
    SAMPLE_CALLS = [("rashod_vody", "(3)", 6), ("zapas_hoda", "(120, 40)", 3)]

    def __init__(self):
        BaseLevel.__init__(self, {
            "number": 15,
            "title": u"Инженерная библиотека",
            "theme": u"Декомпозиция: функции def/return, параметры и "
                     u"аргументы, принцип DRY",
            "goal": u"Собрать библиотеку инженерных расчётов: вода, кислород, "
                    u"запас хода планетохода",
            "xp_reward": 105,
        })
        self.stage_minutes = (7, 8, 15, 10, 5)

        # ------------------------------- этап 1: теория + блок-схема
        self.theory = (
            u"🧰 ОТКРЫВАЕМ ИНЖЕНЕРНУЮ БИБЛИОТЕКУ! Хватает копировать код.\n\n"
            u"ПРИНЦИП DRY (Don't Repeat Yourself): если расчёт нужен чаще "
            u"дважды — упакуй его в ФУНКЦИЮ и вызывай по имени.\n\n"
            u"   def rashod_vody(kolonisty):\n"
            u"       litry = kolonisty * 2\n"
            u"       return litry\n\n"
            u"def — создаёт функцию; kolonisty — ПАРАМЕТР (местная переменная "
            u"функции); скобки при вызове rashod_vody(12) содержат АРГУМЕНТ — "
            u"реальное число, которое передаётся параметру.\n\n"
            u"return — возвращает результат наружу и ОСТАНАВЛИВАЕТ функцию. "
            u"Без return функция вернёт None. Результат можно сразу печатать "
            u"или сохранять в переменную:\n\n"
            u"   itog = rashod_vody(12)\n"
            u"   print(itog)          # 24\n\n"
            u"Функция может принимать несколько параметров: def zapas_hoda("
            u"zaryad, skorost) — и даже считать внутри: return zaryad // "
            u"skorost. Один раз написал — используешь весь урок!")
        self.flowchart = {
            "nodes": [
                _node("start", "start", u"Вызов: rashod_vody(12)"),
                _node("p", "process", u"parametr kolonisty = 12"),
                _node("c", "process", u"litry = kolonisty * 2"),
                _node("r", "io", u"return litry"),
                _node("v", "condition", u"Есть return?"),
                _node("n", "process", u"rezultat = None"),
                _node("e", "end", u"Конец: значение ушло вызывающему коду"),
            ],
            "edges": [("start", "p"), ("p", "c"), ("c", "r"), ("r", "v"),
                      ("v", "e"), ("v", "n"), ("n", "e")],
        }

        # --------------------------------------- этап 2: симулятор
        self.simulator = {
            "mode": "memory",
            "variables": {u"def rashod_vody": u"(kolonisty)",
                          u"вызов": u"rashod_vody(12)",
                          u"return": u"int: 24"},
            "lists": [u"kolonisty = 12", u"litry = 12 * 2",
                      u"return -> 24"],
            "title": u"Конвейер функции",
        }

        # ---------------------------------------- этап 3: практика
        self.tasks = [
            {
                "prompt": u"Расход воды: напиши функцию rashod_vody(kolonisty), "
                          u"которая возвращает kolonisty * 2 литров в сутки. "
                          u"Вызови её для 10 колонистов и напечатай результат. "
                          u"Ожидаемый вывод: 20.",
                "starter": u"",
                "hint": u"def rashod_vody(kolonisty):\n"
                        u"    return kolonisty * 2\n"
                        u"print(rashod_vody(10))",
                "expect_print": [u"20"],
                "expect_print_count": 1,
                "forbidden": [u"while"],
            },
            {
                "prompt": u"Кислород: функция kislorod(chelovek, chasy) "
                          u"возвращает chelovek * chasy (литры O2). Посчитай "
                          u"для 4 человек на 3 часа, сохрани в переменnuyu "
                          u"itog и напечатай её. Ожидаемый вывод: 12.",
                "starter": u"",
                "hint": u"def kislorod(chelovek, chasy):\n"
                        u"    return chelovek * chasy\n"
                        u"itog = kislorod(4, 3)\nprint(itog)",
                "expect_print": [u"12"],
                "expect_print_count": 1,
                "assert_vars": {"itog": 12},
                "forbidden": [u"while"],
            },
            {
                "prompt": u"Запас хода: функция hody(zaryad, skorost) "
                          u"возвращает целочисленное деление zaryad // skorost "
                          u"(часов пути). Напечатай hody(120, 40) — ждём 3.",
                "starter": u"",
                "hint": u"def hody(zaryad, skorost):\n"
                        u"    return zaryad // skorost\n"
                        u"print(hody(120, 40))",
                "expect_print": [u"3"],
                "expect_print_count": 1,
                "forbidden": [u"while"],
            },
        ]

        # ------------------------------------------ этап 4: босс
        self.boss = {
            "title": u"Инструктаж экспедиции: главная сводка",
            "mode": "console",
            "desc": u"БОСС: штаб требует готовую библиотеку и сводку по ней. "
                    u"Напиши ДВЕ функции: voda(k) возвращает k * 2, "
                    u"kislodorod(k, ch) возвращает k * ch. Затем выведи ровно "
                    u"4 строки в порядке:\n"
                    u"1) voda(25)  — ответ 50;\n"
                    u"2) kislodorod(6, 8) — ответ 48;\n"
                    u"3) сумма двух вызовов — ответ 98;\n"
                    u"4) текст ИНСТРУКТАЖ ГОТОВ. Без дублирования кода — "
                    u"только вызовы функций!",
            "starter": u"",
            "expect_print": [u"50", u"48", u"98", u"ИНСТРУКТАЖ ГОТОВ"],
            "expect_print_count": 4,
            "prints_in_order": True,
            "assert_vars": {},
            "forbidden": [u"while", u"lambda"],
        }

        # ------------------------------------------- этап 5: тест
        self.quiz = [
            {
                "q": u"Каким словом создаётся функция?",
                "options": [u"def", u"func", u"return", u"call"],
                "answer": 0,
            },
            {
                "q": u"Что делает return?",
                "options": [u"возвращает результат и завершает функцию",
                            u"печатает текст",
                            u"повторяет цикл",
                            u"удаляет функцию"],
                "answer": 0,
            },
            {
                "q": u"Чем отличается параметр от аргумента?",
                "options": [u"параметр — переменная в def, аргумент — "
                            u"значение при вызове",
                            u"это одно и то же слово",
                            u"аргумент пишется в def",
                            u"параметр нельзя использовать"],
                "answer": 0,
            },
            {
                "q": u"Что вернёт функция без оператора return?",
                "options": [u"None", u"0", u"пустую строку", u"ошибку"],
                "answer": 0,
            },
            {
                "q": u"Зачем нужен принцип DRY?",
                "options": [u"чтобы не дублировать код — расчёт пишется один "
                            u"раз в функции",
                            u"чтобы программа работала медленнее",
                            u"чтобы скрывать код",
                            u"так требует КТП"],
                "answer": 0,
            },
        ]

    # ----------------------------------------------------- этап 2: симулятор
    def get_simulator_spec(self):
        """Живой конвейер: определения и вызовы функций из кода ученика."""
        code = getattr(self, "_student_code", "") or ""
        defs, calls = self._scan_funcs(code)
        cells = {}
        rows = []
        for name in defs[:4]:
            cells[u"def " + name] = u"функция готова"
            rows.append(u"def %s(...) — записана в библиотеку" % name)
        for call in calls[:4]:
            cells[call] = u"ожидает return"
            rows.append(u"вызов %s()" % call)
        if not rows:
            for name, args, res in self.SAMPLE_CALLS:
                cells[u"%s%s" % (name, args)] = u"return int: %d" % res
                rows.append(u"%s%s -> %d" % (name, args, res))
        return {
            "mode": "memory",
            "variables": cells,
            "lists": rows,
            "title": u"Конвейер функций (%d)" % len(defs),
        }

    def set_student_code(self, code):
        """GUI сообщает уровню текущий код редактора для живого конвейера."""
        self._student_code = code or ""

    @staticmethod
    def _scan_funcs(code):
        """Имена def и тексты вызовов из кода ученика (для режима Б)."""
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return [], []
        defs, calls = [], []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                defs.append(node.name)
            elif isinstance(node, ast.Call) and isinstance(node.func,
                                                            ast.Name):
                try:
                    aargs = ", ".join(repr(ast.literal_eval(a))
                                      for a in node.args)
                except Exception:
                    aargs = "..."
                calls.append("%s(%s)" % (node.func.id, aargs))
        return defs, calls

    # ---------------------------------------------------- этап 3: автопроверка
    def check_task(self, sandbox, source, index):
        task = self.get_task(index)
        if not task:
            return False, u"Задача не задана."
        ok, feedback = BaseLevel.check_task(task, sandbox, source)
        if ok:
            feedback = u"✅ Библиотека пополнена! " + feedback
        else:
            feedback += (u"\n💡 Проверь: сначала def с return, потом вызов "
                         u"func(число) снаружи функции.")
        return ok, feedback

    # --------------------------------------------------------- этап 4: босс
    def check_console_boss(self, sandbox, source):
        ok, feedback = BaseLevel.check_console_boss(self, sandbox, source)
        if ok:
            feedback = (u"🏆 БОСС ПОВЕРЖЕН: экспедиция обеспечена "
                        u"библиотекой расчётов! " + feedback)
        return ok, feedback
