# -*- coding: utf-8 -*-
"""module3 — Модуль 3 КТП 7 класса: «Переход в 2D: графика, физика и события»
(уроки 17–21).

Все уровни модуля работают со встроенным эмулятором ``PgZero`` из
``engine.canvas_sim`` (режим В): объекты ``Actor(x, y, w, h)``, метод
``.colliderect()``, функции ``update()`` / ``draw()`` и объект ``keyboard`` —
на чистом ``tkinter.Canvas``, без сторонних библиотек.

Специализированные классы уровней переопределяют методы ``BaseLevel``:
дают уроку уникальную блок-схему, живой PgZero-симулятор, собственные задачи
с автопроверкой и босс-миссию с кастомной механикой ``build_boss_scene``.
Загрузчик ``levels.level_loader`` подхватывает эти классы раньше сборки
уровня из ``ktp_registry``.
"""

from levels.module3.level_17 import Level17  # noqa: F401
from levels.module3.level_18 import Level18  # noqa: F401
from levels.module3.level_19 import Level19  # noqa: F401
from levels.module3.level_20 import Level20  # noqa: F401
from levels.module3.level_21 import Level21  # noqa: F401

__all__ = ["Level17", "Level18", "Level19", "Level20", "Level21"]
