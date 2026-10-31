# -*- coding: utf-8 -*-
"""levels — уроки КТП (34 уровня по 45 минут) для 7 класса.

* :mod:`levels.base_level`   — контракт уровня из 5 этапов урока;
* :mod:`levels.ktp_registry` — данные КТП всех 34 уроков;
* :mod:`levels.level_loader` — динамический загрузчик уровней 1–34.
"""

from levels.base_level import BaseLevel, STAGE_NAMES, grade_from_percent  # noqa: F401
from levels.level_loader import load_level, load_all                      # noqa: F401

__all__ = ["BaseLevel", "STAGE_NAMES", "grade_from_percent",
           "load_level", "load_all"]
