# -*- coding: utf-8 -*-
"""Автотест без GUI: движок, песочница, сохранения, все 34 уровня."""
import os, sys, shutil, tempfile

def run():
    tmp = tempfile.mkdtemp(prefix="novatest_")
    os.environ["NOVA_TERRA_HOME"] = tmp
    from engine.state_manager import StateManager, TOTAL_LEVELS
    from engine.sandbox import CodeSandbox
    from levels.level_loader import load_level
    from levels.base_level import BaseLevel

    assert TOTAL_LEVELS == 34

    # ---- StateManager
    sm = StateManager()
    sm.player_name = u"Тест"
    sm.add_resource("energy", 5)
    sm.add_xp(120)
    sm.set_grade(1, 5, u"босс")
    sm.add_checkpoint(1, 5, u"AvtoTest")
    path = sm.save()
    assert os.path.isfile(path), path
    sm2 = StateManager()
    assert sm2.load()
    assert sm2.player_name == u"Тест" and sm2.resources["energy"] == 105
    assert sm2.get_grade(1) == 5 and sm2.xp == 120
    assert "Энергия" in sm2.hud_text()

    # ---- CodeSandbox
    lines = []
    sb = CodeSandbox(output_callback=lines.append)
    ok = sb.run("print('Нова', 1+1)\nx = 42\n")
    assert ok and lines[-1] == "Нова 2", lines
    ok, printed = sb.capture_print("for i in range(3): print(i)")
    assert ok and printed == ["0", "1", "2"], printed
    ok = sb.run("while True:\n    pass")
    assert not ok and "цикл завис" in (sb.last_error or "").lower(), sb.last_error
    ok = sb.run("print(1/0)")
    assert not ok and "ноль" in sb.last_error.lower()
    ok = sb.run("x +")
    assert not ok and "синтаксис" in sb.last_error.lower()
    ok = sb.run("if 1 > 0:\nprint('да')")
    assert not ok and "отступ" in sb.last_error.lower()
    ok = sb.run("unknown_var")
    assert not ok and "неизвестное имя" in sb.last_error.lower()
    ok = sb.run("print('a' + 1)")
    assert not ok and "str" in sb.last_error and "int" in sb.last_error
    ok = sb.run("open('/etc/passwd')")
    assert not ok and ("запрещ" in sb.last_error.lower()
                       or "охран" in sb.last_error.lower())
    found, val = sb.eval_expr("x = 5")
    assert found and val == 5
    sb.feed_input("7")
    ok, printed = sb.capture_print("n = int(read())\nprint(n * 2)")
    assert ok and printed == ["7", "14"], printed   # эхо введённых данных + вывод

    # ---- Все уровни
    for n in range(1, TOTAL_LEVELS + 1):
        lv = load_level(n)
        assert lv is not None, n
        assert lv.number == n
        assert len(lv.tasks) >= 1 and len(lv.quiz) >= 1
        nodes, edges = lv.get_flowchart()
        assert nodes, ("flow", n)
        res = lv.grade_quiz([q.get("answer") for q in lv.quiz])
        assert res["grade"] == 5, (n, res)
        bad = lv.grade_quiz([None] * len(lv.quiz))
        assert bad["grade"] == 2, (n, bad)
        # автопроверка задачи 1 с эталонным starter, если он рабочий
        t = lv.get_task(0)
        if t and t.get("starter"):
            sb2 = CodeSandbox(output_callback=lambda s: None)
            okc, fb = BaseLevel.check_task(t, sb2, t["starter"])
            if not okc:
                print("WARN level %d task1 starter: %s" % (n, fb.encode("utf-8")))
    # босс-консоль уровня 1
    lv1 = load_level(1)
    vt = {"prompt": "", "expect_print": lv1.boss["expect_print"]}
    sb3 = CodeSandbox(output_callback=lambda s: None)
    okc, fb = BaseLevel.check_task(vt, sb3, "print('ПОСАДКА ЗАВЕРШЕНА')")
    assert okc, fb
    shutil.rmtree(tmp, ignore_errors=True)
    print("SMOKE OK: state/sandbox/levels verified (34 levels)")

if __name__ == "__main__":
    run()
