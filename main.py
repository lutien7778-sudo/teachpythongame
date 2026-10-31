#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""main.py — точка входа игры «Проект "Нова-Терра": Код Колонизации».

Запуск:
  * Thonny: открыть этот файл и нажать F5;
  * терминал: ``python main.py``;
  * переносимый архив: ``python nova_terra.pyz`` (сборка — см. README.md).

Только стандартная библиотека Python 3.8+ (tkinter, json, os, sys, random,
math, time, ast, traceback). Никаких внешних пакетов.
"""

import os
import sys
import traceback


def _bootstrap():
    """Добавить корень проекта/архива в sys.path (для .pyz и Thonny)."""
    here = os.path.dirname(os.path.abspath(__file__))
    for candidate in (here, os.getcwd()):
        if candidate and candidate not in sys.path:
            sys.path.insert(0, candidate)


def main():
    _bootstrap()
    try:
        import tkinter as tk
    except ImportError:
        sys.stderr.write(
            "ОШИБКА: не найден модуль tkinter.\n"
            "Lubuntu/Debian:   sudo apt install python3-tk\n"
            "Windows/macOS:    переустанови Python с галочкой Tcl/Tk.\n")
        return 1
    try:
        from engine.app_window import NovaTerraApp
    except Exception:
        sys.stderr.write("Не удалось загрузить движок игры:\n")
        traceback.print_exc()
        return 1
    root = None
    try:
        root = tk.Tk()
        app = NovaTerraApp(root)
        root.mainloop()
    except Exception:
        traceback.print_exc()
        if root is not None:
            try:
                from tkinter import messagebox
                messagebox.showerror(
                    "Нова-Терра",
                    "Сбой системы базы:\n" + traceback.format_exc(limit=6))
            except Exception:
                pass
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
