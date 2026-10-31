# -*- coding: utf-8 -*-
"""canvas_sim.py — универсальный визуальный виджет ``SimCanvas``.

Три режима отрисовки на чистом ``tkinter.Canvas`` (без сторонних библиотек):

* **Режим А** — блок-схемы: овалы (старт/конец), прямоугольники (действия),
  параллелограммы (ввод/вывод), ромбы условий с подписями веток ``True``/``False``;
* **Режим Б** — ячейки памяти: переменные, списки и матрицы в виде карточек
  «имя -> значение» и сетки ячеек с индексами;
* **Режим В** — встроенный 2D-эмулятор ``PgZero`` для уроков 17–34:
  объекты ``Actor(x, y, w, h)``, метод ``.colliderect()``, коллизии со стенами,
  ``keyboard``, игровой цикл ``update() / draw()`` — всё без Pygame/PgZero.

Уровни передают в ``SimCanvas`` свои функции ``draw()``/``update()``, а также
могут вызывать ``show_flowchart()``, ``show_memory()``, ``show_grid()``.
"""

import math
import random
import time
import tkinter as tk
from tkinter import font as tkfont

# --------------------------------------------------------------------------
#  Цветовая палитра GitHub Dark
# --------------------------------------------------------------------------
BG = "#0d1117"
PANEL = "#161b22"
BORDER = "#30363d"
FG = "#c9d1d9"
ACCENT = "#58a6ff"
GREEN = "#3fb950"
RED = "#f85149"
YELLOW = "#d29922"
PURPLE = "#bc8cff"
ORANGE = "#ffa657"

FLOW_COLORS = {
    "start": ("#1f6feb", "#cde5ff"),
    "end": ("#238636", "#c6f6cf"),
    "process": ("#30363d", "#dbe4ee"),
    "io": ("#8957e5", "#e6dbff"),
    "condition": ("#9e6a03", "#ffe9b3"),
}


class SimCanvas(tk.Canvas):
    """Холст симулятора Нова-Терры с тремя режимами работы."""

    def __init__(self, master=None, width=520, height=430, **kw):
        kw.setdefault("bg", BG)
        kw.setdefault("highlightthickness", 1)
        kw.setdefault("bd", 0)
        super().__init__(master, width=width, height=height, **kw)
        self.mode = "flowchart"
        self._items = []                 # id'ы элементов текущей сцены
        self._rel_layout = {}            # раскладка блок-схемы в долях
        self.pack(fill="both", expand=True, padx=4, pady=4)

        # ---------- состояние эмулятора PgZero (режим В) ----------
        self.screen = {"width": max(120, width - 8), "height": max(120, height - 8)}
        self.keyboard = Keyboard()
        self.actor = Actor(self, x=self.screen["width"] // 2,
                           y=self.screen["height"] // 2, w=40, h=40)
        self.walls = []                  # список Actor-препятствий
        self.stars = []                  # декоративные точки планет
        self._level_draw = None
        self._level_update = None
        self._clock_id = None
        self._fps = 30
        self._frame = 0
        self._t0 = time.time()
        self._build_stars()
        self.bind("<Configure>", self._redraw_flowchart)

    # ============================================================== ОЧИСТКА
    def clear_scene(self):
        self.delete("all")
        self._items = []

    def _redraw_flowchart(self, event=None):
        """Перерисовать схему при изменении размера холста."""
        if getattr(self, "mode", "") == "flowchart" and \
                getattr(self, "_fc_nodes", None) is not None:
            self.show_flowchart(self._fc_nodes, self._fc_edges, self._fc_title)

    def _reg(self, item_id):
        self._items.append(item_id)
        return item_id

    # ======================================================= РЕЖИМ А: СХЕМЫ
    def show_flowchart(self, nodes, edges=None, title=u"Блок-схема системы"):
        """Нарисовать блок-схему.

        ``nodes`` — список словарей::

            {"id": "a", "kind": "start|end|process|io|condition",
             "text": "Текст блока"}

        ``edges`` — список ``(from_id, to_id)`` или
        ``(from_id, to_id, label)`` — подпись ставится True/False у ромбов.
        """
        self.stop_game_loop()
        self.mode = "flowchart"
        self._fc_nodes, self._fc_edges = nodes, edges or []
        self._fc_title = title
        self.clear_scene()
        layout = self._layout_flow(nodes, edges or [])
        w = self.winfo_width() or int(self.cget("width"))
        self._reg(self.create_text(
            w // 2, 14, text=title, fill=ACCENT,
            font=("Courier", 11, "bold")))
        pos = {}
        for node in nodes:
            nid = node.get("id")
            rx, ry = layout[nid]
            kind = node.get("kind", "process")
            pos[nid] = (rx, ry, kind)
            self._draw_flow_node(rx, ry, kind, node.get("text", ""))
        for e in edges or []:
            if len(e) == 3:
                a, b, label = e
            else:
                a, b, label = e[0], e[1], ""
            if a in pos and b in pos:
                self._draw_flow_edge(pos[a][:2], pos[b][:2], label)
        self._rel_layout = layout
        return pos

    @staticmethod
    def _layout_flow(nodes, edges):
        """Авто-раскладка: цепочка сверху вниз, ветки — по бокам.

        Возвращает {id: (доля_ширины_x, пиксельная_y)}.
        Ромб с двумя выходами разводит True-ветку влево, False — вправо.
        """
        succ = {}
        indeg = dict()
        ids = [n.get("id") for n in nodes]
        for nid in ids:
            indeg[nid] = 0
        for e in edges:
            a, b = e[0], e[1]
            if a in indeg and b in indeg:
                succ.setdefault(a, []).append(b)
                indeg[b] += 1
        order, queue = [], [nid for nid, d in indeg.items() if d == 0]
        seen = set()
        while queue:
            nid = queue.pop(0)
            if nid in seen:
                continue
            seen.add(nid)
            order.append(nid)
            for nxt in succ.get(nid, []):
                queue.append(nxt)
        for n in nodes:                       # изолированные узлы — в конец
            if n.get("id") not in seen:
                order.append(n.get("id"))
        kinds = {n.get("id"): n.get("kind", "process") for n in nodes}
        layout, depth = {}, {}
        y = 48
        pending_branch = None                 # (true_id, false_id, y_ромба)
        merge_y = 0
        for idx, nid in enumerate(order):
            children = succ.get(nid, [])
            if len(children) > 1:
                # узел-развилка (обычно ромб): сам идёт по центру
                layout[nid] = (0.5, y)
                depth[nid] = y
                t_id, f_id = children[0], children[1]
                label_t = ""
                label_f = ""
                for e in edges:
                    if e[0] == nid and len(e) == 3:
                        lab = str(e[2]).lower()
                        if lab.startswith("true"):
                            label_t = e[2]
                        elif lab.startswith("false"):
                            label_f = e[2]
                branch_y = y + 76
                layout[t_id] = (0.28, branch_y)
                depth[t_id] = branch_y
                layout[f_id] = (0.72, branch_y)
                depth[f_id] = branch_y
                pending_branch = (t_id, f_id, branch_y)
                merge_y = branch_y + 70
                continue
            if pending_branch and nid in pending_branch[:2]:
                continue                      # уже размещён при развилке
            if pending_branch and nid not in pending_branch[:2]:
                x, yy = 0.5, max(y, merge_y)
                pending_branch = None
            else:
                x, yy = 0.5, y
            layout[nid] = (x, yy)
            depth[nid] = yy
            y = yy + 70
        return layout

    def _flow_px(self, rel_x, rel_y):
        """Доли ширины + пиксельная вертикаль -> координаты на холсте."""
        w = self.winfo_width() or int(self.cget("width"))
        h = self.winfo_height() or int(self.cget("height"))
        return int(w * float(rel_x)), int(min(h - 30, float(rel_y)))

    def _draw_flow_node(self, rx, ry, kind, text):
        cx, cy = self._flow_px(rx, ry)
        bw, bh = 150, 44
        fill, outline = FLOW_COLORS.get(kind, FLOW_COLORS["process"])
        if kind in ("start", "end"):
            i = self._reg(self.create_oval(
                cx - bw // 2, cy - bh // 2, cx + bw // 2, cy + bh // 2,
                fill=fill, outline=outline, width=2))
        elif kind == "condition":
            i = self._reg(self.create_polygon(
                cx, cy - bh // 2 - 8, cx + bw // 2 + 12, cy,
                cx, cy + bh // 2 + 8, cx - bw // 2 - 12, cy,
                fill=fill, outline=outline, smooth=False))
        elif kind == "io":
            k = 14
            i = self._reg(self.create_polygon(
                cx - bw // 2 + k, cy - bh // 2, cx + bw // 2 + k, cy - bh // 2,
                cx + bw // 2 - k, cy + bh // 2, cx - bw // 2 - k, cy + bh // 2,
                fill=fill, outline=outline))
        else:
            i = self._reg(self.create_rectangle(
                cx - bw // 2, cy - bh // 2, cx + bw // 2, cy + bh // 2,
                fill=fill, outline=outline, width=2))
        txt = text if len(text) <= 24 else text[:23] + "…"
        self._reg(self.create_text(cx, cy, text=txt, fill="#ffffff",
                                   font=("Courier", 9, "bold")))
        return i

    def _draw_flow_edge(self, a, b, label):
        ax, ay = self._flow_px(a[0], a[1])
        bx, by = self._flow_px(b[0], b[1])
        arrow = self._reg(self.create_line(
            ax, ay + 22, bx, by - 22, fill=FG, arrow="last", width=2,
            smooth=True, splinesteps=24))
        if label:
            color = GREEN if str(label).lower().startswith("true") else RED
            mx, my = (ax + bx) // 2 + 12, (ay + by) // 2
            self._reg(self.create_text(mx, my, text=str(label), fill=color,
                                       font=("Courier", 9, "bold")))
        return arrow

    # ==================================================== РЕЖИМ Б: ПАМЯТЬ
    def show_memory(self, variables=None, lists=None, matrices=None,
                    title=u"Карта памяти модуля"):
        """Визуализировать переменные, списки и матрицы.

        ``variables`` — dict {имя: значение};
        ``lists``     — dict {имя: [...]};
        ``matrices``  — dict {имя: [[...], [...]]}.
        """
        self.stop_game_loop()
        self.mode = "memory"
        self.clear_scene()
        w = self.winfo_width() or int(self.cget("width"))
        self._reg(self.create_text(w // 2, 14, text=title, fill=ACCENT,
                                   font=("Courier", 11, "bold")))
        y = 40
        variables = variables or {}
        lists = lists or {}
        matrices = matrices or {}
        for name, value in variables.items():
            y = self._draw_var_cell(name, value, y)
        for name, seq in lists.items():
            y = self._draw_list_cells(name, list(seq), y)
        for name, grid in matrices.items():
            y = self._draw_matrix_cells(name, [list(r) for r in grid], y)
        if not (variables or lists or matrices):
            self._reg(self.create_text(w // 2, 80,
                                       text=u"Память пуста — создай переменную!",
                                       fill=YELLOW, font=("Courier", 10)))
        return y

    def _draw_var_cell(self, name, value, y):
        x0, wcell, hcell = 16, 200, 30
        self._reg(self.create_rectangle(x0, y, x0 + wcell, y + hcell,
                                        fill=PANEL, outline=BORDER))
        self._reg(self.create_text(x0 + 8, y + hcell // 2, anchor="w",
                                   text="%s =" % name, fill=PURPLE,
                                   font=("Courier", 10, "bold")))
        self._reg(self.create_text(x0 + wcell - 8, y + hcell // 2, anchor="e",
                                   text=_short(value), fill=GREEN,
                                   font=("Courier", 10, "bold")))
        return y + hcell + 6

    def _draw_list_cells(self, name, seq, y):
        cw = 44
        x0 = 16
        self._reg(self.create_text(x0, y + 6, anchor="w", text=name,
                                   fill=PURPLE, font=("Courier", 10, "bold")))
        y += 16
        for i, v in enumerate(seq[:11]):
            x = x0 + i * (cw + 4)
            self._reg(self.create_rectangle(x, y, x + cw, y + 26,
                                            fill=PANEL, outline=ACCENT))
            self._reg(self.create_text(x + cw // 2, y + 13, text=_short(v),
                                       fill=FG, font=("Courier", 9)))
            self._reg(self.create_text(x + cw // 2, y + 34, text=str(i),
                                       fill=YELLOW, font=("Courier", 8)))
        return y + 44

    def _draw_matrix_cells(self, name, grid, y):
        cw, ch = 40, 24
        x0 = 16
        self._reg(self.create_text(x0, y + 6, anchor="w", text=name,
                                   fill=PURPLE, font=("Courier", 10, "bold")))
        y += 16
        for r, row in enumerate(grid[:8]):
            for c, v in enumerate(row[:10]):
                x = x0 + c * (cw + 3)
                yy = y + r * (ch + 3)
                shade = PANEL if (r + c) % 2 == 0 else "#1c2128"
                self._reg(self.create_rectangle(x, yy, x + cw, yy + ch,
                                                fill=shade, outline=BORDER))
                self._reg(self.create_text(x + cw // 2, yy + ch // 2,
                                           text=_short(v), fill=FG,
                                           font=("Courier", 8)))
        return y + len(grid[:8]) * (ch + 3) + 10

    def show_grid(self, matrix, cell=28, colors=None, title=u"Сетка сектора"):
        """Быстрая сетка чисел/символов (матрица) — частый случай режима Б."""
        return self.show_memory(matrices={"grid": matrix}, title=title)

    # ================================================ РЕЖИМ В: PgZero-эмулятор
    def start_game_loop(self, update_fn=None, draw_fn=None, fps=30):
        """Запустить игровой цикл: ``update_fn(dt)`` затем ``draw_fn()``."""
        self.mode = "pgzero"
        self._level_update = update_fn
        self._level_draw = draw_fn
        self._fps = max(5, min(60, int(fps)))
        self._t0 = time.time()
        self.stop_game_loop(silent=True)
        self._tick()

    def stop_game_loop(self, silent=False):
        if self._clock_id is not None:
            try:
                self.after_cancel(self._clock_id)
            except (ValueError, tk.TclError):
                pass
            self._clock_id = None
        if not silent:
            pass

    def is_loop_running(self):
        return self._clock_id is not None

    def _tick(self):
        try:
            now = time.time()
            dt = now - self._t0
            self._t0 = now
            self._frame += 1
            if self._level_update:
                try:
                    self._level_update(dt)
                except Exception as exc:            # noqa: BLE001
                    self._on_loop_error(exc)
                    return
            self.delete("all")
            self._items = []
            self._draw_planet_bg()
            if self._level_draw:
                try:
                    self._level_draw()
                except Exception as exc:            # noqa: BLE001
                    self._on_loop_error(exc)
                    return
            else:
                self.actor.draw_self()
            self._clock_id = self.after(int(1000 / self._fps), self._tick)
        except tk.TclError:
            self._clock_id = None

    def _on_loop_error(self, exc):
        self.stop_game_loop(silent=True)
        w = self.winfo_width() or int(self.cget("width"))
        self._reg(self.create_text(w // 2, 20, fill=RED,
                                   text=u"Ошибка игрового цикла: %s: %s"
                                        % (type(exc).__name__, exc),
                                   font=("Courier", 9, "bold")))

    def _build_stars(self):
        rnd = random.Random(2077)
        w = int(self.cget("width"))
        h = int(self.cget("height"))
        self._stars_data = [(rnd.randint(4, w - 4), rnd.randint(4, h - 4),
                             rnd.choice((1, 1, 2))) for _ in range(40)]

    def _draw_planet_bg(self):
        for sx, sy, r in getattr(self, "_stars_data", []):
            self._reg(self.create_oval(sx, sy, sx + r, sy + r,
                                       fill="#8b949e", outline=""))
        line = self._reg(self.create_line(0, self.screen["height"] - 40,
                                          self.screen["width"],
                                          self.screen["height"] - 40,
                                          fill="#2ea043", width=2))
        return line

    def set_actor_style(self, color=GREEN, icon=u"🤖"):
        self.actor.color = color
        self.actor.icon = icon

    def add_walls(self, walls):
        """walls — список Actor (препятствия босса/склада)."""
        self.walls = list(walls)

    def collide_with_walls(self, actor):
        for wall in self.walls:
            if actor.colliderect(wall):
                return wall
        return None


def _short(value, maxlen=12):
    s = repr(value)
    if len(s) > maxlen:
        s = s[:maxlen - 1] + "…"
    return s


# --------------------------------------------------------------------------
#  PgZero-совместимые классы
# --------------------------------------------------------------------------
class Rect(object):
    """Прямоугольник в стиле pgzero.Actor (x, y — центр)."""

    def __init__(self, canvas, x=0, y=0, w=40, h=40):
        self.canvas = canvas
        self._x = float(x)
        self._y = float(y)
        self.w = float(w)
        self.h = float(h)

    # координаты -----------------------------------------------------
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, v):
        self._x = float(v)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, v):
        self._y = float(v)

    @property
    def pos(self):
        return (self._x, self._y)

    @pos.setter
    def pos(self, pair):
        self._x, self._y = float(pair[0]), float(pair[1])

    left = property(lambda s: s._x - s.w / 2,
                    lambda s, v: setattr(s, "_x", v + s.w / 2))
    right = property(lambda s: s._x + s.w / 2,
                     lambda s, v: setattr(s, "_x", v - s.w / 2))
    top = property(lambda s: s._y - s.h / 2,
                   lambda s, v: setattr(s, "_y", v + s.h / 2))
    bottom = property(lambda s: s._y + s.h / 2,
                      lambda s, v: setattr(s, "_y", v - s.h / 2))
    center = property(lambda s: s.pos, lambda s, v: setattr(s, "pos", v))

    # столкновения ----------------------------------------------------
    def colliderect(self, other):
        """Пересечение двух прямоугольников (как в pgzero)."""
        if isinstance(other, (tuple, list)):
            ox, oy, ow, oh = other
        else:
            ox, oy, ow, oh = other.x, other.y, other.w, other.h
        return (abs(self._x - ox) * 2 < (self.w + ow) and
                abs(self._y - oy) * 2 < (self.h + oh))

    def collidespoint(self, point):
        px, py = point
        return (abs(px - self._x) * 2 <= self.w and
                abs(py - self._y) * 2 <= self.h)

    def distance_to(self, other):
        return math.hypot(self._x - other.x, self._y - other.y)

    def clamp_to_screen(self):
        sw, sh = self.canvas.screen["width"], self.canvas.screen["height"]
        self._x = max(self.w / 2, min(sw - self.w / 2, self._x))
        self._y = max(self.h / 2, min(sh - self.h / 2, self._y))

    def move(self, dx, dy):
        self._x += dx
        self._y += dy

    def move_ip(self, dx, dy):
        self.move(dx, dy)


class Actor(Rect):
    """Объект-персонаж в стиле PgZero: Actor(x, y, w, h).

    Поддерживает ``.move/.colliderect()/.draw_self()``, атрибуты ``angle``,
    ``speed``, свойства направления из pgzero (top/middle/bottom/left/right).
    """

    def __init__(self, canvas, x=0, y=0, w=40, h=40, image=None,
                 color=GREEN, icon=u"🙂"):
        super().__init__(canvas, x, y, w, h)
        self.image = image
        self.color = color
        self.icon = icon
        self.angle = 0.0
        self.speed = 0.0
        self.visible = True
        self.text_label = ""

    # движение под углом (pgzero-style) --------------------------------
    def turn(self, degrees):
        self.angle += degrees

    def forward(self, pixels):
        rad = math.radians(self.angle)
        self._x += pixels * math.sin(rad)
        self._y -= pixels * math.cos(rad)

    def update_physics(self, dt):
        if self.speed:
            self.forward(self.speed * dt)

    # отрисовка ----------------------------------------------------------
    def draw_self(self):
        c = self.canvas
        if not self.visible:
            return
        if self.w <= 0 or self.h <= 0:
            return
        x0, y0 = self._x - self.w / 2, self._y - self.h / 2
        x1, y1 = self._x + self.w / 2, self._y + self.h / 2
        c.create_rectangle(x0, y0, x1, y1, fill=self.color,
                           outline="#ffffff", width=1, tags="actor")
        fs = max(7, int(min(self.w, self.h) * 0.55))
        c.create_text(self._x, self._y, text=self.icon,
                      font=("Courier", fs), tags="actor")
        if self.text_label:
            c.create_text(self._x, y0 - 8, text=self.text_label,
                          fill=YELLOW, font=("Courier", 9, "bold"),
                          tags="actor")


class Keyboard(object):
    """Клавиатура в стиле pgzero: keyboard.left, keyboard.space…"""

    KEYS = ("up", "down", "left", "right", "space", "enter", "escape", "shift",
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
            "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
            "1", "2", "3", "4", "5")

    def __init__(self):
        for k in self.KEYS:
            setattr(self, k, False)

    def press(self, key):
        if hasattr(self, key):
            setattr(self, key, True)

    def release(self, key):
        if hasattr(self, key):
            setattr(self, key, False)

    def reset(self):
        for k in self.KEYS:
            setattr(self, k, False)

    def pressed_keys(self):
        return tuple(k for k in self.KEYS if getattr(self, k, False))


#: Соответствие клавиш Tk -> атрибутов Keyboard
KEYMAP = {
    "Up": "up", "Down": "down", "Left": "left", "Right": "right",
    "space": "space", "Return": "enter", "Escape": "escape",
    "Shift_L": "shift", "Shift_R": "shift",
}


def bind_keyboard(canvas, keyboard):
    """Подключить клавиши к объекту Keyboard эмулятора."""
    def _norm(event):
        k = event.keysym
        if k in KEYMAP:
            return KEYMAP[k]
        low = k.lower()
        if len(low) == 1 and (low.isalnum()):
            return low
        return None

    def _press(event):
        key = _norm(event)
        if key:
            keyboard.press(key)
            return "break"

    def _release(event):
        key = _norm(event)
        if key:
            keyboard.release(key)
            return "break"

    canvas.bind("<KeyPress>", _press)
    canvas.bind("<KeyRelease>", _release)
    canvas.focus_set()
    return canvas


def draw_text(canvas, x, y, text, color=FG, size=12, bold=True):
    return canvas.create_text(x, y, text=text, fill=color,
                              font=("Courier", size, "bold" if bold else ""))
