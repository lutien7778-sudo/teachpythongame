# -*- coding: utf-8 -*-
"""base_level.py — контракт урока игры «Проект "Нова-Терра"».

Каждый уровень (урок 45 минут) состоит из 5 этапов:

1. **Брифинг + Схема**    — легенда сектора и блок-схема алгоритма (SimCanvas, режим А);
2. **Симулятор**          — интерактивная визуализация (режим Б или В);
3. **Практика (3 задачи)** — редактор кода + песочница, автопроверка print/eval;
4. **Босс-миссия**        — игровая миссия сектора базы (PgZero-эмулятор или консоль);
5. **Тест (5 вопросов)**  — викторина, итоговая оценка 2–5 и чекпоинт.

Уровень описывается данными (см. ``levels/ktp_registry.py``) и загружается
динамически через ``levels/level_loader.py``. Класс ``BaseLevel`` умеет сам
собирать все этапы из словаря-описания; наследники могут переопределять любой
метод (например, дать уникальную босс-логику в ``build_boss_scene``).
"""

import random

#: Порядок и названия 5 этапов урока (45 минут).
STAGE_FLOWCHART = 0
STAGE_SIMULATOR = 1
STAGE_PRACTICE = 2
STAGE_BOSS = 3
STAGE_QUIZ = 4

STAGE_NAMES = [
    u"1. Брифинг + Схема",
    u"2. Симулятор",
    u"3. Практика (3 задачи)",
    u"4. Босс-миссия сектора",
    u"5. Тест (5 вопросов)",
]

STAGE_MINUTES = [7, 8, 15, 10, 5]     # хронометраж 45-минутного урока

#: Баллы -> оценка по 5-балльной шкале.
GRADE_SCALE = [(90, 5), (75, 4), (55, 3), (0, 2)]


def grade_from_percent(percent):
    """Перевести процент правильных ответов в оценку 2..5."""
    for border, grade in GRADE_SCALE:
        if percent >= border:
            return grade
    return 2


class BaseLevel(object):
    """Данные + поведение одного урока.

    Атрибуты (заполняются level_loader из описания КТП):

    * ``number`` — номер уровня 1..34;
    * ``title``, ``theme``, ``goal`` — название/тема/цель урока;
    * ``briefing`` — текст легенды;
    * ``flowchart`` — dict(nodes=[...], edges=[...]) для этапа 1;
    * ``simulator`` — dict(mode="memory"|"pgzero", variables/lists/matrices...)
      для этапа 2;
    * ``tasks`` — список из 3 задач {prompt, starter, checks};
    * ``boss`` — dict(title, mode, arena, walls, goal_code, success_print)
      для этапа 3 (босс-миссия);
    * ``quiz`` — список 5 вопросов {q, options, answer} для теста;
    * ``xp_reward`` — опыт за прохождение.
    """

    def __init__(self, description=None):
        d = description or {}
        self.number = int(d.get("number", 1))
        self.title = d.get("title", u"Урок %d" % self.number)
        self.theme = d.get("theme", "")
        self.goal = d.get("goal", "")
        self.briefing = d.get("briefing", "")
        self.flowchart = d.get("flowchart", {"nodes": [], "edges": []})
        self.simulator = d.get("simulator", {"mode": "memory"})
        self.tasks = list(d.get("tasks", []))
        self.boss = d.get("boss", {})
        self.quiz = list(d.get("quiz", []))
        self.xp_reward = int(d.get("xp_reward", 50))
        #: прогресс этапов: 0 — не пройден, 1 — пройден
        self.stage_done = [False] * 5
        self._rnd = random.Random(1000 + self.number)

    # ------------------------------------------------------------ статус
    @property
    def current_stage(self):
        for i, done in enumerate(self.stage_done):
            if not done:
                return i
        return 4

    def is_completed(self):
        return all(self.stage_done)

    def mark_done(self, stage_index):
        if 0 <= stage_index < 5:
            self.stage_done[stage_index] = True

    def progress_percent(self):
        return int(100.0 * sum(1 for x in self.stage_done if x) / 5.0)

    # ------------------------------------------------------ этап 1: схема
    def get_flowchart(self):
        """Вернуть (nodes, edges) блок-схемы брифинга."""
        nodes = self.flowchart.get("nodes", [])
        edges = self.flowchart.get("edges", [])
        return nodes, edges

    # --------------------------------------------------- этап 2: симулятор
    def get_simulator_spec(self):
        return self.simulator

    # ---------------------------------------------------- этап 3: практика
    def get_task(self, index):
        """Задача с индексом 0..2 (или None)."""
        if 0 <= index < len(self.tasks):
            return self.tasks[index]
        return None

    @staticmethod
    def check_task(task, sandbox, source):
        """Автопроверка задачи ученика.

        Возвращает (ok: bool, feedback: str). Проверяются:
        * ``must_run``   — код обязан выполниться без ошибок;
        * ``expect_print``— список подстрок, которые обязаны появиться в print();
        * ``expect_vars`` — dict {имя: ожидаемое значение} после запуска;
        * ``forbidden``  — подстроки, которых в коде быть не должно.
        """
        if not task:
            return False, u"Задача не задана."
        src = (source or "").strip()
        if not src:
            return False, u"Пусто! Напиши код в редакторе и нажми «Запустить»."
        for bad in task.get("forbidden", []):
            if bad in src:
                return False, u"Нельзя использовать «%s» в этом задании." % bad
        ok, printed = sandbox.capture_print(src)
        if not ok:
            err = sandbox.last_error
            return False, u"Код завершился с ошибкой: %s" % (
                err if err else "см. терминал")
        for frag in task.get("expect_print", []):
            joined = "\n".join(printed)
            if str(frag) not in joined:
                return False, u"Ожидался вывод, содержащий «%s». Получено: %s" % (
                    frag, joined or "<пусто>")
        for name, expected in task.get("expect_vars", {}).items():
            found, value = sandbox.eval_expr(name)
            if not found:
                return False, u"Переменная «%s» не создана (код её не определяет)." % name
            if value != expected:
                return False, u"«%s» = %r, а должно быть %r." % (name, value, expected)
        return True, u"Отлично! Система сектора подтверждает монтаж. +XP"

    # ------------------------------------------------------- этап 4: босс
    def get_boss_spec(self):
        return self.boss

    def build_boss_scene(self, canvas):
        """Подготовить арену босса на SimCanvas (режим PgZero).

        Возвращает dict(update=fn, draw=fn) — функции игрового цикла.
        Реализация по умолчанию: «дойди до цели, не касаясь стен».
        """
        spec = self.boss or {}
        arena = spec.get("arena", {})
        goal_x = arena.get("goal_x", canvas.screen["width"] - 40)
        goal_y = arena.get("goal_y", canvas.screen["height"] - 60)
        from_start = arena.get("start", (30, 30))
        speed = arena.get("speed", 3)
        canvas.actor.pos = from_start
        canvas.actor.icon = spec.get("icon", u"🤖")
        canvas.actor.color = spec.get("color", "#3fb950")
        walls = []
        from engine.canvas_sim import Actor
        for (wx, wy, ww, wh) in spec.get("walls", []):
            walls.append(Actor(canvas, wx, wy, ww, wh,
                               color="#f85149", icon=u"🪨"))
        canvas.add_walls(walls)
        goal = Actor(canvas, goal_x, goal_y, 34, 34,
                     color="#d29922", icon=u"🚀")
        state = {"won": False, "lost": False}

        def update(dt):
            kb = canvas.keyboard
            dx = dy = 0
            if kb.left:
                dx -= speed
            if kb.right:
                dx += speed
            if kb.up:
                dy -= speed
            if kb.down:
                dy += speed
            canvas.actor.move(dx, dy)
            canvas.actor.clamp_to_screen()
            if canvas.collide_with_walls(canvas.actor):
                state["lost"] = True
                canvas.stop_game_loop(silent=True)
            elif canvas.actor.colliderect(goal):
                state["won"] = True
                canvas.stop_game_loop(silent=True)

        def draw():
            for wall in canvas.walls:
                wall.draw_self()
            goal.draw_self()
            canvas.actor.draw_self()
            if state["won"]:
                msg = u"БОСС ПОВЕРЖЕН: %s" % spec.get("title", u"сектор чист")
                canvas.create_text(canvas.screen["width"] // 2, 24,
                                   text=msg, fill="#3fb950",
                                   font=("Courier", 12, "bold"))
            elif state["lost"]:
                canvas.create_text(canvas.screen["width"] // 2, 24,
                                   text=u"ЩИТ ПРОБИТ! Старт миссии — кнопка «Миссия»",
                                   fill="#f85149", font=("Courier", 11, "bold"))
        return {"update": update, "draw": draw, "state": state,
                "goal": goal, "walls": walls}

    # --------------------------------------------------------- этап 5: тест
    def get_quiz(self):
        return self.quiz

    def grade_quiz(self, answers):
        """answers — список выбранных индексов (или None). -> (score, grade)."""
        total = len(self.quiz) or 1
        correct = 0
        for q, ans in zip(self.quiz, answers):
            if ans is not None and ans == q.get("answer"):
                correct += 1
        percent = int(round(100.0 * correct / total))
        return {"correct": correct, "total": total, "percent": percent,
                "grade": grade_from_percent(percent)}
