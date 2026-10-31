# -*- coding: utf-8 -*-
"""level_loader.py — динамический загрузчик уровней 1–34.

Порядок поиска уровня (по номеру):

1. Внешний файл ``levels/level_XX.py`` (например ``level_07.py``) —
   если он содержит класс-наследник ``BaseLevel``, он используется как есть
   (позволяет авторам давать урокам уникальную босс-механику);
2. Иначе уровень собирается из словаря-описания ``levels/ktp_registry.py``
   (строгое соответствие КТП 7 класса);
3. Иначе — заглушка, чтобы игра никогда не «падала» на missing-уроке.

Все импорты защищены ``importlib`` + ``traceback`` и пишутся в консоль игры.
"""

import importlib
import importlib.util
import os
import sys
import traceback

from levels.base_level import BaseLevel

try:
    from levels import ktp_registry
except Exception:                       # реестр обязателен, но защищаемся
    ktp_registry = None
    traceback.print_exc()

TOTAL_LEVELS = 34


class FallbackLevel(BaseLevel):
    """Заглушка для уровня без описания."""

    def __init__(self, number):
        BaseLevel.__init__(self, {
            "number": number,
            "title": u"Сектор %d (описание готовится)" % number,
            "theme": u"Резервный модуль базы",
            "goal": u"Миссия недоступна: обнови реестр КТП.",
            "briefing": u"Датчики сектора молчат. Инженер переходит к "
                        u"резервному протоколу: изучи print() и сохрани игру.",
            "flowchart": {"nodes": [
                {"id": "s", "kind": "start", "text": u"Старт"},
                {"id": "p", "kind": "process", "text": "print('Резерв')"},
                {"id": "e", "kind": "end", "text": u"Конец"}],
                "edges": [("s", "p"), ("p", "e")]},
            "simulator": {"mode": "memory",
                          "variables": {"сектор": number}},
            "tasks": [{"prompt": u"Выведи слово Резерв",
                       "starter": "", "expect_print": [u"Резерв"]}] * 1,
            "boss": {"title": u"Резервная миссия", "mode": "console",
                     "desc": u"Напечатай 'РЕЗЕРВ'.",
                     "expect_print": [u"РЕЗЕРВ"]},
            "quiz": [{"q": u"print нужен для:",
                      "options": [u"вывода", u"удаления", u"рисования",
                                  u"сна"], "answer": 0}],
        })


def _module_path(number):
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "level_%02d.py" % number)


def load_level(number):
    """Вернуть экземпляр уровня ``number`` (1..34). При некорректном номере — None."""
    number = int(number)
    if not (1 <= number <= TOTAL_LEVELS):
        return None
    # 1) внешний специализированный модуль level_XX.py
    path = _module_path(number)
    if os.path.isfile(path):
        try:
            spec = importlib.util.spec_from_file_location(
                "levels.level_%02d" % number, path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)
            for attr in vars(module).values():
                if (isinstance(attr, type) and issubclass(attr, BaseLevel)
                        and attr is not BaseLevel
                        and getattr(attr, "LEVEL_NUMBER", number) == number):
                    obj = attr()
                    if isinstance(obj, BaseLevel):
                        obj.number = number
                        return obj
        except Exception:               # noqa: BLE001
            traceback.print_exc()
    # 2) описание из реестра КТП
    if ktp_registry is not None:
        desc = ktp_registry.get_level_description(number)
        if desc:
            return BaseLevel(desc)
    # 3) заглушка
    return FallbackLevel(number)


def load_all():
    """Словарь {номер: экземпляр} для карты уровней."""
    return {n: load_level(n) for n in range(1, TOTAL_LEVELS + 1)}


def level_titles():
    """[(номер, название)] по всему КТП — для карты уровней."""
    out = []
    for n in range(1, TOTAL_LEVELS + 1):
        lv = load_level(n)
        out.append((n, lv.title if lv else u"—"))
    return out
