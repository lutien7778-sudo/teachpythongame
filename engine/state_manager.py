# -*- coding: utf-8 -*-
"""state_manager.py — персистентное состояние игры «Проект "Нова-Терра"».

Сохраняет прогресс ученика в ``saves/save_profile.json``:

* имя ученика;
* открытый уровень (1..34);
* ресурсы базы: энергия, кислород, щиты, металл;
* XP (очки опыта);
* оценки за уроки (5-балльная шкала) и авто-чекпоинты.

Все операции атомарны: запись идёт во временный файл, затем ``os.replace()`` —
профиль не испортится даже при внезапном закрытии Thonny.
"""

import json
import os
import sys
import time

TOTAL_LEVELS = 34
MAX_CHECKPOINTS = 20
MAX_EVENTS = 20

#: Стартовые ресурсы новой экспедиции.
DEFAULT_RESOURCES = {
    "energy": 100,      # энергия, кВт·ч
    "oxygen": 100,      # кислород, % запаса генератора
    "shields": 100,     # щиты, % целостности купола
    "metal": 50,        # металл, кг запаса конструкции
}

RESOURCE_LABELS_RU = {
    "energy": "Энергия",
    "oxygen": "Кислород",
    "shields": "Щиты",
    "metal": "Металл",
}


def default_save_dir():
    """Каталог ``saves/`` рядом с игрой (работает и из .pyz-архива)."""
    try:
        if getattr(sys, "frozen", False):          # сборка PyInstaller
            base = os.path.dirname(os.path.abspath(sys.executable))
        else:
            here = os.path.abspath(__file__)
            # внутри zipapp __file__ указывает внутрь архива — берём cwd
            if ".zip" in here or ".pyz" in here:
                base = os.getcwd()
            else:
                base = os.path.dirname(os.path.dirname(here))
    except Exception:
        base = os.getcwd()
    return os.path.join(base, "saves")


class StateManager:
    """Единая точка доступа к профилю игрока."""

    def __init__(self, save_dir=None, filename="save_profile.json"):
        self.save_dir = save_dir or default_save_dir()
        self.filename = filename
        self.path = os.path.join(self.save_dir, filename)
        self.data = self._new_profile()
        self.dirty = False

    # ----------------------------------------------------------- профиль
    @staticmethod
    def _new_profile():
        return {
            "player_name": "",
            "unlocked_level": 1,
            "current_level": 1,
            "resources": dict(DEFAULT_RESOURCES),
            "xp": 0,
            "grades": {},            # {"1": 5, "7": 4, ...}
            "checkpoints": [],       # [{"level":1,"grade":5,"time":"..."}]
            "events": [],            # журнал действий
            "play_time_sec": 0,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "version": 1,
        }

    # ------------------------------------------------------- базовые поля
    @property
    def player_name(self):
        return self.data.get("player_name", "")

    @player_name.setter
    def player_name(self, value):
        self.data["player_name"] = str(value).strip()[:40]
        self.dirty = True

    @property
    def unlocked_level(self):
        return int(self.data.get("unlocked_level", 1))

    @unlocked_level.setter
    def unlocked_level(self, value):
        self.data["unlocked_level"] = max(1, min(TOTAL_LEVELS, int(value)))
        self.dirty = True

    @property
    def current_level(self):
        return int(self.data.get("current_level", 1))

    @current_level.setter
    def current_level(self, value):
        self.data["current_level"] = max(1, min(TOTAL_LEVELS, int(value)))
        self.dirty = True

    @property
    def resources(self):
        return self.data.setdefault("resources", dict(DEFAULT_RESOURCES))

    @property
    def xp(self):
        return int(self.data.get("xp", 0))

    # ------------------------------------------------------------ ресурсы
    def add_resource(self, key, amount):
        """Изменить ресурс (можно отрицательным числом), кламп 0..99999."""
        if key not in RESOURCE_LABELS_RU:
            raise KeyError("Неизвестный ресурс: %r" % (key,))
        res = self.resources
        res[key] = max(0, min(99999, int(res.get(key, 0)) + int(amount)))
        self.dirty = True
        return res[key]

    def set_resource(self, key, value):
        if key not in RESOURCE_LABELS_RU:
            raise KeyError("Неизвестный ресурс: %r" % (key,))
        self.resources[key] = max(0, min(99999, int(value)))
        self.dirty = True

    def add_xp(self, amount):
        self.data["xp"] = max(0, int(self.data.get("xp", 0)) + int(amount))
        self.dirty = True
        return self.data["xp"]

    # ------------------------------------------------------------- оценки
    def set_grade(self, level_no, grade, comment=""):
        """Поставить оценку за урок (уровень 1..34, оценка 2..5)."""
        level_no = max(1, min(TOTAL_LEVELS, int(level_no)))
        grade = max(2, min(5, int(grade)))
        self.data.setdefault("grades", {})[str(level_no)] = grade
        self.dirty = True
        self.add_checkpoint(level_no, grade, comment)
        return grade

    def get_grade(self, level_no):
        return self.data.get("grades", {}).get(str(int(level_no)))

    def average_grade(self):
        grades = list(self.data.get("grades", {}).values())
        if not grades:
            return 0.0
        return round(sum(grades) / len(grades), 2)

    # --------------------------------------------------------- чекпоинты
    def add_checkpoint(self, level_no, grade, comment=""):
        """Авто-чекпоинт после пройденного этапа/урока."""
        cps = self.data.setdefault("checkpoints", [])
        cps.append({
            "level": int(level_no),
            "grade": int(grade),
            "comment": str(comment)[:120],
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        })
        if len(cps) > MAX_CHECKPOINTS:
            del cps[:-MAX_CHECKPOINTS]
        self.dirty = True

    def last_checkpoint(self):
        cps = self.data.get("checkpoints", [])
        return cps[-1] if cps else None

    def log_event(self, text):
        events = self.data.setdefault("events", [])
        events.append({"time": time.strftime("%H:%M:%S"), "text": str(text)[:160]})
        if len(events) > MAX_EVENTS:
            del events[:-MAX_EVENTS]
        self.dirty = True

    # -------------------------------------------------------- сохранение
    def save(self):
        """Записать профиль на диск. Возвращает путь к файлу."""
        try:
            os.makedirs(self.save_dir, exist_ok=True)
        except OSError:
            pass
        self.data["updated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
        tmp = self.path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, self.path)
        self.dirty = False
        return self.path

    def load(self):
        """Прочитать профиль с диска. Повреждённый файл -> новый профиль."""
        if not os.path.isfile(self.path):
            self.data = self._new_profile()
            return False
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                raw = json.load(f)
            if not isinstance(raw, dict):
                raise ValueError("profile is not a dict")
        except (ValueError, OSError):
            self.data = self._new_profile()
            return False
        merged = self._new_profile()
        for k, v in raw.items():
            if k == "resources" and isinstance(v, dict):
                res = dict(DEFAULT_RESOURCES)
                for rk, rv in v.items():
                    if rk in res:
                        try:
                            res[rk] = max(0, min(99999, int(rv)))
                        except (TypeError, ValueError):
                            pass
                merged["resources"] = res
            elif k == "player_name":
                merged[k] = str(v)[:40]
            elif k in ("unlocked_level", "current_level", "xp"):
                try:
                    merged[k] = int(v)
                except (TypeError, ValueError):
                    pass
            elif k in ("grades", "checkpoints", "events"):
                if isinstance(v, (dict, list)):
                    merged[k] = v
        merged["unlocked_level"] = max(1, min(TOTAL_LEVELS, merged["unlocked_level"]))
        merged["current_level"] = max(1, min(TOTAL_LEVELS, merged["current_level"]))
        self.data = merged
        self.dirty = False
        return True

    def has_save(self):
        return os.path.isfile(self.path)

    def reset(self):
        """Полный сброс профиля (новая экспедиция)."""
        self.data = self._new_profile()
        self.dirty = True
        return self.path

    # --------------------------------------------------------------- HUD
    def hud_text(self):
        """Строка ресурсов для верхнего HUD главного окна."""
        r = self.resources
        name = self.player_name or "Инженер"
        return (
            u"{name} | Энергия: {e} | Кислород: {o} | Щиты: {s} | "
            u"Металл: {m} | XP: {xp} | Открыто уровней: {lv}/34 | "
            u"Средний балл: {avg}"
        ).format(
            name=name,
            e=r.get("energy", 0),
            o=r.get("oxygen", 0),
            s=r.get("shields", 0),
            m=r.get("metal", 0),
            xp=self.xp,
            lv=self.unlocked_level,
            avg=self.average_grade() or "-",
        )
