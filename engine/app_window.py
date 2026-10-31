# -*- coding: utf-8 -*-
"""app_window.py — главное окно игры «Проект "Нова-Терра": Код Колонизации».

Tkinter, 1150x750, тема GitHub Dark (#0d1117):

* **верхний HUD** — ресурсы базы (энергия/кислород/щиты/металл), имя инженера,
  XP, кнопки «Сохранить», «Загрузить», «Новая игра»;
* **левая панель** — выбор уровня и 5 вкладок этапов 45-минутного урока
  (Брифинг+Схема / Симулятор / Практика из 3 задач / Босс-миссия / Тест);
* **правая панель** — редактор кода ученика (Tab = 4 пробела) и консоль Shell
  с перехватом print() песочницы.

Только стандартная библиотека Python 3.8+.
"""

import tkinter as tk
from tkinter import ttk, font as tkfont, messagebox

from engine.state_manager import StateManager, TOTAL_LEVELS
from engine.sandbox import CodeSandbox
from engine.canvas_sim import SimCanvas, bind_keyboard, BG, PANEL, BORDER, \
    FG, ACCENT, GREEN, RED, YELLOW, PURPLE
from levels.base_level import STAGE_NAMES, STAGE_MINUTES, BaseLevel
from levels.level_loader import load_level

APP_TITLE = u"Проект «Нова-Терра»: Код Колонизации — Python, 7 класс"
WIN_W, WIN_H = 1150, 750


class CodeEditor(tk.Text):
    """Редактор кода: Tab = 4 пробела, блочный отступ, счётчик строк."""

    def __init__(self, master=None, **kw):
        kw.setdefault("bg", "#010409")
        kw.setdefault("fg", "#e6edf3")
        kw.setdefault("insertbackground", ACCENT)
        kw.setdefault("font", ("Courier", 11))
        kw.setdefault("wrap", "none")
        kw.setdefault("undo", True)
        kw.setdefault("tabspacing", 4)
        super().__init__(master, **kw)
        self.bind("<KeyRelease>", self._refresh_linebar)
        self.linebar = None

    def set_linebar(self, bar):
        self.linebar = bar
        self._refresh_linebar()

    def _refresh_linebar(self, event=None):
        if self.linebar is not None:
            lines = int(self.index("end-1c").split(".")[0])
            self.linebar.config(text="строк: %d" % lines)
        return None

    @staticmethod
    def handle_tab(event):
        widget = event.widget
        sel = widget.tag_ranges("sel")
        if sel:                                   # выделение — блок целиком
            first_line = int(str(sel[0]).split(".")[0])
            last_line = int(str(sel[1]).split(".")[0])
            for ln in range(first_line, last_line + 1):
                widget.insert("%d.0" % ln, "    ")
            widget.tag_remove("sel", "1.0", "end")
            widget.tag_add("sel", "%d.0" % first_line,
                           "%d.end" % (last_line + 1))
            return "break"
        widget.insert("insert", "    ")
        return "break"


class NovaTerraApp(object):
    """Главное окно приложения."""

    def __init__(self, root):
        self.root = root
        root.title(APP_TITLE)
        root.geometry("%dx%d" % (WIN_W, WIN_H))
        root.minsize(980, 620)
        root.configure(bg=BG)

        self.state = StateManager()
        self.state.load()
        self.level = None                 # текущий экземпляр BaseLevel
        self.task_index = 0               # активная задача практики (0..2)
        self.tasks_ok = set()             # решённые задачи текущего урока
        self.quiz_vars = []               # tk.IntVar теста
        self.boss_scene = None
        self.editor_bufs = {}             # черновики кода по номеру задачи

        self._setup_theme()
        self._build_hud()
        self._build_left_panel()
        self._build_right_panel()
        self.sandbox = CodeSandbox(output_callback=self.shell_write)
        # объект арены доступен в коде ученика (уроки 17–34)
        self.sandbox.inject(canvas=self.sim)

        self._ask_name_if_empty()
        self.open_level(min(self.state.current_level,
                            self.state.unlocked_level))
        self.shell_write(u"СИСТЕМА НОВА-ТЕРРА ONLINE. Добро пожаловать, "
                         u"инженер!", "sys")
        self.shell_write(u"Хронометраж урока 45 мин: " + u" | ".join(
            u"%s — %d мин" % (n.split(". ")[1], m)
            for n, m in zip(STAGE_NAMES, STAGE_MINUTES)))

    # ------------------------------------------------------------- тема
    def _setup_theme(self):
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure(".", background=BG, foreground=FG,
                        fieldbackground=PANEL, bordercolor=BORDER,
                        lightcolor=PANEL, darkcolor=PANEL)
        style.configure("TNotebook", background=BG, borderwidth=0)
        style.configure("TNotebook.Tab", background=PANEL,
                        foreground="#8b949e", padding=(8, 5),
                        font=("Courier", 9, "bold"))
        style.map("TNotebook.Tab",
                  background=[("selected", "#1f6feb")],
                  foreground=[("selected", "#ffffff")])
        style.configure("TFrame", background=BG)
        style.configure("TLabel", background=BG, foreground=FG)
        style.configure("TButton", background=PANEL, foreground=FG,
                        bordercolor=BORDER, focusthickness=1,
                        font=("Courier", 9, "bold"), padding=5)
        style.map("TButton",
                  background=[("active", "#21262d"), ("pressed", "#30363d")],
                  foreground=[("disabled", "#484f58")])
        style.configure("Vertical.TScrollbar", background=PANEL,
                        troughcolor=BG, arrowcolor=FG)
        style.configure("TCombobox", fieldbackground=PANEL, background=PANEL,
                        foreground=FG, arrowcolor=FG)
        style.configure("TRadiobutton", background=BG, foreground=FG)
        self.ui_font = tkfont.Font(family="Courier", size=10)
        self.hud_font = tkfont.Font(family="Courier", size=10, weight="bold")

    # -------------------------------------------------------------- HUD
    def _build_hud(self):
        hud = tk.Frame(self.root, bg=PANEL, height=58)
        hud.pack(side="top", fill="x")
        hud.pack_propagate(False)
        self.hud_label = tk.Label(hud, text="", bg=PANEL, fg=FG,
                                  font=self.hud_font, anchor="w")
        self.hud_label.pack(side="left", padx=12, pady=6)
        btns = tk.Frame(hud, bg=PANEL)
        btns.pack(side="right", padx=8)
        ttk.Button(btns, text=u"Сохранить", command=self.save_game)\
            .pack(side="left", padx=3)
        ttk.Button(btns, text=u"Загрузить", command=self.load_game)\
            .pack(side="left", padx=3)
        ttk.Button(btns, text=u"Новая игра", command=self.new_game)\
            .pack(side="left", padx=3)
        self.refresh_hud()

    def refresh_hud(self):
        self.hud_label.config(text=self.state.hud_text())

    # ------------------------------------------------------ левая панель
    def _build_left_panel(self):
        left = tk.Frame(self.root, bg=BG, width=600)
        left.pack(side="left", fill="both", expand=False, padx=(8, 4), pady=8)
        left.pack_propagate(False)

        top_row = tk.Frame(left, bg=BG)
        top_row.pack(fill="x")
        self.level_combo = ttk.Combobox(
            top_row, values=[u"Уровень %d" % i for i in
                             range(1, TOTAL_LEVELS + 1)],
            state="readonly", width=14, font=self.ui_font)
        self.level_combo.pack(side="left", padx=4, pady=4)
        self.level_combo.bind("<<ComboboxSelected>>",
                              lambda e: self.on_pick_level())
        ttk.Button(top_row, text=u"Открыть ▶",
                   command=self.on_pick_level).pack(side="left", padx=4)
        self.stage_status = tk.Label(left, text="", bg=BG, fg=YELLOW,
                                     font=self.ui_font, anchor="w",
                                     justify="left")
        self.stage_status.pack(fill="x", padx=6)

        self.notebook = ttk.Notebook(left)
        self.notebook.pack(fill="both", expand=True, padx=4, pady=4)
        tab_frames = []
        for name in STAGE_NAMES:
            f = tk.Frame(self.notebook, bg=BG)
            self.notebook.add(f, text=name)
            tab_frames.append(f)
        self.tab_brief, self.tab_sim, self.tab_practice, \
            self.tab_boss, self.tab_quiz = tab_frames

        # ---- этап 1: брифинг + схема
        self.brief_text = tk.Text(self.tab_brief, bg=PANEL, fg=FG,
                                  wrap="word", font=self.ui_font,
                                  relief="flat", height=7, padx=8, pady=6)
        self.brief_text.pack(fill="x", padx=4, pady=(4, 2))
        bbar = tk.Frame(self.tab_brief, bg=BG)
        bbar.pack(fill="x", padx=4)
        ttk.Button(bbar, text=u"Этап пройден",
                   command=lambda: self.complete_stage(0)).pack(side="right",
                                                                padx=4)
        self.brief_canvas_host = tk.Frame(self.tab_brief, bg=BG)
        self.brief_canvas_host.pack(fill="both", expand=True, padx=4, pady=4)

        # ---- этап 2: симулятор
        self.sim_host = tk.Frame(self.tab_sim, bg=BG)
        self.sim_host.pack(fill="both", expand=True, padx=4, pady=4)
        sim_bar = tk.Frame(self.tab_sim, bg=BG)
        sim_bar.pack(fill="x", padx=4, pady=2)
        ttk.Button(sim_bar, text=u"Обновить симуляцию",
                   command=self.render_simulator).pack(side="left", padx=4)
        ttk.Button(sim_bar, text=u"Этап пройден",
                   command=lambda: self.complete_stage(1)).pack(side="right",
                                                                padx=4)

        # ---- этап 3: практика
        prac_head = tk.Frame(self.tab_practice, bg=BG)
        prac_head.pack(fill="x", padx=4, pady=2)
        self.task_label = tk.Label(prac_head, text="", bg=BG, fg=GREEN,
                                   wraplength=560, justify="left",
                                   font=self.ui_font)
        self.task_label.pack(side="left", fill="x", expand=True)
        self.task_nav = tk.Frame(self.tab_practice, bg=BG)
        self.task_nav.pack(fill="x", padx=4)
        self.task_buttons = []
        for i in range(3):
            b = ttk.Button(self.task_nav, text=u"Задача %d" % (i + 1),
                           command=lambda k=i: self.select_task(k))
            b.pack(side="left", padx=3, pady=2)
            self.task_buttons.append(b)
        ttk.Button(self.task_nav, text=u"Проверить задачу",
                   command=self.check_current_task).pack(side="right", padx=4)
        self.practice_canvas_host = tk.Frame(self.tab_practice, bg=BG,
                                             height=150)
        self.practice_canvas_host.pack(fill="x", padx=4)

        # ---- этап 4: босс
        boss_bar = tk.Frame(self.tab_boss, bg=BG)
        boss_bar.pack(fill="x", padx=4, pady=2)
        self.boss_desc = tk.Label(boss_bar, text="", bg=BG, fg=RED,
                                  wraplength=560, justify="left",
                                  font=self.ui_font)
        self.boss_desc.pack(anchor="w")
        ctl = tk.Frame(self.tab_boss, bg=BG)
        ctl.pack(fill="x", padx=4)
        ttk.Button(ctl, text=u"Старт миссии",
                   command=self.start_boss_mission).pack(side="left", padx=4)
        ttk.Button(ctl, text=u"Стоп",
                   command=self.stop_boss_mission).pack(side="left", padx=4)
        ttk.Button(ctl, text=u"Миссия выполнена",
                   command=lambda: self.complete_stage(3)).pack(side="right",
                                                                padx=4)
        self.boss_host = tk.Frame(self.tab_boss, bg=BG)
        self.boss_host.pack(fill="both", expand=True, padx=4, pady=4)

        # ---- этап 5: тест
        quiz_scroll_wrap = tk.Frame(self.tab_quiz, bg=BG)
        quiz_scroll_wrap.pack(fill="both", expand=True)
        self.quiz_canvas = tk.Canvas(quiz_scroll_wrap, bg=BG,
                                     highlightthickness=0)
        qbar = ttk.Scrollbar(quiz_scroll_wrap, orient="vertical",
                             command=self.quiz_canvas.yview)
        self.quiz_inner = tk.Frame(self.quiz_canvas, bg=BG)
        self.quiz_inner.bind(
            "<Configure>",
            lambda e: self.quiz_canvas.configure(
                scrollregion=self.quiz_canvas.bbox("all")))
        self._quiz_window = self.quiz_canvas.create_window(
            (0, 0), window=self.quiz_inner, anchor="nw")
        self.quiz_canvas.configure(yscrollcommand=qbar.set)
        self.quiz_canvas.bind(
            "<Configure>",
            lambda e: self.quiz_canvas.itemconfigure(self._quiz_window,
                                                     width=e.width))
        self.quiz_canvas.pack(side="left", fill="both", expand=True)
        qbar.pack(side="right", fill="y")
        quiz_bottom = tk.Frame(self.tab_quiz, bg=BG)
        quiz_bottom.pack(fill="x", padx=4, pady=4)
        ttk.Button(quiz_bottom, text=u"Оценить тест",
                   command=self.submit_quiz).pack(side="left", padx=4)
        self.quiz_result = tk.Label(quiz_bottom, text="", bg=BG, fg=YELLOW,
                                    font=self.ui_font)
        self.quiz_result.pack(side="left", padx=8)

        # холсты: симулятор (этапы 1–2), мини-шпаргалка (этап 3), арена (4)
        self.sim = SimCanvas(self.sim_host, width=560, height=330)
        self.flow = SimCanvas(self.brief_canvas_host, width=560, height=230)
        self.mini = SimCanvas(self.practice_canvas_host, width=560, height=140)
        self.boss = SimCanvas(self.boss_host, width=560, height=300)
        bind_keyboard(self.boss, self.boss.keyboard)

    # ----------------------------------------------------- правая панель
    def _build_right_panel(self):
        right = tk.Frame(self.root, bg=BG, width=520)
        right.pack(side="right", fill="both", expand=True, padx=(4, 8), pady=8)
        right.pack_propagate(False)

        head = tk.Frame(right, bg=BG)
        head.pack(fill="x")
        tk.Label(head, text=u"РЕДАКТОР КОДА ИНЖЕНЕРА", bg=BG, fg=ACCENT,
                 font=("Courier", 10, "bold")).pack(side="left", padx=4)
        self.linebar = tk.Label(head, text="строк: 1", bg=BG, fg="#8b949e",
                                font=("Courier", 9))
        self.linebar.pack(side="right", padx=6)

        ed_frame = tk.Frame(right, bg=BORDER)
        ed_frame.pack(fill="both", expand=True, padx=4, pady=(2, 4))
        self.editor = CodeEditor(ed_frame, height=18)
        escroll = ttk.Scrollbar(ed_frame, orient="vertical",
                                command=self.editor.yview)
        self.editor.configure(yscrollcommand=escroll.set)
        escroll.pack(side="right", fill="y")
        self.editor.pack(side="left", fill="both", expand=True)
        self.editor.set_linebar(self.linebar)
        self.editor.bind("<Tab>", CodeEditor.handle_tab)
        self.editor.bind("<Shift-Tab>", lambda e: self._unindent(e))

        runbar = tk.Frame(right, bg=BG)
        runbar.pack(fill="x", padx=4)
        ttk.Button(runbar, text=u"Запустить (F5)",
                   command=self.run_code).pack(side="left", padx=3)
        ttk.Button(runbar, text=u"Очистить консоль",
                   command=self.clear_shell).pack(side="left", padx=3)
        ttk.Button(runbar, text=u"Подсказка",
                   command=self.show_hint).pack(side="left", padx=3)
        self.root.bind("<F5>", lambda e: self.run_code())

        sh_frame = tk.Frame(right, bg=BORDER)
        sh_frame.pack(fill="both", expand=True, padx=4, pady=(4, 2))
        tk.Label(sh_frame, text=u" Shell — вывод системы базы ",
                 bg=BG, fg=GREEN, font=("Courier", 9, "bold"))\
            .pack(anchor="w", pady=(2, 0))
        self.shell = tk.Text(sh_frame, bg="#010409", fg="#7ee787",
                             font=("Courier", 10), wrap="word", height=10,
                             relief="flat", state="disabled", padx=6, pady=4)
        sscroll = ttk.Scrollbar(sh_frame, orient="vertical",
                                command=self.shell.yview)
        self.shell.configure(yscrollcommand=sscroll.set)
        sscroll.pack(side="right", fill="y")
        self.shell.pack(side="left", fill="both", expand=True)
        self.shell.tag_configure("err", foreground=RED)
        self.shell.tag_configure("ok", foreground=GREEN)
        self.shell.tag_configure("sys", foreground=ACCENT)

        self.statusbar = tk.Label(self.root, text=u"Готов к работе.",
                                  bg=PANEL, fg="#8b949e", anchor="w",
                                  font=("Courier", 9))
        self.statusbar.pack(side="bottom", fill="x")

    def _unindent(self, event):
        w = event.widget
        line = int(w.index("insert").split(".")[0])
        txt = w.get("%d.0" % line, "%d.end" % line)
        if txt.startswith("    "):
            w.delete("%d.0" % line, "%d.4" % line)
        return "break"

    # ------------------------------------------------------------ shell
    def shell_write(self, text, tag=None):
        self.shell.configure(state="normal")
        self.shell.insert("end", str(text) + "\n", (tag,) if tag else ())
        self.shell.configure(state="disabled")
        self.shell.see("end")

    def clear_shell(self):
        self.shell.configure(state="normal")
        self.shell.delete("1.0", "end")
        self.shell.configure(state="disabled")

    def set_status(self, text):
        self.statusbar.config(text=text)

    # ------------------------------------------------------- выбор уровня
    def on_pick_level(self):
        raw = self.level_combo.get()
        try:
            num = int(raw.split()[-1])
        except (ValueError, IndexError):
            return
        if num > self.state.unlocked_level:
            messagebox.showinfo(
                APP_TITLE,
                u"Сектор %d ещё не открыт! Пройди уроки до %d."
                % (num, self.state.unlocked_level))
            self.level_combo.current(self.state.current_level - 1)
            return
        self.open_level(num)

    def open_level(self, number):
        number = max(1, min(TOTAL_LEVELS, int(number)))
        lv = load_level(number)
        if lv is None:
            return
        self.stop_boss_mission(silent=True)
        self.level = lv
        self.state.current_level = number
        self.level_combo.current(number - 1)
        self.task_index = 0
        self.tasks_ok = set()
        self.editor_bufs = {}
        self._fill_briefing()
        self.render_simulator()
        self.select_task(0)
        self._fill_boss_tab()
        self._fill_quiz()
        self._update_stage_status()
        self.shell_write(u"— УРОВЕНЬ %d: %s —" % (number, lv.title), "sys")
        self.set_status(u"Уровень %d из 34 | Тема КТП: %s"
                        % (number, lv.theme))

    # ---------------------------------------------------- этап 1: брифинг
    def _fill_briefing(self):
        lv = self.level
        self.brief_text.configure(state="normal")
        self.brief_text.delete("1.0", "end")
        self.brief_text.insert(
            "end",
            u"УРОК %d. %s\nТема КТП: %s\nЦель: %s\n\n%s\n"
            % (lv.number, lv.title, lv.theme, lv.goal, lv.briefing))
        self.brief_text.configure(state="disabled")
        nodes, edges = lv.get_flowchart()
        if nodes:
            self.flow.show_flowchart(nodes, edges,
                                     u"Блок-схема: %s" % lv.title)
        else:
            self.flow.show_memory(variables={"цель": lv.goal},
                                  title=u"Память брифинга")

    # -------------------------------------------------- этап 2: симулятор
    def render_simulator(self):
        spec = self.level.get_simulator_spec() or {}
        mode = spec.get("mode", "memory")
        if mode == "pgzero":
            self.sim.show_memory(
                variables={"режим": "PgZero-арена",
                           "actor.pos": tuple(round(v, 1)
                                              for v in self.sim.actor.pos)},
                lists={"количество стен": len(self.sim.walls)}
                if isinstance(self.sim.walls, list) else None,
                title=u"Конфиг арены (запусти босс-миссию)")
        else:
            self.sim.show_memory(
                variables=spec.get("variables"),
                lists=spec.get("lists"),
                matrices=spec.get("matrices"),
                title=u"Симулятор: память модуля «%s»" % self.level.title)

    # --------------------------------------------------- этап 3: практика
    def select_task(self, index):
        index = max(0, min(2, int(index)))
        self.editor_bufs[self.task_index] = self.current_editor_code()
        self.task_index = index
        task = self.level.get_task(index)
        if task is None:
            self.task_label.config(
                text=u"Задачи сектора готовятся (зарезервировано место).")
            return
        saved = self.editor_bufs.get(index)
        code = saved if saved is not None else task.get("starter", "")
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", code or "")
        self.task_label.config(
            text=u"Задача %d из 3: %s" % (index + 1, task.get("prompt", "")))
        hint = task.get("hint")
        if hint:
            self.mini.show_memory(
                variables={"подсказка": hint},
                title=u"Шпаргалка к задаче %d" % (index + 1))
        else:
            self.mini.show_memory(
                variables={
                    "ожидается в выводе": str(task.get("expect_print", [])),
                    "переменные для проверки":
                        str(list((task.get("expect_vars") or {}).keys())),
                },
                title=u"Чек-лист автопроверки задачи %d" % (index + 1))

    def current_editor_code(self):
        return self.editor.get("1.0", "end-1c")

    def run_code(self):
        code = self.current_editor_code()
        self.editor_bufs[self.task_index] = code
        self.shell_write(u"$ запуск программы…", "sys")
        ok = self.sandbox.run(code)
        if ok:
            self.shell_write(u"[ОК] Программа завершилась без ошибок.", "ok")
        return ok

    def check_current_task(self):
        task = self.level.get_task(self.task_index)
        code = self.current_editor_code()
        self.editor_bufs[self.task_index] = code
        ok, feedback = BaseLevel.check_task(task, self.sandbox, code)
        self.shell_write(feedback, "ok" if ok else "err")
        if ok:
            self.state.add_xp(10)
            self.state.add_resource("metal", 5)
            self.state.log_event(u"Ур.%d задача %d решена"
                                 % (self.level.number, self.task_index + 1))
            self.tasks_ok.add(self.task_index)
            self.task_buttons[self.task_index].config(
                text=u"✔ Задача %d" % (self.task_index + 1))
            self.refresh_hud()
            if len(self.tasks_ok) >= 3:
                self.complete_stage(2, quiet=True)
        return ok

    def show_hint(self):
        task = self.level.get_task(self.task_index) or {}
        hint = task.get("hint") or task.get("starter") or \
            u"Разбери задачу на шаги и начни с print()"
        self.shell_write(u"ПОДСКАЗКА: " + str(hint), "sys")

    # ------------------------------------------------------ этап 4: босс
    def _fill_boss_tab(self):
        spec = self.level.get_boss_spec() or {}
        self.boss_desc.config(text=u"БОСС СЕКТОРА: %s — %s" % (
            spec.get("title", u"сектор"), spec.get("desc", "")))

    def start_boss_mission(self):
        spec = self.level.get_boss_spec() or {}
        mode = spec.get("mode", "console")
        if mode == "pgzero":
            scene = self.level.build_boss_scene(self.boss)
            self.boss_scene = scene
            self.boss.focus_set()
            self.boss.start_game_loop(scene["update"], scene["draw"])
            self.shell_write(u"МИССИЯ ЗАПУЩЕНА: управляй стрелками, "
                             u"доведи модуль до цели!", "sys")
        else:
            code = self.current_editor_code()
            self.shell_write(u"БОСС-МИССИЯ (консоль): проверяю код…", "sys")
            virtual_task = {
                "prompt": spec.get("desc", ""),
                "expect_print": spec.get("expect_print", []),
                "expect_vars": spec.get("expect_vars", {}),
                "forbidden": spec.get("forbidden", []),
            }
            ok, feedback = BaseLevel.check_task(virtual_task, self.sandbox,
                                                code)
            self.shell_write(feedback, "ok" if ok else "err")
            if ok:
                self.complete_stage(3, quiet=True)

    def stop_boss_mission(self, silent=False):
        self.boss.stop_game_loop()
        self.boss.clear_scene()
        self.boss.draw_planet_bg()
        if not silent:
            self.shell_write(u"Миссия остановлена.", "sys")

    # ------------------------------------------------------- этап 5: тест
    def _fill_quiz(self):
        for child in self.quiz_inner.winfo_children():
            child.destroy()
        self.quiz_vars = []
        tk.Label(self.quiz_inner,
                 text=u"Тест: 5 вопросов (5 минут). Верные ответы -> оценка "
                      u"и чекпоинт в профиле.",
                 bg=BG, fg=ACCENT, font=self.ui_font).pack(anchor="w", pady=4)
        for qi, q in enumerate(self.level.get_quiz()):
            frame = tk.Frame(self.quiz_inner, bg=PANEL, padx=8, pady=6)
            frame.pack(fill="x", pady=3, padx=2)
            tk.Label(frame, text=u"%d. %s" % (qi + 1, q.get("q", "")),
                     bg=PANEL, fg=FG, wraplength=520, justify="left",
                     font=self.ui_font).pack(anchor="w")
            var = tk.IntVar(value=-1)
            self.quiz_vars.append(var)
            for oi, opt in enumerate(q.get("options", [])):
                tk.Radiobutton(frame, text=opt, variable=var, value=oi,
                               bg=PANEL, fg="#adbac7", selectcolor=BG,
                               activebackground=PANEL, activeforeground=FG,
                               font=("Courier", 9), anchor="w",
                               wraplength=500, justify="left").pack(
                    anchor="w", fill="x")
        self.quiz_result.config(text="")

    def submit_quiz(self):
        answers = [v.get() if v.get() >= 0 else None for v in self.quiz_vars]
        res = self.level.grade_quiz(answers)
        grade = res["grade"]
        text = (u"Тест: %d/%d (%d%%) -> оценка %d"
                % (res["correct"], res["total"], res["percent"], grade))
        self.quiz_result.config(text=text,
                                fg=GREEN if grade >= 4 else YELLOW)
        self.shell_write(text, "ok" if grade >= 3 else "err")
        if grade >= 3:
            self.complete_stage(4, quiet=True)
            self.finish_level(grade)
        return res

    # --------------------------------------------------------- прогресс
    def complete_stage(self, index, quiet=False):
        if self.level is None:
            return
        self.level.mark_done(index)
        if not quiet:
            self.shell_write(u"Этап «%s» завершён." % STAGE_NAMES[index],
                             "ok")
        self._update_stage_status()

    def finish_level(self, grade=None):
        lv = self.level
        xp = lv.xp_reward
        self.state.add_xp(xp)
        self.state.add_resource("energy", 20)
        self.state.add_resource("oxygen", 10)
        self.state.add_resource("shields", 5)
        if grade is None:
            grade = self.state.get_grade(lv.number) or 4
        self.state.set_grade(lv.number, grade,
                             comment=u"уровень %d пройден" % lv.number)
        if lv.number == self.state.unlocked_level and lv.number < TOTAL_LEVELS:
            self.state.unlocked_level = lv.number + 1
        self.state.save()
        self.refresh_hud()
        self.shell_write(u"УРОВЕНЬ %d ПРОЙДЕН! Оценка %d, +%d XP. "
                         u"Открыт уровень %d."
                         % (lv.number, grade, xp, self.state.unlocked_level),
                         "ok")
        if lv.number == TOTAL_LEVELS:
            self._finale_screen()

    def _finale_screen(self):
        nodes = [
            {"id": "a", "kind": "start", "text": u"Корабль у планеты"},
            {"id": "b", "kind": "condition", "text": u"Все системы готовы?"},
            {"id": "c", "kind": "io", "text": u"ПОСАДКА"},
            {"id": "d", "kind": "process", "text": u"Ждать ремонта"},
            {"id": "e", "kind": "end", "text": u"ГОРОД НОВА-ТЕРРА!"},
        ]
        edges = [("a", "b"), ("b", "c", u"True"), ("b", "d", u"False"),
                 ("c", "e"), ("d", "c")]
        self.flow.show_flowchart(nodes, edges,
                                 u"ФИНАЛ КУРСА: прибытие переселенцев")
        messagebox.showinfo(
            APP_TITLE,
            u"КОРАБЛЬ «ПЕРЕСЕЛЕНЕЦ-1» ПРИЗЕМЛИЛСЯ!\n\n"
            u"34 урока пройдены. Город Нова-Терра принимает жителей.\n"
            u"Средний балл инженера: %s" % self.state.average_grade())

    def _update_stage_status(self):
        if self.level is None:
            return
        marks = []
        for i, name in enumerate(STAGE_NAMES):
            short = name.split(". ")[1]
            marks.append(u"%s%s" % (u"[+]" if self.level.stage_done[i]
                                    else u"[ ]", short))
        self.stage_status.config(
            text=u"ЭТАПЫ УРОКА (%d мин):  %s"
                 % (sum(STAGE_MINUTES), "   ".join(marks)))

    # ------------------------------------------------------- сохранение
    def save_game(self):
        if self.level is not None:
            self.editor_bufs[self.task_index] = self.current_editor_code()
        path = self.state.save()
        self.refresh_hud()
        self.shell_write(u"ПРОГРЕСС СОХРАНЁН: %s" % path, "sys")
        self.set_status(u"Сохранено: " + path)

    def load_game(self):
        if self.state.load():
            self.refresh_hud()
            num = min(self.state.current_level, self.state.unlocked_level)
            self.open_level(num)
            self.shell_write(u"ПРОФИЛЬ ЗАГРУЖЕН. Инженер: %s, открыто "
                             u"уровней: %d"
                             % (self.state.player_name or "?",
                                self.state.unlocked_level), "sys")
        else:
            self.shell_write(u"Файл сохранения не найден — начинай новую "
                             u"экспедицию!", "err")

    def new_game(self):
        if not messagebox.askyesno(APP_TITLE,
                                   u"Начать новую экспедицию? Текущий прогресс "
                                   u"будет очищен."):
            return
        self.state.reset()
        self.state.save()
        self.refresh_hud()
        self.open_level(1)
        self.shell_write(u"НОВАЯ ЭКСПЕДИЦИЯ НАЧАТА. Удачи, инженер!", "sys")

    # ------------------------------------------------------------- имя
    def _ask_name_if_empty(self):
        if self.state.player_name:
            return
        dlg = tk.Toplevel(self.root)
        dlg.title(u"Регистрация инженера")
        dlg.geometry("380x170")
        dlg.configure(bg=PANEL)
        dlg.resizable(False, False)
        dlg.transient(self.root)
        tk.Label(dlg, text=u"Проект «НОВА-ТЕРРА»\nКак тебя записать в журнал "
                           u"экспедиции?", bg=PANEL, fg=FG,
                 font=("Courier", 10, "bold")).pack(pady=(12, 6))
        entry = tk.Entry(dlg, bg=BG, fg=GREEN, insertbackground=GREEN,
                         font=("Courier", 12), justify="center")
        entry.pack(padx=20, ipady=4)
        entry.focus_force()

        def confirm(event=None):
            name = entry.get().strip() or u"Инженер"
            self.state.player_name = name
            self.state.save()
            self.refresh_hud()
            dlg.destroy()

        entry.bind("<Return>", confirm)
        ttk.Button(dlg, text=u"Начать экспедицию",
                   command=confirm).pack(pady=10)


def run():
    """Создать и запустить главное окно (вызывается из main.py)."""
    root = tk.Tk()
    app = NovaTerraApp(root)
    root.mainloop()
    return app
