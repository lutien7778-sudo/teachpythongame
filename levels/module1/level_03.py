# -*- coding: utf-8 -*-
"""Урок 3 — «Энергосеть базы» (Модуль 1, КТП: Числа, вычисления и типы данных).

Хронометраж 45 минут:
  * stage_1_theory    (7 мин) — int/float/str, функции приведения int(), float(),
    арифметика +, -, *, целочисленное деление // и остаток %;
  * stage_2_simulator (8 мин) — живой расчёт энергосети: код ученика
    превращается в ячейки памяти с типами (SimCanvas, режим Б);
  * stage_3_practice  (15 мин) — 3 задачи: мощность генераторов, деление //
    между колониями, резерв % ;
  * stage_4_boss      (10 мин) — пуск реактора: точный расчёт по формуле;
  * stage_5_quiz      (5 мин) — 5 вопросов, оценка 2–5, чекпоинт в профиле.
"""

import ast

from levels.base_level import BaseLevel


def _node(nid, kind, text):
    return {"id": nid, "kind": kind, "text": text}


class Level03(BaseLevel):
    """Энергостанция Нова-Терры: числа, типы, // и %."""

    LEVEL_NUMBER = 3

    def __init__(self):
        BaseLevel.__init__(self, {
            "number": 3,
            "title": u"Энергосеть базы",
            "theme": u"Числа, вычисления и типы данных. int, float, str, "
                     u"приведение типов, операторы + - * // %",
            "goal": u"Рассчитать мощность генераторов, раздать энергию "
                    u"колонию через // и собрать аварийный резерв через %",
            "xp_reward": 80,
        })
        self.stage_minutes = (7, 8, 15, 10, 5)

        # ------------------------------- этап 1: теория + блок-схема
        self.theory = (
            u"⚡ ЭНЕРГОБЛОК БАЗЫ ТРЕБУЕТ РАСЧЁТА!\n\n"
            u"Python хранит числа в двух основных типах:\n"
            u"   int   — целые: 12, 0, -5 (генераторы, баллоны, секции);\n"
            u"   float — дробные: 3.6, 12.0 (напряжение, температура).\n"
            u"Строка \"12\" — это ТЕКСТ, а не число: \"12\" + 3 выдаст ошибку "
            u"типа (TypeError).\n\n"
            u"ПРИВЕДЕНИЕ ТИПОВ возвращает тексту числовой смысл:\n"
            u"   int(\"12\") -> 12        float(\"2.5\") -> 2.5\n"
            u"   str(12)     -> \"12\"    round(2.7) -> 3\n\n"
            u"АРИФМЕТИКА ИСПОЛНИТЕЛЯ:\n"
            u"   7 + 3 -> 10   7 - 3 -> 4   7 * 3 -> 21\n"
            u"   7 / 3  -> 2.333...  обычное деление ВСЕГДА даёт float;\n"
            u"   7 // 3 -> 2         ЦЕЛОЧИСЛЕННОЕ деление: сколько РОВНЫХ "
            u"пачек достанется каждой колонии;\n"
            u"   7 % 3  -> 1         ОСТАТОК от деления: что падает в "
            u"аварийный резерв.\n\n"
            u"Пример энергосети: 100 кВт на 3 генератора:\n"
            u"   100 // 3 = 33 кВт каждому,  100 % 3 = 1 кВт — в резерв.")
        self.flowchart = {
            "nodes": [
                _node("start", "start", u"Старт: снять показания"),
                _node("a", "process", u"generatorov = 3"),
                _node("b", "process", u"moschnost = 100 * generatorov"),
                _node("c", "process", u"na_koloniyu = moschnost // 3"),
                _node("d", "process", u"rezerv = moschnost % 3"),
                _node("out", "io", u"print(na_koloniyu, rezerv)"),
                _node("end", "end", u"Конец: сеть стабильна"),
            ],
            "edges": [("start", "a"), ("a", "b"), ("b", "c"), ("c", "d"),
                      ("d", "out"), ("out", "end")],
        }

        # --------------------------------------- этап 2: симулятор
        self.simulator = {
            "mode": "memory",
            "variables": {u"generatorov": u"int = 3",
                          u"moschnost": u"int = 300",
                          u"na_koloniyu": u"int = 100",
                          u"rezerv": u"int = 0"},
            "lists": [u"100 кВт : 3 = 33.33 кВт (/)",
                      u"100 // 3 = 33 кВт ровными пачками",
                      u"100 % 3 = 1 кВт в аварийный резерв"],
            "title": u"Щиток энергосети: ячейки и типы",
        }

        # ---------------------------------------- этап 3: практика
        self.tasks = [
            {
                "prompt": u"Мощность блока: в генераторе 12 ячеек по 8 кВт. "
                          u"Создай переменnye generator = 12 и moshchnost_odnoy = 8, "
                          u"посчитай total = generator * moshchnost_odnoy и "
                          u"выведи его print().",
                "starter": u"generator = 12\nmoshchnost_odnoy = 8\n",
                "hint": u"total = generator * moshchnost_odnoy\nprint(total)",
                "expect_print": [u"96"],
                "assert_vars": {"total": 96},
                "expect_types": {"total": "int"},
            },
            {
                "prompt": u"Раздача энергии: 100 кВт ровно делим между 3 "
                          u"колониями оператором // (целое число кВт каждой), "
                          u"а остаток собираем в резерв оператором %. Выведи "
                          u"f-строками «На колонию: 33» и «Резерв: 1».",
                "starter": u"energiya = 100\nkolonii = 3\n",
                "hint": u"na_koloniyu = energiya // kolonii\n"
                        u"rezerv = energiya % kolonii\n"
                        u'print(f"На колонию: {na_koloniyu}")\n'
                        u'print(f"Резерв: {rezerv}")',
                "assert_vars": {"na_koloniyu": 33, "rezerv": 1},
                "expect_print": [u"На колонию: 33", u"Резерв: 1"],
                "prints_in_order": True,
            },
            {
                "prompt": u"Приведение типов: датчик прислал строку "
                          u"napryazhenie = \"220.5\". Преврати её в float и "
                          u"прибавь 19.5 — получишь ровно 240.0. Выведи результат.",
                "starter": u"napryazhenie = \"220.5\"\n",
                "hint": u"itog = float(napryazhenie) + 19.5\nprint(itog)",
                "expect_print": [u"240.0"],
                "assert_vars": {"itog": 240.0},
                "expect_types": {"itog": "float"},
                "forbidden": ["240"],
            },
        ]

        # ------------------------------------------ этап 4: босс
        self.boss = {
            "title": u"Пуск термоядерного реактора «Гелиос»",
            "mode": "console",
            "desc": u"БОСС: реактор запускается только точным расчётом! "
                    u"Показания датчиков пришли СТРОКАМИ: toplivo = \"947\", "
                    u"sektorov = \"8\". Привеги их к int, посчитай po_sectoru "
                    u"(//) и v_rezerve (%), затем выведи ровно три строки:\n"
                    u"«РЕАКТОР ЗАПУЩЕН», «По секторам: 118», «Резерв: 3».\n"
                    u"Если перепутаешь // и % — реактор уйдёт в перегрев!",
            "starter": u"toplivo = \"947\"\nsektorov = \"8\"\n\n"
                       u"# 1) int(...)  2) //  3) %  4) print(f\"...\")\n",
            "expect_print": [u"РЕАКТОР ЗАПУЩЕН", u"По секторам: 118",
                             u"Резерв: 3"],
            "prints_in_order": True,
            "assert_vars": {"po_sectoru": 118, "v_rezerve": 3},
            "forbidden": ["input("],
        }

        # ------------------------------------------- этап 5: тест
        self.quiz = [
            {
                "q": u"Какой тип у значения 3.6?",
                "options": [u"float", u"int", u"str", u"bool"],
                "answer": 0,
            },
            {
                "q": u"Чему равно 7 // 2?",
                "options": [u"3", u"3.5", u"4", u"1"],
                "answer": 0,
            },
            {
                "q": u"Чему равно 7 % 2?",
                "options": [u"1", u"0", u"3.5", u"2"],
                "answer": 0,
            },
            {
                "q": u"Что сделает int(\"12\") + 3?",
                "options": [u"15 — строка превратится в число",
                            u"ошибку TypeError",
                            u"\"123\"",
                            u"12"],
                "answer": 0,
            },
            {
                "q": u"Почему \"5\" + 3 вызывает ошибку?",
                "options": [u"нельзя складывать строку (str) и число (int)",
                            u"5 слишком маленькое число",
                            u"Python умеет только сложение float",
                            u"нужны двойные скобки"],
                "answer": 0,
            },
        ]

    # ----------------------------------------------------- этап 2: симулятор
    def get_simulator_spec(self):
        """Живой щиток: переменные кода ученика + их фактические типы."""
        code = getattr(self, "_student_code", "") or ""
        cells = self._scan(code)
        if not cells:
            cells = {u"energiya": u"int: ?", u"kolonii": u"int: ?"}
        return {
            "mode": "memory",
            "variables": cells,
            "lists": [u"/  -> точное деление (float)",
                      u"// -> ровные пачки для колоний",
                      u"%  -> остаток в аварийный резерв"],
            "title": u"Щиток энергосети: память и типы",
        }

    def set_student_code(self, code):
        """GUI сообщает уровню текущий код редактора для живого щитка."""
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
        return cells

    # ---------------------------------------------------- этап 3: автопроверка
    def check_task(self, sandbox, source, index):
        task = self.get_task(index)
        if not task:
            return False, u"Задача не задана."
        ok, feedback = BaseLevel.check_task(task, sandbox, source)
        if ok:
            feedback = u"✅ Энергоблок стабилизирован! " + feedback
        elif u"TypeError" in feedback or u"типы" in feedback:
            feedback += u"\n💡 Совет: оберни строку датчика в int() или float()."
        return ok, feedback

    # --------------------------------------------------------- этап 4: босс
    def check_console_boss(self, sandbox, source):
        ok, feedback = BaseLevel.check_console_boss(self, sandbox, source)
        if ok:
            feedback = (u"🏆 БОСС ПОВЕРЖЕН: реактор «Гелиос» вышел наnominal "
                        u"118 кВт на сектор, резерв 3 кВт в банке!")
        return ok, feedback
