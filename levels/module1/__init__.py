# -*- coding: utf-8 -*-
"""module1 — Модуль 1 КТП 7 класса: «Основы алгоритмики и данные базы» (уроки 1–4).

Специализированные классы уровней переопределяют методы ``BaseLevel``:
дают уроку уникальную блок-схему, интерактивный симулятор, собственные
задачи с автопроверкой и босс-миссию. Загрузчик ``levels.level_loader``
подхватывает эти классы раньше, чем сборку уровня из ``ktp_registry``.
"""

from levels.module1.level_01 import Level01  # noqa: F401
from levels.module1.level_02 import Level02  # noqa: F401
from levels.module1.level_03 import Level03  # noqa: F401
from levels.module1.level_04 import Level04  # noqa: F401

__all__ = ["Level01", "Level02", "Level03", "Level04"]
