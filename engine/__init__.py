# -*- coding: utf-8 -*-
"""engine — ядро игры «Проект "Нова-Терра": Код Колонизации».

Модули пакета (только стандартная библиотека Python 3.8+):

* :mod:`engine.state_manager` — профиль и сохранения (``saves/save_profile.json``);
* :mod:`engine.sandbox`       — безопасный запуск кода ученика ``CodeSandbox``;
* :mod:`engine.canvas_sim`    — визуальный виджет ``SimCanvas`` (блок-схемы,
  память, PgZero-эмулятор);
* :mod:`engine.app_window`    — главное окно Tkinter 1150x750 (тема GitHub Dark).
"""

__version__ = "1.0.0"
__all__ = ["__version__"]
