# -*- coding: utf-8 -*-
"""Урок 13 — «Главный архив колонии» (Модуль 2, КТП: Словари).

Хронометраж 45 минут:
  * stage_1_theory    (7 мин) — ассоциативный массив dict, пары «ключ-значение»,
    доступ по ключу, добавление и изменение полей;
  * stage_2_simulator (8 мин) — живой архив: словарь из кода ученика
    рисуется ячейками памяти (SimCanvas, режим Б);
  * stage_3_practice  (15 мин) — 3 задачи: база жилых отсеков, каталог флоры,
    добавление нового поля в карточку;
  * stage_4_boss      (10 мин) — полная инвентаризация архива колонии;
  * stage_5_quiz      (5 мин) — 5 вопросов, оценка 2–5, чекпоинт в профиле.
"""

import ast

from levels.base_level import BaseLevel


def _node(nid, kind, text):
    return {"id": nid, "kind": kind, "text": text}


class Level13(BaseLevel):
    """Главный архив Нова-Терры: словари и базы данных."""

    LEVEL_NUMBER = 13

    #: Эталонная карточка жилого отсека для симулятора.
    SAMPLE = {"otsek": "A-1", "person": 4, "kislodorod": True}

    def __init__(self):
        BaseLevel.__init__(self, {
            "number": 13,
            "title": u"Главный архив колонии",
            "theme": u"Словари dict: пары «ключ-значение», доступ по ключу, "
                     u"добавление и изменение полей",
            "goal": u"Завести электронную базу данных жилых отсеков и каталог "
                    u"местной флоры планеты",
            "xp_reward": 95,
        })
        self.stage_minutes = (7, 8, 15, 10, 5)

        # ------------------------------- этап 1: теория + блок-схема
        self.theory = (
            u"🗄 ГЛАВНЫЙ АРХИВ КОЛОНИИ ОТКРЫТ ДЛЯ ЗАПИСИ!\n\n"
            u"СПИСОК хранит данные по ПОРЯДКУ (индекс 0, 1, 2...). СЛОВАРЬ "
            u"хранит данные по ИМЕНИ — это пара «ключ: значение».\n\n"
            u'   otk = {"nomer": "A-1", "lyudi": 4}\n\n'
            u"ДОСТУП ПО КЛЮЧУ — квадратные скобки с именем ключа:\n\n"
            u'   print(otk["lyudi"])        # 4\n\n'
            u"ИЗМЕНЕНИЕ и ДОБАВЛЕНИЕ записей делаются одним и тем же "
            u"присваиванием. Если ключ уже есть — поле обновится; если ключа "
            u"нет — оно ДОБАВИТСЯ в словарь:\n\n"
            u'   otk["lyudi"] = 6           # изменили поле\n'
            u'   otk["germetik"] = True     # добавили новое поле\n\n'
            u"ОШИБКА KeyError — Python требует ключ, которого в архиве нет. "
            u"Проверить наличие ключа можно оператором in:\n\n"
            u'   if "voda" in otk:\n'
            u"       ...\n\n"
            u"Перебор всех записей: for klyuch in otk: печатает ключи, а "
            u"print(otk[klyuch]) — соответствующие значения.")
        self.flowchart = {
            "nodes": [
                _node("start", "start", u"Старт: открываем архив dict"),
                _node("w", "io", u"klyuch = запись карточки"),
                _node("c", "condition", u"Ключ уже есть?"),
                _node("u", "process", u"izmenit pole: d[k] = novoe"),
                _node("a", "process", u"dobavit klyuch: d[k] = znachenie"),
                _node("p", "io", u"print(d[klyuch])"),
                _node("e", "end", u"Конец: карточка сохранена"),
            ],
            "edges": [("start", "w"), ("w", "c"), ("c", "u"), ("c", "a"),
                      ("u", "p"), ("a", "p"), ("p", "e")],
        }

        # --------------------------------------- этап 2: симулятор
        self.simulator = {
            "mode": "memory",
            "variables": {u"otsek": u"dict: 3", u'"nomer"': u"str: A-1",
                          u'"lyudi"': u"int: 4", u'"germetik"': u"bool: True"},
            "lists": [u"ключ -> значение", u'"nomer" -> "A-1"',
                      u'"lyudi" -> 4', u'"germetik" -> True'],
            "title": u"Карточка жилого отсека",
        }

        # ---------------------------------------- этап 3: практика
        self.tasks = [
            {
                "prompt": u"База жилых отсеков: создай словарь otk = "
                          u"{\"nomer\": \"A-1\", \"lyudi\": 4} и напечатай "
                          u"значение поля lyudi одной строкой. Ожидаемый "
                          u"вывод: 4.",
                "starter": u"",
                "hint": u'otk = {"nomer": "A-1", "lyudi": 4}\n'
                        u'print(otk["lyudi"])',
                "expect_print": [u"4"],
                "expect_print_count": 1,
                "expect_vars": {"otk": {"nomer": "A-1", "lyudi": 4}},
                "forbidden": [u"[0]", u"[1]"],
            },
            {
                "prompt": u"Каталог флоры: в словаре flora = {\"sapun\": "
                          u"\"куст\", \"kras\": \"мох\"} добавь НОВЫЙ ключ "
                  u"\"svet\" со значением \"гриб\" (строкой через присваивание) "
                          u"и напечатай весь словарь. Ожидаемый вывод: "
                          u"{'sapun': 'куст', 'kras': 'мох', 'svet': 'гриб'}.",
                "starter": u'flora = {"sapun": "куст", "kras": "мох"}\n',
                "hint": u'flora["svet"] = "гриб"\nprint(flora)',
                "expect_print": [u"{'sapun': 'куст', 'kras': 'мох', "
                                 u"'svet': 'гриб'}"],
                "expect_print_count": 1,
                "expect_vars": {"flora": {"sapun": "куст", "kras": "мох",
                                          "svet": "гриб"}},
                "forbidden": [u"append"],
            },
            {
                "prompt": u"Изменение поля: в карточке otk = {\"nomer\": "
                          u"\"B-2\", \"lyudi\": 3} поселись ещё два "
                          u"колониста — запиши в поле lyudi значение 5 и "
                          u"напечатай его. Ожидаемый вывод: 5.",
                "starter": u'otk = {"nomer": "B-2", "lyudi": 3}\n',
                "hint": u'otk["lyudi"] = 5\nprint(otk["lyudi"])',
                "expect_print": [u"5"],
                "expect_print_count": 1,
                "assert_vars": {"otk": {"nomer": "B-2", "lyudi": 5}},
                "forbidden": [u"del "],
            },
        ]

        # ------------------------------------------ этап 4: босс
        self.boss = {
            "title": u"Полная инвентаризация главного архива",
            "mode": "console",
            "desc": u"БОСС: архив колонии обязан принять полный отчёт. Карточка "
                    u"baza = {\"sklad\": \"Omega\", \"modul\": 7}. Выполни "
                    u"ровно 4 действия и выведи ровно 4 строки в порядке:\n"
                    u"1) печать поля modul (ответ: 7);\n"
                    u"2) добавь ключ \"energiya\" со значением 100 и напечатай "
                    u"весь словарь (порядок ключей: sklad, modul, energiya);\n"
                    u"3) проверь оператором in: напечатай True (ключ \"sklad\" "
                    u"в архиве есть);\n"
                    u"4) напечатай АРХИВ ОБНОВЛЕН.",
            "starter": u'baza = {"sklad": "Omega", "modul": 7}\n',
            "expect_print": [u"7",
                             u"{'sklad': 'Omega', 'modul': 7, "
                             u"'energiya': 100}",
                             u"True", u"АРХИВ ОБНОВЛЕН"],
            "expect_print_count": 4,
            "prints_in_order": True,
            "assert_vars": {},
            "forbidden": [u"del ", u".pop(", u"list("],
        }

        # ------------------------------------------- этап 5: тест
        self.quiz = [
            {
                "q": u"Чем словарь отличается от списка?",
                "options": [u"данные хранятся парами «ключ: значение»",
                            u"в нём нельзя хранить числа",
                            u"он всегда короче",
                            u"ничем"],
                "answer": 0,
            },
            {
                "q": u"Как обратиться к полю lyudi словаря otk?",
                "options": ['otk["lyudi"]', "otk.lyudi", "otk(lyudi)",
                            'otk["lyudi", 0]'],
                "answer": 0,
            },
            {
                "q": u"Что сделает запись d[\"novy\"] = 5, если ключа \"novy\" нет?",
                "options": [u"добавит новое поле в словарь",
                            u"вызовет SyntaxError",
                            u"удалит словарь",
                            u"ничего не сделает"],
                "answer": 0,
            },
            {
                "q": u"Какая ошибка возникнет при обращении к несуществующему ключу?",
                "options": [u"KeyError", u"IndexError", u"TypeError",
                            u"ValueError"],
                "answer": 0,
            },
            {
                "q": u"Как проверить, есть ли ключ \"voda\" в словаре otk?",
                "options": ['if "voda" in otk:', 'if otk.has("voda"):',
                            "if otk == \"voda\":", 'if "voda" is otk:'],
                "answer": 0,
            },
        ]

    # ----------------------------------------------------- этап 2: симулятор
    def get_simulator_spec(self):
        """Живой архив: первый словарь из кода ученика."""
        code = getattr(self, "_student_code", "") or ""
        data = self._scan_dict(code) or dict(self.SAMPLE)
        cells = {u"arhiv": u"dict: %d" % len(data)}
        rows = [u"ключ -> значение"]
        for k, v in list(data.items())[:8]:
            cells[u"%r" % k] = u"%s: %s" % (type(v).__name__, v)
            rows.append(u"%r -> %r" % (k, v))
        return {
            "mode": "memory",
            "variables": cells,
            "lists": rows,
            "title": u"Карточка архива (%d полей)" % len(data),
        }

    def set_student_code(self, code):
        """GUI сообщает уровню текущий код редактора для живого архива."""
        self._student_code = code or ""

    @staticmethod
    def _scan_dict(code):
        """Первый литеральный словарь из кода ученика (для режима Б)."""
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return {}
        for node in ast.walk(tree):
            if isinstance(node, ast.Dict) and node.keys:
                out = {}
                for k, v in zip(node.keys, node.values):
                    try:
                        kk = ast.literal_eval(k)
                        vv = ast.literal_eval(v)
                    except Exception:
                        continue
                    out[kk] = vv
                if out:
                    return out
        return {}

    # ---------------------------------------------------- этап 3: автопроверка
    def check_task(self, sandbox, source, index):
        task = self.get_task(index)
        if not task:
            return False, u"Задача не задана."
        ok, feedback = BaseLevel.check_task(task, sandbox, source)
        if ok:
            feedback = u"✅ Запись принята архивом! " + feedback
        else:
            feedback += (u"\n💡 Помни: значение берут по ИМЕНИ ключа в "
                         u"квадратных скобках: otk[\"lyudi\"].")
        return ok, feedback

    # --------------------------------------------------------- этап 4: босс
    def check_console_boss(self, sandbox, source):
        ok, feedback = BaseLevel.check_console_boss(self, sandbox, source)
        if ok:
            feedback = (u"🏆 БОСС ПОВЕРЖЕН: главный архив колонии оцифрован — "
                        u"все отсеки учтены! " + feedback)
        return ok, feedback
