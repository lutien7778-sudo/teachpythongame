# -*- coding: utf-8 -*-
"""module2 — Модуль 2 КТП 7 класса: «Циклы и структуры данных» (уроки 9–12).

Специализированные классы уровней переопределяют методы ``BaseLevel``:
дают уроку уникальную блок-схему, интерактивный симулятор, собственные
задачи с автопроверкой и босс-миссию. Загрузчик ``levels.level_loader``
подхватывает эти классы раньше, чем сборку уровня из ``ktp_registry``.
"""

from levels.module2.level_09 import Level09  # noqa: F401
from levels.module2.level_10 import Level10  # noqa: F401
from levels.module2.level_11 import Level11  # noqa: F401
from levels.module2.level_12 import Level12  # noqa: F401

__all__ = ["Level09", "Level10", "Level11", "Level12"]
