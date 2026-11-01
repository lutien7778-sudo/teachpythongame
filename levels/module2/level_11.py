# -*- coding: utf-8 -*-
"""Урок 11 — «Конвейер руды» (Модуль 2, КТП: Динамические списки и очереди).

Хронометраж 45 минут:
  * stage_1_theory    (7 мин) — методы списка .append(), .pop(), .remove(),
    оператор in, очередь как конвейер;
  * stage_2_simulator (8 мин) — живой конвейер: содержимое бункера из кода
    ученика рисуется цепочкой ячеек (SimCanvas, режим Б);
  * stage_3_practice  (15 мин) — 3 задачи: разгрузка вагонетки (.append),
    проверка наличия детали (in), лимит вместимости бункера;
  * stage_4_boss      (10 мин) — плавильный бункер: собрать партию без
    переполнения и выдать шихту через .pop();
  * stage_5_quiz      (5 мин) — 5 вопросов, оценка 2–5, чекпоинт в профиле.
"""

import ast

from levels.base_level import BaseLevel


def _node(nid, kind, text):
    return {"id": nid, "kind": kind, "text": text}


class Level11(BaseLevel):
    """Конвейер Нова-Терры: динамические списки и очередь."""

    LEVEL_NUMBER = 11

    def __init__(self):
        BaseLevel.__init__(self, {
            "number": 11,
            "title": u"Конвейер руды",
            "theme": u"Динамические списки: методы append(), pop(), remove(), "
                     u"оператор in, очередь с ограничением вместимости",
            "goal": u"Наладить загрузку плавильного бункера: принимать руду, "
                    u"проверять состав и не допускать переполнения",
            "xp_reward": 90,
        })
        self.stage_minutes = (7, 8, 15, 10, 5)

        # ------------------------------- этап 1: теория + блок-схема
        self.theory = (
            u"⛏️ РУДОКОП НАПОЛНИЛ ВАГОНЕТКИ! КОНВЕЙЕР ЖДЁТ КОДА.\n\n"
            u"Список можно менять прямо во время работы программы — для "
            u"этого у него есть МЕТОДЫ (команды-действия):\n\n"
            u"   ochered.append(\"руда\")  — добавить элемент в КОНЕЦ;\n"
            u"   posledniy = ochered.pop() — снять ПОСЛЕДНИЙ элемент "
            u"(он же возвращается);\n"
            u"   ochered.remove(\"песок\") — удалить первое совпадение "
            u"(если элемента нет — ValueError!);\n"
            u"   len(ochered)              — текущая длина очереди.\n\n"
            u"ОПЕРАТОР in отвечает «есть ли предмет в списке» и возвращает "
            u"True/False:\n"
            u"   if \"уран\" in ochered:  -> опасная загрузка!\n\n"
            u"ОЧЕРЕДЬ (queue) — список, где новые грузы встают в хвост "
            u"(append), а в плавку уходят с конца (pop). Вместимость бункера "
            u"ограничена, поэтому перед append всегда проверяем len():\n\n"
            u"   if len(bunker) < 6:\n"
            u"       bunker.append(ruda)\n"
            u"   else:\n"
            u'       print("Бункер полон!")\n\n'
            u"Так конвейер не заклинивает.")
        self.flowchart = {
            "nodes": [
                _node("start", "start", u"Старт: пришла вагонетка"),
                _node("r", "io", u"ruda = read()"),
                _node("c", "condition", u"len(bunker) < 6?"),
                _node("a", "process", u"bunker.append(ruda)"),
                _node("f", "process", u"print('Бункер полон!')"),
                _node("e", "end", u"Конец: смена закрыта"),
            ],
            "edges": [("start", "r"), ("r", "c"), ("c", "a"),
                      ("c", "f"), ("a", "e"), ("f", "e")],
        }

        # --------------------------------------- этап 2: симулятор
        self.simulator = {
            "mode": "memory",
            "variables": {u"bunker": u"list: 3", u"limit": u"int: 6"},
            "lists": [u"[0] железо", u"[1] медь", u"[2] никель"],
            "title": u"Конвейер: лента и бункер",
        }

        # ---------------------------------------- этап 3: практика
        self.tasks = [
            {
                "prompt": u"Разгрузка вагонетки: создай пустой список "
                          u"bunker = [] и методом .append() добавь в него по "
                          u"порядку три груза: \"железо\", \"медь\", "
                          u"\"никель\". Затем напечатай сам список.",
                "starter": u"# плавильный бункер пуст\nbunker = []\n",
                "hint": u'bunker.append("железо")\n'
                        u'bunker.append("медь")\n'
                        u'bunker.append("никель")\n'
                        u"print(bunker)",
                "expect_print": [u"['железо', 'медь', 'никель']"],
                "assert_vars": {"bunker": [u"железо", u"медь", u"никель"]},
                "forbidden": [u"bunker = [\""],
            },
            {
                "prompt": u"Проверка состава: в списке ruda стоят "
                          u"[\"железо\", \"уран\", \"медь\"]. Оператором in "
                          u"и условием if проверь, есть ли в партии уран, и "
                          u"если да — выведи «Радиация! Карантин». Если бы "
                          u"урана не было, вывод должен был быть «Партия "
                          u"чистая» (используй else).",
                "starter": u'ruda = ["железо", "уран", "медь"]\n',
                "hint": u'if "уран" in ruda:\n'
                        u'    print("Радиация! Карантин")\n'
                        u"else:\n"
                        u'    print("Партия чистая")',
                "expect_print": [u"Радиация! Карантин"],
                "expect_print_count": 1,
                "forbidden_print": [u"Партия чистая"],
            },
            {
                "prompt": u"Лимит вместимости: бункер вмещает не больше 3 "
                          u"контейнеров, список bunker уже содержит два. "
                          u"Создай список novye = [\"олово\", \"ртуть\", "
                          u"\"свинец\"] и в цикле for добавляй грузы через "
                          u".append() ТОЛЬКО пока len(bunker) < 3, иначе "
                          u"печатай «Отказ: бункер полон». В конце выведи "
                          u"длину списка.",
                "starter": u'bunker = ["железо", "медь"]\nnovye = ["олово",'
                           u' "ртуть", "свинец"]\n',
                "hint": u"for gruz in novye:\n"
                        u"    if len(bunker) < 3:\n"
                        u"        bunker.append(gruz)\n"
                        u"    else:\n"
                        u'        print("Отказ: бункер полон")\n'
                        u"print(len(bunker))",
                "expect_print": [u"Отказ: бункер полон", u"3"],
                "prints_in_order": True,
                "assert_vars": {"bunker": [u"железо", u"медь", u"олово"]},
            },
        ]

        # ------------------------------------------ этап 4: босс
        self.boss = {
            "title": u"Плавильный бункер «Циклоп»",
            "mode": "console",
            "desc": u"БОСС: смена на плавильне! Загрузи пустой список "
                    u"bunker четырьмя рудами через .append() (железо, медь, "
                    u"никель, кобальт), затем СНИМИ три последних контейнера "
                    u"методом .pop(), печатая каждый снятый груз строкой, и "
                    u"в конце удали оставшийся первый груз методом .remove(). "
                    u"Выведи ровно 4 строки: три снятых груза в порядке "
                    u"снятия (кобальт, никель, медь) и длину пустого бункера "
                    u"— 0. Удалишь лишним .pop() — IndexError остановит цех!",
            "starter": u"# смена на плавильне\nbunker = []\n",
            "expect_print": [u"кобальт", u"никель", u"медь", u"0"],
            "expect_print_count": 4,
            "prints_in_order": True,
            "assert_vars": {"bunker": []},
            "forbidden": [u"del ", u"clear()", u"bunker = [\""],
        }

        # ------------------------------------------- этап 5: тест
        self.quiz = [
            {
                "q": u"Что делает метод a.append(x)?",
                "options": [u"добавляет x в конец списка",
                            u"удаляет x из списка",
                            u"сортирует список",
                            u"добавляет x в начало"],
                "answer": 0,
            },
            {
                "q": u"Что возвращает вызов a.pop() без аргументов?",
                "options": [u"последний элемент, удалив его из списка",
                            u"первый элемент", u"длину списка", u"None"],
                "answer": 0,
            },
            {
                "q": u"Как проверить, что деталь есть в списке crates?",
                "options": [u"if \"деталь\" in crates:",
                            u"if crates.has(\"деталь\"):",
                            u"if crates.find(\"деталь\") == 0:",
                            u"if exists(\"деталь\", crates):"],
                "answer": 0,
            },
            {
                "q": u"Что случится при a.remove(\"нет такого\")?",
                "options": [u"ошибка ValueError", u"ничего",
                            u"список очистится", u"добавится элемент"],
                "answer": 0,
            },
            {
                "q": u"Перед append в ограниченном бункере проверяют:",
                "options": [u"len(bunker) < вместимость",
                            u"bunker != 0",
                            u"type(bunker) == list",
                            u"проверка не нужна"],
                "answer": 0,
            },
        ]

    # ----------------------------------------------------- этап 2: симулятор
    def get_simulator_spec(self):
        """Живая лента конвейера: список(и) из кода ученика."""
        code = getattr(self, "_student_code", "") or ""
        lists = self._scan_lists(code)
        vars_ = {}
        rows = []
        for name, items in lists:
            vars_[name] = u"list: %d" % len(items)
            for i, v in enumerate(items[:8]):
                rows.append(u"%s[%d] = %s" % (name, i, cut(v)))
        if not rows:
            vars_ = {u"bunker": u"list: ? (пустой?)", u"limit": u"int: 3"}
            rows = [u"append -> в хвост ленты", u"pop -> с конца в плавку",
                    u"in -> есть груз на ленте?"]
        return {
            "mode": "memory",
            "variables": vars_,
            "lists": rows[:8],
            "title": u"Конвейер: лента загрузки",
        }

    def set_student_code(self, code):
        """GUI сообщает уровню текущий код редактора для живой ленты."""
        self._student_code = code or ""

    @staticmethod
    def _scan_lists(code):
        """[(имя, [литеральные элементы...])] — все списки-литералы в коде."""
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return []
        out = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign) and isinstance(node.value,
                                                           ast.List):
                tgt = node.targets[0]
                if not isinstance(tgt, ast.Name):
                    continue
                items = []
                for elt in node.value.elts:
                    try:
                        items.append(repr(ast.literal_eval(elt)).strip("'\""))
                    except Exception:
                        items.append(u"…")
                out.append((tgt.id, items))
        return out[:4]

    # ---------------------------------------------------- этап 3: автопроверка
    def check_task(self, sandbox, source, index):
        task = self.get_task(index)
        if not task:
            return False, u"Задача не задана."
        ok, feedback = BaseLevel.check_task(task, sandbox, source)
        if ok:
            feedback = u"✅ Конвейер принял партию! " + feedback
        elif u"ValueError" in feedback or u"IndexError" in feedback:
            feedback += (u"\n💡 Совет: pop() нельзя звать на пустом списке, "
                         u"a remove(x) — если x отсутствует. Сначала "
                         u"проверяй оператором in.")
        return ok, feedback

    # --------------------------------------------------------- этап 4: босс
    def check_console_boss(self, sandbox, source):
        ok, feedback = BaseLevel.check_console_boss(self, sandbox, source)
        if ok:
            feedback = (u"🏆 БОСС ПОВЕРЖЕН: бункер «Циклоп» отработал смену "
                        u"— 4 загрузки, 3 выпуска в плавку, остаток удалён "
                        u"через remove()! " + feedback)
        return ok, feedback


def cut(text, limit=16):
    """Короткая подпись значения для ячеек канвы."""
    s = str(text)
    return s if len(s) <= limit else s[:limit - 1] + u"…"
