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


#: Корень папки levels/ (здесь лежат module1 … module6 и level_XX.py).
_HERE = os.path.dirname(os.path.abspath(__file__))

#: Кэш уже загруженных уровней: {номер: экземпляр}.
_CACHE = {}


def _candidate_paths(number):
    """Все пути, где может лежать файл уровня ``number``.

    Порядок поиска:
      1. levels/moduleN/level_XX.py — уроки, отсортированные по модулям КТП;
      2. levels/level_XX.py         — исторический плоский формат.
    """
    name = "level_%02d.py" % number
    paths = [os.path.join(_HERE, "module%d" % m, name) for m in range(1, 7)]
    paths.append(os.path.join(_HERE, name))
    return paths


def _module_path(number):
    """Первый существующий путь к файлу уровня (или None)."""
    for p in _candidate_paths(number):
        if os.path.isfile(p):
            return p
    return None


def _instantiate_from_file(path, number):
    """Загрузить файл уровня и вернуть экземпляр его BaseLevel-класса."""
    fname = os.path.splitext(os.path.basename(path))[0]           # level_05
    parent = os.path.basename(os.path.dirname(path))              # module1 / levels
    mod_name = "levels.%s.%s" % (parent, fname) if parent != "levels" \
        else "levels.%s" % fname
    spec = importlib.util.spec_from_file_location(mod_name, path)
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
    return None


def load_level(number):
    """Вернуть экземпляр уровня ``number`` (1..34). При некорректном номере — None."""
    number = int(number)
    if not (1 <= number <= TOTAL_LEVELS):
        return None
    if number in _CACHE:
        return _CACHE[number]
    # 1) специализированный файл уровня (levels/moduleN/level_XX.py или levels/level_XX.py)
    path = _module_path(number)
    if path is not None:
        try:
            obj = _instantiate_from_file(path, number)
            if obj is not None:
                _CACHE[number] = obj
                return obj
        except Exception:               # noqa: BLE001
            traceback.print_exc()
    # 2) описание из реестра КТП
    if ktp_registry is not None:
        try:
            desc = ktp_registry.get_level_description(number)
        except Exception:               # noqa: BLE001
            traceback.print_exc()
            desc = None
        if desc:
            obj = BaseLevel(desc)
            obj.number = number
            _CACHE[number] = obj
            return obj
    # 3) заглушка — игра никогда не «падает» на missing-уроке
    obj = FallbackLevel(number)
    _CACHE[number] = obj
    return obj


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
