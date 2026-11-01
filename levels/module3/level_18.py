# -*- coding: utf-8 -*-
"""Урок 18 — «Спутник связи» (КТП: Игровой цикл Game Loop).

Хронометраж 45 минут:
  * stage_1_theory    (7 мин) — понятие FPS, непрерывный цикл update(),
    плавное изменение actor.x / actor.y по кадрам;
  * stage_2_simulator (8 мин) — живой PgZero-симулятор (режим В): спутник
    летит по круговой орбите вокруг базы со скоростью из кода ученика;
  * stage_3_practice  (15 мин) — 3 задачи с автопроверкой: шаг по X, счётчик
    кадров цикла, окружность через math.cos/sin;
  * stage_4_boss      (10 мин) — миссия PgZero: связь установится, если
    спутник сделает полный круг по орбите и вернётся к старту;
  * stage_5_quiz      (5 мин) — 5 вопросов, оценка 2–5, чекпоинт.
"""

import ast
import math

from engine.canvas_sim import Actor
from levels.base_level import BaseLevel
from levels.module3.level_17 import inject_pgzero, _node


class Level18(BaseLevel):
    """Игровой цикл: 30 кадров в секунду двигают спутник по орбите."""

    LEVEL_NUMBER = 18

    #: Центр орбиты относительно размера экрана (доли).
    ORBIT_CX_RATIO = 0.5
    ORBIT_CY_RATIO = 0.5
    ORBIT_RX = 110          # горизонтальный радиус орбиты, px
    ORBIT_RY = 70           # вертикальный радиус орбиты, px

    def __init__(self):
        BaseLevel.__init__(self, {
            "number": 18,
            "title": u"Спутник связи",
            "theme": u"Игровой цикл Game Loop: FPS, update(), плавное движение",
            "goal": u"Понять, как бесконечный цикл кадров update() превращает "
                    u"маленькие шаги actor.x / actor.y в плавный полёт спутника",
            "xp_reward": 80,
        })
        self.stage_minutes = (7, 8, 15, 10, 5)

        # ------------------------------- этап 1: теория + блок-схема
        self.theory = (
            u"📡 СПУТНИК СВЯЗИ НА ОРБИТЕ! ЧТО ДЕРЖИТ ЕГО В ПОЛЁТЕ?\n\n"
            u"Ответ — GAME LOOP, ИГРОВОЙ ЦИКЛ. Это сердце любой игры и "
            u"любой анимации:\n\n"
            u"    пока игра жива:\n"
            u"        1) обработать ввод (клавиатура);\n"
            u"        2) update()   — обновить позиции объектов;\n"
            u"        3) draw()     — нарисовать новый кадр.\n\n"
            u"Цикл повторяется ~30 раз в секунду — это и есть FPS "
            u"(frames per second, кадров в секунду). Каждый вызов update() "
            u"— ОДИН КАДР.\n\n"
            u"ПЛАВНОСТЬ = МАЛЕНЬКИЕ ШАГИ. Спутник не перепрыгивает на новое "
            u"место — на каждом кадре он сдвигается чуть-чуть:\n\n"
            u"    sputnik.x = sputnik.x + 2     # на 2 пикселя вправо за кадр\n\n"
            u"За секунду это 2 * 30 = 60 пикселей — плавный полёт!\n\n"
            u"КРУГОВАЯ ОРБИТА считается тригонометрией (модуль math):\n\n"
            u"    ugol = ugol + 0.05                       # фаза растёт по кадрам\n"
            u"    sputnik.x = cx + R * math.cos(ugol)      # cos — горизонталь\n"
            u"    sputnik.y = cy + R * math.sin(ugol)      # sin — вертикаль\n\n"
            u"В эмуляторе движка за цикл отвечают функции UPDATE() и DRAW() — "
            u"их запускает SimCanvas (режим PgZero). Никаких сторонних "
            u"библиотек: чистый tkinter + math!")
        self.briefing = self.theory
        self.flowchart = {
            "nodes": [
                _node("start", "start", u"Старт: ugol = 0"),
                _node("upd", "process", u"update(): кадры идут -> ugol += shag"),
                _node("calc", "process", u"x = cx + R*cos(ugol), y = cy + R*sin(ugol)"),
                _node("drw", "io", u"draw(): кадр на экран (~30 FPS)"),
                _node("c1", "condition", u"ugol >= 2*pi? (полный круг)"),
                _node("lnk", "io", u"print('СВЯЗЬ УСТАНОВЛЕНА')"),
                _node("end", "end", u"Цикл завершён: канал связи открыт"),
            ],
            "edges": [("start", "upd"), ("upd", "calc"), ("calc", "drw"),
                      ("drw", "c1"), ("c1", "upd"), ("c1", "lnk"),
                      ("lnk", "end")],
        }

        # --------------------------------------- этап 2: симулятор
        self.simulator = {
            "mode": "pgzero",
            "variables": {u"FPS": u"int: 30",
                          u"ugol": u"float: 0.0",
                          u"sputnik.pos": u"(cx + R*cos, cy + R*sin)"},
            "lists": [u"update() каждый кадр", u"draw() каждый кадр",
                      u"шаг фазы берётся из твоего кода"],
            "title": u"Орбита связи",
        }

        # ---------------------------------------- этап 3: практика
        self.tasks = [
            {
                "prompt": u"ШАГ ЗА КАДР. Спутник st = Actor(0, 100) стартует "
                          u"из левого края. Напиши ЦИКЛ for на 5 кадров, в "
                          u"котором на каждом шаге st.x увеличивается на 2 "
                          u"(st.x = st.x + 2 или st.x += 2). После цикла "
                          u"напечатай итоговый x. Ответ: 10 (5 кадров * 2 px).",
                "starter": u"st = Actor(0, 100)\n",
                "hint": u"for kadr in range(5):\n    st.x = st.x + 2\nprint(st.x)",
                "expect_print": [u"10"],
                "expect_print_count": 1,
                "forbidden": [u"while"],
            },
            {
                "prompt": u"СЧЁТЧИК КАДРОВ. Пройди циклом for по range(12) и "
                          u"на каждой итерации увеличивай переменную kadr на 1 "
                          u"(начни с kadr = 0). В конце напечатай число "
                          u"сделанных кадров. Ответ: 12.",
                "starter": u"kadr = 0\n",
                "hint": u"for i in range(12):\n    kadr += 1\nprint(kadr)",
                "expect_print": [u"12"],
                "expect_print_count": 1,
                "assert_vars": {"kadr": 12},
                "forbidden": [u"while"],
            },
            {
                "prompt": u"ТОЧКА НА ОКРУЖНОСТИ. База в центре (cx=280, "
                          u"cy=150), радиус орбиты R=100. Импортируй math "
                          u"(import math), посчитай для ugol = 0 позицию "
                          u"спутника: sx = cx + R * math.cos(ugol), "
                          u"sy = cy + R * math.sin(ugol) и напечатай ровно "
                          u"2 строки: sx (ответ 380.0) и sy (ответ 150.0).",
                "starter": u"import math\ncx = 280\ncy = 150\nR = 100\nugol = 0\n",
                "hint": u"sx = cx + R * math.cos(ugol)\nsy = cy + R * math.sin(ugol)\n"
                        u"print(sx)\nprint(sy)",
                "expect_print": [u"380.0", u"150.0"],
                "prints_in_order": True,
                "expect_print_count": 2,
                "forbidden": [u"while"],
            },
        ]

        # ------------------------------------------ этап 4: босс
        self.boss = {
            "title": u"Полный круг: открыть канал связи с колонией",
            "mode": "console",
            "desc": u"БОСС: смоделируй игровой цикл спутника. Сделай цикл "
                    u"for po phase in range(63): на каждом кадре увеличивай "
                    u"phase на 0.1 и пересчитывай позицию орбиты: "
                    u"sx = 280 + 110 * math.cos(phase), "
                    u"sy = 150 + 70 * math.sin(phase) (импортируй math). "
                    u"Веди счётчик кадров kadr (+1 за цикл). Когда цикл "
                    u"завершится (фаза прошла 2*pi ≈ полный круг), выведи "
                    u"РОВНО 3 строки по порядку: 1) 'КАДРОВ: 63'; "
                    u"2) 'СВЯЗЬ УСТАНОВЛЕНА'; 3) 'ПОЗИЦИЯ: 389, 143' — "
                    u"округлённые int(round(sx)), int(round(sy)) финальной "
                    u"точки орбиты. Ручные константы вместо расчёта циклом "
                    u"автопроверка не примет!",
            "starter": u"import math\nphase = 0.0\nkadr = 0\n",
            "expect_print": [u"КАДРОВ: 63", u"СВЯЗЬ УСТАНОВЛЕНА",
                             u"ПОЗИЦИЯ: 389, 143"],
            "prints_in_order": True,
            "expect_print_count": 3,
            "forbidden": [u"while"],
        }

        # ------------------------------------------- этап 5: тест
        self.quiz = [
            {
                "q": u"Что такое игровой цикл (game loop)?",
                "options": [u"повторяющийся набор: ввод -> update() -> draw()",
                            u"однократный запуск программы",
                            u"файл с картинками игры",
                            u"кнопка «Старт»"],
                "answer": 0,
            },
            {
                "q": u"FPS — это…",
                "options": [u"число кадров, рисуемых за секунду",
                            u"скорость интернета",
                            u"размер экрана",
                            u"число клавиш на клавиатуре"],
                "answer": 0,
            },
            {
                "q": u"Почему движение получается плавным?",
                "options": [u"за каждый кадр объект сдвигается на маленький шаг",
                            u"Python сам сглаживает картинки",
                            u"экран мерцает быстрее глаз",
                            u"объекты не двигаются вообще"],
                "answer": 0,
            },
            {
                "q": u"Какие функции модуля math задают точку окружности?",
                "options": [u"math.cos (x) и math.sin (y)",
                            u"math.sqrt и math.pi",
                            u"math.floor и math.ceil",
                            u"math.pow и math.exp"],
                "answer": 0,
            },
            {
                "q": u"Что произойдёт, если в update() забыть менять координаты?",
                "options": [u"картинка замерла — объекты стоят на месте",
                            u"программа упадёт с ошибкой",
                            u"спутник улетит с орбиты сам",
                            u"FPS вырастет"],
                "answer": 0,
            },
        ]

    # -------------------------------------------------- этап 2: симулятор
    @staticmethod
    def _scan_step(code):
        """Найти в коде ученика приращение фазы (ugol/phase += число)."""
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return None
        best = None
        for node in ast.walk(tree):
            if isinstance(node, (ast.AugAssign, ast.Assign)):
                targets = ([node.target] if isinstance(node, ast.AugAssign)
                           else node.targets)
                names = {getattr(t, "id", "") for t in targets}
                if names & {"ugol", "phase", "shag", "step"}:
                    try:
                        val = ast.literal_eval(node.value)
                    except Exception:                # noqa: BLE001
                        continue
                    if isinstance(val, (int, float)) and not isinstance(val, bool):
                        v = abs(float(val))
                        if 0 < v <= 1.0 and (best is None or v < best):
                            best = v
        return best

    def get_simulator_spec(self):
        """Скорость спутника наследуется из кода ученика (фаза за кадр)."""
        code = getattr(self, "_student_code", "") or ""
        step = self._scan_step(code)
        variables = {u"FPS": u"int: 30",
                     u"шаг фазы из кода": (u"float: %.3f" % step)
                     if step else u"не найден (по умолч. 0.05)",
                     u"орбита": u"R=%d x r=%d px" % (self.ORBIT_RX,
                                                     self.ORBIT_RY)}
        lists = [u"update(): фаза растёт каждый кадр",
                 u"x = cx + Rx*cos(ugol); y = cy + Ry*sin(ugol)",
                 u"draw(): новый кадр ~30 раз в секунду"]
        return {"mode": "pgzero", "variables": variables, "lists": lists,
                "title": u"Орбита связи (режим В)", "step": step}

    def set_student_code(self, code):
        """GUI сообщает уровню текущий код редактора для живого симулятора."""
        self._student_code = code or ""

    def build_sim_scene(self, canvas):
        """Живая орбита: спутник движется по кругу, скорость — из кода."""
        sw, sh = canvas.screen["width"], canvas.screen["height"]
        cx, cy = int(sw * self.ORBIT_CX_RATIO), int(sh * self.ORBIT_CY_RATIO)
        step = self.get_simulator_spec().get("step") or 0.05
        state = {"angle": 0.0, "laps": 0}
        orbit = Actor(canvas, cx + self.ORBIT_RX, cy, 26, 26,
                      color="#1f6feb", icon=u"🛰")
        base = Actor(canvas, cx, cy, 56, 44, color="#21262d", icon=u"📡")

        def update(dt):
            state["angle"] += step * max(1.0, dt * 30.0)
            if state["angle"] >= 2 * math.pi:
                state["angle"] -= 2 * math.pi
                state["laps"] += 1
            orbit.x = cx + self.ORBIT_RX * math.cos(state["angle"])
            orbit.y = cy + self.ORBIT_RY * math.sin(state["angle"])

        def draw():
            canvas._draw_planet_bg()
            canvas.create_oval(cx - self.ORBIT_RX, cy - self.ORBIT_RY,
                               cx + self.ORBIT_RX, cy + self.ORBIT_RY,
                               outline="#30363d")
            base.draw_self()
            canvas.create_line(cx, cy, orbit.x, orbit.y, fill="#8957e5")
            orbit.draw_self()
            canvas.create_text(sw // 2, 14,
                               text=u"КАДРОВ/С: 30 | КРУГОВ: %d | ШАГ ФАЗЫ: "
                                    u"%.3f" % (state["laps"], step),
                               fill="#58a6ff", font=("Courier", 9, "bold"))
        return {"update": update, "draw": draw}

    # ------------------------------------------------ этап 3: автопроверка
    def check_task(self, sandbox, source, index):
        task = self.get_task(index)
        if not task:
            return False, u"Задача не задана."
        inject_pgzero(sandbox)
        ok, feedback = BaseLevel.check_task(task, sandbox, source)
        if ok:
            feedback = u"✅ Кадр принят! Орбита корректируется. " + feedback
        else:
            feedback += (u"\n💡 Вспомни game loop: каждый кадр — маленький "
                         u"шаг. Цикл for делает N кадров подряд.")
        return ok, feedback

    # ------------------------------------------------------------ босс
    def check_console_boss(self, sandbox, source):
        inject_pgzero(sandbox)
        ok, feedback = BaseLevel.check_console_boss(self, sandbox, source)
        if ok:
            feedback = (u"🏆 БОСС ПОВЕРЖЕН: спутник сделал полный круг, "
                        u"канал связи с колонией открыт! " + feedback)
        return ok, feedback
