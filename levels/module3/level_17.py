# -*- coding: utf-8 -*-
"""Урок 17 — «Орбитальный радар» (КТП: Экран как декартова система).

Первый 2D-урок Модуля 3. Хронометраж 45 минут:
  * stage_1_theory    (7 мин) — экран как координатная плоскость, ось Y вниз,
    объект Actor(x, y, w, h), функция draw();
  * stage_2_simulator (8 мин) — живой PgZero-радар (SimCanvas, режим В):
    все вызовы Actor(...) из кода ученика расставляются на орбите;
  * stage_3_practice  (15 мин) — 3 задачи с автопроверкой: маяк в центр
    экрана, купол базы по координатам, два объекта + константы SCREEN;
  * stage_4_boss      (10 мин) — миссия PgZero: довести разведчик до
    посадочного маяка, не задев магнитные бури (keyboard + colliderect);
  * stage_5_quiz      (5 мин) — 5 вопросов, оценка 2–5, чекпоинт.
"""

import ast
import math

from engine.canvas_sim import Actor
from levels.base_level import BaseLevel


def _node(nid, kind, text):
    return {"id": nid, "kind": kind, "text": text}


#: Фабрика учебного объекта Actor(x, y, w, h) для песочницы (уроки 17–21).
#: Атрибут ``canvas`` позволяет автопроверке доставать координаты ученика.
ACTOR_SRC = u"""\
class Actor(object):
    def __init__(self, x=0, y=0, w=40, h=40, canvas=None):
        self.x, self.y, self.w, self.h = float(x), float(y), float(w), float(h)
        self.canvas = canvas
    @property
    def pos(self):
        return (self.x, self.y)
    def draw_self(self):
        if self.canvas is not None:
            self.canvas.actor.pos = (self.x, self.y)
            self.canvas.actor.draw_self()
    def colliderect(self, other):
        return (abs(self.x - other.x) * 2 < (self.w + other.w) and
                abs(self.y - other.y) * 2 < (self.h + other.h))
"""


def make_actor_class():
    """Скомпилировать учебный Actor из исходника (общий для всех уроков М3)."""
    ns = {}
    exec(compile(ACTOR_SRC, "<nova_actor>", "exec"), ns)  # доверенный код движка
    return ns["Actor"]


def inject_pgzero(sandbox):
    """Подключить к песочнице класс Actor и константы экрана SCREEN."""
    sandbox.inject(Actor=make_actor_class(),
                   SCREEN={"w": 560, "h": 300})


class Level17(BaseLevel):
    """Экран Нова-Терры как декартова система координат."""

    LEVEL_NUMBER = 17

    #: Арена босса (пиксели режима В).
    ARENA_W = 560
    ARENA_H = 300
    #: Посадочный маяк (центр цели).
    GOAL_X = 500
    GOAL_Y = 250
    #: Магнитные бури (x, y, w, h) — касаться нельзя.
    STORMS = [(280, 150, 60, 60), (390, 60, 50, 130), (180, 250, 90, 40)]

    def __init__(self):
        BaseLevel.__init__(self, {
            "number": 17,
            "title": u"Орбитальный радар",
            "theme": u"Экран как декартова система: координаты, Actor, draw()",
            "goal": u"Научиться размещать объекты базы на экране по "
                    u"координатам (x — вправо, y — вниз) и рисовать их "
                    u"функцией draw()",
            "xp_reward": 80,
        })
        self.stage_minutes = (7, 8, 15, 10, 5)

        # ------------------------------- этап 1: теория + блок-схема
        self.theory = (
            u"🛰 МОДУЛЬ 3! МЫ ВЫХОДИМ В ЭФИР И ОТКРЫВАЕМ ORBITAL RADAR.\n\n"
            u"Экран монитора — это ДЕКАРТОВА ПЛОСКОСТЬ, но с хитростью:\n"
            u"* ось X идёт ВПРАВО (как в математике);\n"
            u"* ось Y идёт ВНИЗ! Верхний левый угол экрана — это (0; 0),\n"
            u"  а не центр. Чем больше y — тем НИЖЕ объект.\n\n"
            u"В нашем эмуляторе PgZero (встроен в движок, без сторонних\n"
            u"библиотек!) любой объект — это ACTOR:\n\n"
            u"    mayak = Actor(300, 200)      # точка (x; y) — ЦЕНТР объекта\n"
            u"    dome  = Actor(100, 50, 80, 60)  # x, y, ширина w, высота h\n\n"
            u"Атрибуты: mayak.x, mayak.y, mayak.pos = (x, y).\n"
            u"Размер экрана задают константы SCREEN.w и SCREEN.h\n"
            u"(у нашего радара это 560 x 300 пикселей).\n\n"
            u"Функция DRAW() вызывается каждый кадр и рисует объекты:\n\n"
            u"    def draw():\n"
            u"        mayak.draw_self()\n"
            u"        dome.draw_self()\n\n"
            u"Команда mayak.draw_self() выводит спрайт ровно в его координатах."
            u"\n\nЗАДАЧА ИНЖЕНЕРА: разметить орбитальную карту — посадочные\n"
            u"маяки и купола базы — по точным координатам!")
        self.briefing = self.theory
        self.flowchart = {
            "nodes": [
                _node("start", "start", u"Старт урока: экран 560x300"),
                _node("c1", "condition", u"x < SCREEN.w / 2 ?"),
                _node("l", "process", u"mayak.x = 150 (левый фланг)"),
                _node("r", "process", u"mayak.x = 410 (правый фланг)"),
                _node("dome", "process", u"dome = Actor(280, 210, 90, 70)"),
                _node("dr", "io", u"draw(): mayak.draw_self(), dome.draw_self()"),
                _node("end", "end", u"Радар: метки на карте сектора"),
            ],
            "edges": [("start", "c1"), ("c1", "l"), ("c1", "r"),
                      ("l", "dome"), ("r", "dome"), ("dome", "dr"),
                      ("dr", "end")],
        }

        # --------------------------------------- этап 2: симулятор
        self.simulator = {
            "mode": "pgzero",
            "variables": {u"SCREEN.w": u"int: 560",
                          u"SCREEN.h": u"int: 300",
                          u"actor": u"Actor(x, y, w, h)"},
            "lists": [u"X -> вправо", u"Y -> вниз", u"(0,0) - верхний левый угол"],
            "title": u"Орбитальный радар",
        }

        # ---------------------------------------- этап 3: практика
        self.tasks = [
            {
                "prompt": u"МАЯК В ЦЕНТР ЭКРАНА. Создай mayak = Actor(280, 150) "
                          u"и напечатай его координаты ДВУМЯ строками: сначала "
                          u"x (ответ 280), затем y (ответ 150). Не перепутай "
                          u"порядок аргументов: Actor(x, y)!",
                "starter": u"",
                "hint": u"mayak = Actor(280, 150)\nprint(mayak.x)\nprint(mayak.y)",
                "expect_print": [u"280", u"150"],
                "prints_in_order": True,
                "expect_print_count": 2,
                "forbidden": [u"while", u"input"],
            },
            {
                "prompt": u"РАЗМЕТИКА БАЗЫ. Купол habitat лежит на широте 200: "
                          u"habitat = Actor(120, 200, 80, 60). Напечатай ровно "
                          u"3 строки: pos кортежем (ответ (120.0, 200.0)), "
                          u"ширину w (80.0) и высоту h (60.0).",
                "starter": u"habitat = Actor(120, 200, 80, 60)\n",
                "hint": u"print(habitat.pos)\nprint(habitat.w)\nprint(habitat.h)",
                "expect_print": [u"(120.0, 200.0)", u"80.0", u"60.0"],
                "prints_in_order": True,
                "expect_print_count": 3,
                "forbidden": [u"while"],
            },
            {
                "prompt": u"ДВА КУПОЛА И КОНСТАНТЫ. В коде уже заданы размеры "
                          u"экрана SCREEN_w = 560, SCREEN_h = 300. Добавь "
                          u"купол kupol = Actor(400, 100, 90, 70) и маяк "
                          u"mayak = Actor(SCREEN_w // 2, SCREEN_h // 2) — "
                          u"строго в центр радара. Выведи ровно 2 строки: "
                          u"pos купола (400.0, 100.0) и pos маяка (280.0, 150.0).",
                "starter": u"SCREEN_w = 560\nSCREEN_h = 300\n",
                "hint": u"kupol = Actor(400, 100, 90, 70)\n"
                        u"mayak = Actor(SCREEN_w // 2, SCREEN_h // 2)\n"
                        u"print(kupol.pos)\nprint(mayak.pos)",
                "expect_print": [u"(400.0, 100.0)", u"(280.0, 150.0)"],
                "prints_in_order": True,
                "expect_print_count": 2,
                "forbidden": [u"while"],
            },
        ]

        # ------------------------------------------ этап 4: босс
        self.boss = {
            "title": u"Calibration Run: разведчик к посадочному маяку",
            "mode": "pgzero",
            "desc": u"Управляй разведчиком стрелками. Доведи его от точки "
                    u"спуска (30; 30) до посадочного маяка 🚀 в правом нижнем "
                    u"углу радара, НЕ задев красные магнитные бури 🪨. "
                    u"Центр маяка: (%d; %d). Стены-бури: %s. "
                    u"Касание бури = перезапуск миссии кнопкой «Миссия»."
                    % (self.GOAL_X, self.GOAL_Y, str(self.STORMS)),
            "arena": {"start": (30, 30), "speed": 4,
                      "goal_x": self.GOAL_X, "goal_y": self.GOAL_Y},
            "walls": self.STORMS,
            "icon": u"🛰",
            "color": u"#58a6ff",
        }

        # ------------------------------------------- этап 5: тест
        self.quiz = [
            {
                "q": u"Где находится точка (0; 0) на экране?",
                "options": [u"в верхнем левом углу", u"в центре экрана",
                            u"в нижнем правом углу", u"на произвольном месте"],
                "answer": 0,
            },
            {
                "q": u"Чем отличается экранная ось Y от математической?",
                "options": [u"она направлена вниз: больше y — ниже объект",
                            u"она отсутствует",
                            u"она измеряется в градусах",
                            u"она всегда отрицательная"],
                "answer": 0,
            },
            {
                "q": u"Что задаёт Actor(100, 200)?",
                "options": [u"объект с центром в точке x=100, y=200",
                            u"прямоугольник от (100;100) до (200;200)",
                            u"два отдельных числа-переменных",
                            u"цвет пикселя 100200"],
                "answer": 0,
            },
            {
                "q": u"Зачем нужна функция draw()?",
                "options": [u"она вызывается каждый кадр и рисует объекты",
                            u"она удаляет объекты с экрана",
                            u"она считает FPS",
                            u"она читает клавиатуру"],
                "answer": 0,
            },
            {
                "q": u"Как разместить спрайт ровно по центру экрана 560x300?",
                "options": [u"Actor(SCREEN.w // 2, SCREEN.h // 2)",
                            u"Actor(0, 0)",
                            u"Actor(560, 300)",
                            u"Actor.center()"],
                "answer": 0,
            },
        ]

    # -------------------------------------------------- этап 2: симулятор
    def get_simulator_spec(self):
        """Живой PgZero-радар: все Actor(...) из кода ученика на орбите."""
        code = getattr(self, "_student_code", "") or ""
        specs = self._scan_actors(code)
        variables = {u"SCREEN.w": u"int: %d" % self.ARENA_W,
                     u"SCREEN.h": u"int: %d" % self.ARENA_H,
                     u"объектов на карте": u"int: %d" % len(specs)}
        lists = [u"Actor(x, y, w, h) — центр в (x; y), ось Y вниз"]
        for i, s in enumerate(specs[:6]):
            lists.append(u"%d: (%.0f; %.0f) %.0fx%.0f" % (i + 1, s[0], s[1],
                                                           s[2], s[3]))
        return {"mode": "pgzero", "variables": variables, "lists": lists,
                "title": u"Орбитальный радар (режим В)",
                "objects": specs}

    def set_student_code(self, code):
        """GUI сообщает уровню текущий код редактора для живого радара."""
        self._student_code = code or ""

    @staticmethod
    def _scan_actors(code):
        """Вытащить вызовы Actor(x, y[, w, h]) с литеральными числами."""
        out = []
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return out
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            f = node.func
            fname = getattr(f, "id", None) or getattr(f, "attr", None)
            if fname != "Actor":
                continue
            nums = []
            for arg in node.args[:4]:
                try:
                    v = ast.literal_eval(arg)
                except Exception:                    # noqa: BLE001
                    v = None
                if isinstance(v, (int, float)) and not isinstance(v, bool):
                    nums.append(float(v))
            if len(nums) >= 2:
                w = nums[2] if len(nums) > 2 else 40.0
                h = nums[3] if len(nums) > 3 else 40.0
                out.append((nums[0], nums[1], w, h))
        return out

    def build_sim_scene(self, canvas):
        """Сцена живого радара (режим В): орбита + объекты кода ученика."""
        sw, sh = canvas.screen["width"], canvas.screen["height"]
        cx, cy = sw // 2, sh // 2
        specs = self.get_simulator_spec().get("objects") or []
        actors = []
        palette = ["#58a6ff", "#3fb950", "#d29922", "#bc8cff", "#ffa657",
                   "#f85149"]
        for i, (ax, ay, aw, ah) in enumerate(specs[:6]):
            a = Actor(canvas, ax, ay, aw, ah)
            a.color = palette[i % len(palette)]
            a.icon = u"🛰" if i % 2 == 0 else u"🏠"
            actors.append(a)

        state = {"angle": 0.0}

        def update(dt):
            state["angle"] += dt * 1.2          # спутник летит по орбите

        def draw():
            canvas._draw_planet_bg()
            # рамка радара и оси координат
            canvas.create_rectangle(2, 2, sw - 2, sh - 2, outline="#30363d")
            canvas.create_line(0, cy, sw, cy, fill="#30363d")
            canvas.create_line(cx, 0, cx, sh, fill="#30363d")
            canvas.create_text(14, 12, text=u"(0,0)", fill="#8b949e",
                               font=("Courier", 8, "bold"))
            canvas.create_text(sw - 24, sh - 12, text=u"(%d,%d)" % (sw, sh),
                               fill="#8b949e", font=("Courier", 8, "bold"))
            # база в центре
            base = Actor(canvas, cx, cy, 60, 46, color="#21262d", icon=u"🏗")
            base.draw_self()
            # орбитальный спутник
            ox = cx + int(90 * math.cos(state["angle"]))
            oy = cy + int(60 * math.sin(state["angle"]))
            orb = Actor(canvas, ox, oy, 26, 26, color="#1f6feb", icon=u"🛰")
            orb.draw_self()
            for a in actors:
                a.draw_self()
            info = (u"Объектов из твоего кода: %d — пиши Actor(x, y) и жми "
                    u"«Симулятор»" % len(actors))
            canvas.create_text(sw // 2, sh - 12, text=info, fill="#58a6ff",
                               font=("Courier", 8, "bold"))
        return {"update": update, "draw": draw}

    # ------------------------------------------------ этап 3: автопроверка
    def check_task(self, sandbox, source, index):
        task = self.get_task(index)
        if not task:
            return False, u"Задача не задана."
        inject_pgzero(sandbox)
        ok, feedback = BaseLevel.check_task(task, sandbox, source)
        if ok:
            feedback = u"✅ Метка нанесена на орбитальную карту! " + feedback
        else:
            feedback += (u"\n💡 Помни: Actor(x, y) — первый аргумент X "
                         u"(вправо), второй Y (вниз).")
        return ok, feedback

    # ------------------------------------------------------------ босс
    def check_console_boss(self, sandbox, source):
        inject_pgzero(sandbox)
        ok, feedback = BaseLevel.check_console_boss(self, sandbox, source)
        if ok:
            feedback = (u"🏆 БОСС ПОВЕРЖЕН: радар откалиброван, маяки на "
                        u"карте! " + feedback)
        return ok, feedback
