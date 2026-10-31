# -*- coding: utf-8 -*-
"""ktp_registry.py — календарно-тематический план (КТП) на 34 урока.

Каждая запись — полное описание уровня для ``BaseLevel``: легенда, блок-схема,
спецификация симулятора, 3 практические задачи с автопроверками, босс-миссия
и тест из 5 вопросов. Тематика строго соответствует программе 7 класса:
переменные -> типы -> ветвления -> циклы -> функции -> списки/матрицы ->
PgZero-игры (уроки 17–34) -> финальная посадка корабля переселенцев.
"""

def _n(nid, kind, text):
    return {"id": nid, "kind": kind, "text": text}


def _flow_linear(steps, cond=None):
    """Цепочка start -> ... -> end; cond — опциональный ромб с ветками."""
    nodes = [_n("start", "start", u"Старт")]
    edges = [("start", "b1")]
    prev = "start"
    i = 1
    for s in steps:
        nodes.append(_n("b%d" % i, "process", s))
        edges.append((prev, "b%d" % i))
        prev = "b%d" % i
        i += 1
    if cond:
        nodes.append(_n("c1", "condition", cond[0]))
        edges.append((prev, "c1"))
        nodes.append(_n("yes", "io", cond[1]))
        edges.append(("c1", "yes", u"True"))
        nodes.append(_n("no", "process", cond[2]))
        edges.append(("c1", "no", u"False"))
        nodes.append(_n("end", "end", u"Готово"))
        edges.append(("yes", "end"))
        edges.append(("no", "end"))
    else:
        nodes.append(_n("end", "end", u"Готово"))
        edges.append((prev, "end"))
    return {"nodes": nodes, "edges": edges}


#: ------------------------------------------------------------------ УРОКИ
#: Список из 34 словарей-описаний (индекс 0 = уровень 1).
LEVELS = []


def _register(num, title, theme, goal, briefing, flow, sim, tasks, boss, quiz,
              xp=50):
    LEVELS.append({
        "number": num, "title": title, "theme": theme, "goal": goal,
        "briefing": briefing, "flowchart": flow, "simulator": sim,
        "tasks": tasks, "boss": boss, "quiz": quiz, "xp_reward": xp,
    })


# ============================================================ БЛОК 1 (1–8)
_register(
    1, u"Посадка модуля", u"Первая программа, print()",
    u"Запустить двигатель стыковочного модуля через print()",
    u"Капсула инженера входит в атмосферу Нова-Терры. Чтобы включить "
    u"двигатели-гасители, нужно отправить первую команду компьютеру базы.",
    _flow_linear([u"Включить питание", u"print('Огонь!')", u"Мягкая посадка"]),
    {"mode": "memory", "variables": {"команда": "print()"}},
    [
        {"prompt": u"Выведи фразу: Система запущена",
         "starter": u"",
         "expect_print": [u"Система запущена"],
         "hint": u"Текст берётся в кавычки: print(\"...\")"},
        {"prompt": u"Выведи число 2077",
         "starter": u"print()", "expect_print": [u"2077"]},
        {"prompt": u"Выведи две строки: Нова и Терра (двумя print)",
         "starter": u"", "expect_print": [u"Нова", u"Терра"]},
    ],
    {"title": u"Гасители тяги", "mode": "console",
     "desc": u"Напиши код, печатающий «ПОСАДКА ЗАВЕРШЕНА».",
     "expect_print": [u"ПОСАДКА ЗАВЕРШЕНА"]},
    [
        {"q": u"Какая функция выводит текст на экран?",
         "options": [u"print()", u"save()", u"draw()", u"lock()"], "answer": 0},
        {"q": u"Текст в Python заключают в...",
         "options": [u"скобки ()", u"кавычки \"\"", u"звёздочки **", u"пробелы"],
         "answer": 1},
        {"q": u"print(\"Нова\") выведет:",
         "options": [u"Нова", u"\"Нова\"", u"ошибку", u"ничего"], "answer": 0},
        {"q": u"Python запускает программы со скоростью примерно:",
         "options": [u"1 кадр в час", u"миллионы строк в секунду",
                     u"1 строка в день", u"как калькулятор"], "answer": 1},
        {"q": u"Что делает команда print(2+2)?",
         "options": [u"печатает 2+2", u"печатает 4", u"создаёт файл",
                     u"выключает базу"], "answer": 1},
    ],
)

_register(
    2, u"Энергоблок: переменные", u"Переменные и присваивание",
    u"Создать переменные энергии и мощности реактора",
    u"Модуль сел. Реактор нужно именованно подключить к сети: каждая "
    u"величина хранится в своей ячейке памяти — переменной.",
    _flow_linear([u"x = 100", u"y = x * 2", u"print(y)"]),
    {"mode": "memory", "variables": {"energy": 100, "power": 200}},
    [
        {"prompt": u"Создай переменную oxygen = 50 и выведи её",
         "starter": u"oxygen = \nprint()",
         "expect_vars": {"oxygen": 50}, "expect_print": [u"50"]},
        {"prompt": u"metal = 30, increased = metal + 20. Выведи increased",
         "starter": u"metal = 30\n",
         "expect_vars": {"increased": 50}, "expect_print": [u"50"]},
        {"prompt": u"Придумай имя переменной для щитов shields и запиши 100",
         "starter": u"", "expect_vars": {"shields": 100}},
    ],
    {"title": u"Пуск реактора", "mode": "console",
     "desc": u"Создай reactor_power = 1000 и выведи его.",
     "expect_print": [u"1000"], "expect_vars": {"reactor_power": 1000}},
    [
        {"q": u"Переменная — это...",
         "options": [u"именованная ячейка памяти", u"кнопка на клавиатуре",
                     u"файл на диске", u"тип ошибки"], "answer": 0},
        {"q": u"Как правильно создать переменную?",
         "options": [u"2x = 5", u"x = 5", u"var x = 5", u"x := 5"], "answer": 1},
        {"q": u"a = 7; print(a + 3) даст:", "options": [u"73", u"10", u"a+3",
                                                        u"ошибку"], "answer": 1},
        {"q": u"Имя переменной НЕ может начинаться с:",
         "options": [u"буквы", u"_", u"цифры", u"кириллицы"], "answer": 2},
        {"q": u"Присваивание означает:",
         "options": [u"записать значение в имя", u"равенство из математики",
                     u"удалить файл", u"напечатать twice"], "answer": 0},
    ],
)

_register(
    3, u"Типы грунта", u"int, float, str, bool",
    u"Классифицировать данные планеты по типам",
    u"Зонды передают образцы: глубина (float), название минерала (str), "
    u"пригодность воздуха (bool), количество кристаллов (int).",
    _flow_linear([u"Прочитать данные", u"type(значение)",
                  u"Записать в журнал"]),
    {"mode": "memory",
     "variables": {"depth": 12.5, "mineral": "кварц", "air_ok": True,
                   "crystals": 7}},
    [
        {"prompt": u"Создай temp = 36.6 и выведи type(temp)",
         "starter": u"temp = \nprint(type())",
         "expect_print": [u"float"]},
        {"prompt": u"Создай имя планеты name = 'Нова-Терра' (str) и выведи его",
         "starter": u"", "expect_print": [u"Нова-Терра"]},
        {"prompt": u"is_safe = True. Выведи type(is_safe)",
         "starter": u"", "expect_print": [u"bool"]},
    ],
    {"title": u"Лаборатория образцов", "mode": "console",
     "desc": u"Выведи type(42) и type('42') — они разные!",
     "expect_print": [u"<class 'int'>", u"<class 'str'>"]},
    [
        {"q": u"type(3.14) вернёт:", "options": [u"int", u"float", u"str",
                                                 u"bool"], "answer": 1},
        {"q": u"\"10\" — это...", "options": [u"число", u"строка", u"логика",
                                              u"ошибка"], "answer": 1},
        {"q": u"Логический тип называется:",
         "options": [u"logic", u"bool", u"flag", u"true"], "answer": 1},
        {"q": u"int — это тип для:",
         "options": [u"целых чисел", u"текста", u"картинок", u"списков"],
         "answer": 0},
        {"q": u"True и False пишутся:",
         "options": [u"строчными буквами", u"с заглавной буквы",
                     u"в скобках", u"как 1/0 обязательно"], "answer": 1},
    ],
)

_register(
    4, u"Калькулятор колониста", u"Арифметика и ввод read()",
    u"Рассчитать материалы для жилого купола",
    u"Купол требует металла и стекла. Инженер вводит размеры — программа "
    u"считает площадь и массу. Данные приходят через read().",
    _flow_linear([u"w = read()", u"h = read()", u"s = w * h", u"print(s)"]),
    {"mode": "memory", "variables": {"w": 6, "h": 4, "s": 24}},
    [
        {"prompt": u"Выведи результат 17 // 5",
         "starter": u"print()", "expect_print": [u"3"]},
        {"prompt": u"Выведи остаток от деления 17 % 5",
         "starter": u"", "expect_print": [u"2"]},
        {"prompt": u"side = 5; выведи площадь квадрата side ** 2",
         "starter": u"side = 5\n", "expect_print": [u"25"],
         },
    ],
    {"title": u"Смета купола", "mode": "console",
     "desc": u"r=10, посчи и выведи длину окружения 2*3.14*r (62.8).",
     "expect_print": [u"62.8"]},
    [
        {"q": u"7 / 2 в Python 3 равно:", "options": [u"3", u"3.5", u"4",
                                                     u"1"], "answer": 1},
        {"q": u"Остаток от деления даёт оператор:",
         "options": ["%", "//", "/", "**"], "answer": 0},
        {"q": u"2 ** 4 это:", "options": [u"8", u"16", u"6", u"24"],
         "answer": 1},
        {"q": u"10 // 3 это:", "options": [u"3.33", u"3", u"1", u"9"],
         "answer": 1},
        {"q": u"read() возвращает данные как:",
         "options": [u"число", u"строку", u"список", u"картинку"], "answer": 1},
    ],
)

_register(
    5, u"Переводчик сигналов", u"Преобразование типов int()/str()/float()",
    u"Превратить текст зонда в числа и обратно",
    u"Зонд шлёт «12 метров». Компьютер понимает только настоящие числа: "
    u"строку надо преобразовать через int(), а число для экрана — через str().",
    _flow_linear([u"s = '12'", u"n = int(s)", u"n = n + 3",
                  u"print(str(n) + ' м')"]),
    {"mode": "memory", "variables": {"s": "12", "n": 15}},
    [
        {"prompt": u"Выведи int('40') + 2", "starter": u"",
         "expect_print": [u"42"]},
        {"prompt": u"Сделай print(str(7) + str(3)) — что получится?",
         "starter": u"", "expect_print": [u"73"]},
        {"prompt": u"price='99'; выведи price умноженное на 2 как число",
         "starter": u"price = '99'\n", "expect_print": [u"198"]},
    ],
    {"title": u"Шлюз связи", "mode": "console",
     "desc": u"Дано depth='250'. Выведи глубину, увеличенную на 50 (300).",
     "expect_print": [u"300"]},
    [
        {"q": u"int('5') + 5 даст:", "options": [u"'55'", u"10", u"ошибку",
                                                u"55"], "answer": 1},
        {"q": u"str(10) превращает число в:",
         "options": [u"строку '10'", u"float", u"bool", u"ошибку"], "answer": 0},
        {"q": u"float('2.5') + 1 =", "options": [u"3.5", u"'2.51'", u"2.6",
                                                 u"ошибку"], "answer": 0},
        {"q": u"int('привет') :", "options": [u"0", u"ошибку ValueError",
                                              u"'привет'", u"None"],
         "answer": 1},
        {"q": u"Почему print('5'+5) ошибётся?",
         "options": [u"нельзя складывать строку и число", u"5 слишком мало",
                     u"нет пробела", u"tkinter мешает"], "answer": 0},
    ],
)

_register(
    6, u"Сортировка грузов", u"Ввод с клавиатуры, if",
    u"Отбраковать груз меньше нормы через if",
    u"Грузовой дрон сбрасывает ящики. Компьютер проверяет массу каждого: "
    u"если легче 10 кг — сигнал тревоги. Здесь появляется условие if.",
    _flow_linear([], cond=(u"mass >= 10?", u"Груз принят", u"ТРЕВОГА")),
    {"mode": "flow_hint", "variables": {"mass": 7}},
    [
        {"prompt": u"x = 12; если x > 10 — выведи 'ОК'",
         "starter": u"x = 12\nif x > 10:\n    ",
         "expect_print": [u"ОК"]},
        {"prompt": u"temp = -3; если temp < 0 — выведи 'Мороз'",
         "starter": u"temp = -3\n", "expect_print": [u"Мороз"]},
        {"prompt": u"level = 5; если level == 5 выведи 'Максимум'",
         "starter": u"", "expect_print": [u"Максимум"]},
    ],
    {"title": u"Таможня орбитального лифта", "mode": "console",
     "desc": u"cargo = 8. Если cargo < 10 выведи 'ОТБРАКОВАН', иначе 'ПРИНЯТ'.",
     "expect_print": [u"ОТБРАКОВАН"]},
    [
        {"q": u"После условия if всегда ставится:",
         "options": [":", u";", u".", u"!"], "answer": 0},
        {"q": u"Блок if выполняется, когда условие:",
         "options": [u"True", u"False", u"пустое", u"числовое"], "answer": 0},
        {"q": u"Сравнение «равно» записывается:",
         "options": ["=", "==", "!=", "=>"], "answer": 1},
        {"q": u"Отступ внутри if обязателен?",
         "options": [u"да, 4 пробела", u"нет", u"только tab",
                     u"по желанию учителя"], "answer": 0},
        {"q": u"if 5 > 3: print('A') выведет:",
         "options": ["A", "5 > 3", "False", "ничего"], "answer": 0},
    ],
)

_register(
    7, u"Аварийный контур", u"if / elif / else",
    u"Построить трёхступенчатую защиту кислорода",
    u"Уровень кислорода падает. База сама выбирает режим: норма, экономия "
    u"или аварийная герметизация. Три ступени — if, elif, else.",
    _flow_linear([], cond=(u"o > 60?", u"НОРМА", u"o > 30?")),
    {"mode": "memory", "variables": {"oxygen": 45, "режим": "экономия"}},
    [
        {"prompt": u"o=70: if o>60 'НОРМА' elif o>30 'ЭКОНОМИЯ' else 'АВАРИЯ'",
         "starter": u"o = 70\nif o > 60:\n    print('НОРМА')\n",
         "expect_print": [u"НОРМА"]},
        {"prompt": u"То же для o = 45 → 'ЭКОНОМИЯ'",
         "starter": u"o = 45\n", "expect_print": [u"ЭКОНОМИЯ"]},
        {"prompt": u"То же для o = 10 → 'АВАРИЯ'",
         "starter": u"o = 10\n", "expect_print": [u"АВАРИЯ"]},
    ],
    {"title": u"Щит от радиации", "mode": "console",
     "desc": u"rad = 120. Если rad>100 'ЩИТ', elif rad>50 'ПРЕДУПРЕЖДЕНИЕ', "
             u"иначе 'ТИХО'. Ожидаем 'ЩИТ'.",
     "expect_print": [u"ЩИТ"]},
    [
        {"q": u"elif — это:",
         "options": [u"иначе если", u"повтор цикла", u"ошибка", u"функция"],
         "answer": 0},
        {"q": u"else выполняет блок, когда:",
         "options": [u"все предыдущие условия ложны", u"условие True",
                     u"программа спит", u"нет переменных"], "answer": 0},
        {"q": u"Сколько блоков if/elif/else выполнится за один прогон?",
         "options": [u"ровно один", u"все", u"ни одного всегда", u"два"],
         "answer": 0},
        {"q": u"elif можно писать несколько раз?",
         "options": [u"да", u"нет", u"только один", u"только в while"],
         "answer": 0},
        {"q": u"При o=45 код из задачи 2 печати:",
         "options": [u"ЭКОНОМИЯ", u"НОРМА", u"АВАРИЯ", u"ошибку"], "answer": 0},
    ],
)

_register(
    8, u"Логика шлюзов", u"and, or, not, сложные условия",
    u"Спроектировать электронику двойного шлюза",
    u"Шлюз открывает только внешнюю дверь, когда давление сравнялось И "
    u"кислород в норме. Логические операторы — электрические цепи решения.",
    _flow_linear([], cond=(u"davlenie and kislorod?", u"ОТКРЫТЬ", u"ЖДАТЬ")),
    {"mode": "memory", "variables": {"davlenie": True, "kislorod": True,
                                     "открыт": True}},
    [
        {"prompt": u"Выведи результат: True and False",
         "starter": u"", "expect_print": [u"False"]},
        {"prompt": u"a=True, b=False. Выведи a or b",
         "starter": u"a = True\nb = False\n", "expect_print": [u"True"]},
        {"prompt": u"Выведи not False", "starter": u"", "expect_print": [u"True"]},
    ],
    {"title": u"Мастер-замок сектора", "mode": "console",
     "desc": u"code=7, key=7. Если code==key and key>5 выведи 'ШЛЮЗ ОТКРЫТ'.",
     "expect_print": [u"ШЛЮЗ ОТКРЫТ"]},
    [
        {"q": u"and даёт True, когда:",
         "options": [u"оба условия True", u"хотя бы одно True",
                     u"оба False", u"одно False"], "answer": 0},
        {"q": u"or даёт True, когда:",
         "options": [u"хотя бы одно условие True", u"оба False",
                     u"только правое", u"никогда"], "answer": 0},
        {"q": u"not True =", "options": [u"False", u"True", u"1", u"ошибку"],
         "answer": 0},
        {"q": u"(5 > 3) and (2 > 4) =", "options": [u"True", u"False", u"5",
                                                    u"ошибку"], "answer": 1},
        {"q": u"Операторы лучше комбинировать через:",
         "options": [u"скобки ()", u"кавычки", u"табляцию", u"comment"],
         "answer": 0},
    ],
)

# ======================================================== БЛОК 2 (9–16)
_register(
    9, u"Конвейер добычи", u"Цикл while",
    u"Заставить бур работать, пока есть порода",
    u"Автономный бур опускается в шахту. Он должен долбить, ПОКА глубина "
    u"меньше цели. Это цикл while — повтор по условию.",
    _flow_linear([], cond=(u"depth < 100?", u"бур +10", u"СТОП")) ,
    {"mode": "memory", "variables": {"depth": 100, "циклов": 10}},
    [
        {"prompt": u"i=1; while i<=3: печатай i и увеличивай i на 1",
         "starter": u"i = 1\nwhile i <= 3:\n    print(i)\n    i = i + 1\n",
         "expect_print": [u"1", u"2", u"3"]},
        {"prompt": u"energy=100; пока energy>0 уменьшай на 40 и печатай",
         "starter": u"energy = 100\n", "expect_print": [u"60", u"20"]},
        {"prompt": u"Посчитай, сколько раз выполнится while n < 3: n += 1 (n=0), "
                    u"выведи 3",
         "starter": u"n = 0\n", "expect_print": [u"3"]},
    ],
    {"title": u"Шахта редких металлов", "mode": "console",
     "desc": u"ore=0. Пока ore<5 добавляй по 1 и в конце выведи 'ДОБЫТО 5'.",
     "expect_print": [u"ДОБЫТО 5"]},
    [
        {"q": u"while повторяет блок, пока условие:",
         "options": [u"True", u"False", u"пустое", u"отрицательное"],
         "answer": 0},
        {"q": u"Если никогда не менять условие — будет:",
         "options": [u"бесконечный цикл", u"1 итерация", u"ошибка синтаксиса",
                     u"выход"], "answer": 0},
        {"q": u"Безопасный лимит итераций в песочнице игры:",
         "options": [u"1000", u"10", u"1 млн", u"без лимита"], "answer": 0},
        {"q": u"i += 1 эквивалентно:",
         "options": ["i = i + 1", "i = 1", "i == 1", "i - 1"], "answer": 0},
        {"q": u"while i != 5: i += 1 при i=0 завершится при i =",
         "options": [u"5", u"4", u"0", u"никогда"], "answer": 0},
    ],
)

_register(
    10, u"Счётчик дронов", u"Цикл for + range()",
    u"Облететь 10 секторов планетоходом",
    u"Дрон-разведчик обязан посетить каждый сектор по номеру. Цикл "
    u"for sector in range(N) — автоматический счётчик облёта.",
    _flow_linear([u"for s in range(10)", u"скан(s)", u"отчёт"]),
    {"mode": "memory", "lists": {"секторы": [0, 1, 2, 3, 4]}},
    [
        {"prompt": u"for i in range(3): print(i)", "starter": u"",
         "expect_print": [u"0", u"1", u"2"]},
        {"prompt": u"Выведи числа от 1 до 5 (range(1,6))",
         "starter": u"", "expect_print": [u"1", u"5"]},
        {"prompt": u"Печатай чётные 2..10: range(2, 11, 2)",
         "starter": u"", "expect_print": [u"2", u"10"]},
    ],
    {"title": u"Карта сектора", "mode": "console",
     "desc": u"for s in range(1,6): печатай 'СЕКТОР' и номер. Нужен СЕКТОР 5.",
     "expect_print": [u"СЕКТОР 5"]},
    [
        {"q": u"range(4) порождает числа:",
         "options": [u"0 1 2 3", u"1 2 3 4", u"0 1 2 3 4", u"4 4 4 4"],
         "answer": 0},
        {"q": u"for — это цикл:",
         "options": [u"по последовательности", u"по condition", u"случайный",
                     u"однократный"], "answer": 0},
        {"q": u"range(2, 8, 2) даст:", "options": [u"2 4 6", u"2 4 6 8",
                                                   u"2 3 4", u"8 6 4 2"],
         "answer": 0},
        {"q": u"Переменная цикла записывается сюда:",
         "options": ["for i in ...", "while i", "if i", "print i"], "answer": 0},
        {"q": u"range(1, 3) выполнится раз:",
         "options": [u"2", u"3", u"1", u"0"], "answer": 0},
    ],
)

_register(
    11, u"Погодная станция", u"Вложенные циклы и условия",
    u"Собрать температуру по 3 дням и 4 измерениям",
    u"Станция меряет погоду 3 раза в сутки, 4 суток подряд. Внешний цикл — "
    u"сутки, внутренний — часы измерений. Так устроены матрицы данных.",
    _flow_linear([u"for day in range(4)", u"  for h in range(3)",
                  u"    замер(day,h)"]),
    {"mode": "memory",
     "matrices": {"t": [[12, 14, 9], [13, 15, 8], [11, 13, 7], [12, 16, 6]]}},
    [
        {"prompt": u"4 дня × 2 часа: печатай 'День d Час c'",
         "starter": u"for d in range(1, 5):\n    for c in range(1, 3):\n"
                    u"        print('День', d, 'Час', c)\n",
         "expect_print": [u"День 1 Час 1", u"День 4 Час 2"]},
        {"prompt": u"Во вложенном цикле посчитай сумму 1..3 (выведи 6)",
         "starter": u"s = 0\nfor i in range(1, 4):\n    s += i\nprint(s)\n",
         "expect_print": [u"6"]},
        {"prompt": u"Печатай '*' квадратом 3×3 (двойной for)",
         "starter": u"", "expect_print": [u"***"]},
    ],
    {"title": u"Штормовое предупреждение", "mode": "console",
     "desc": u"for t in range(-5, 6): если t<-3 печатай 'ШТОРМ'. Ожидаем ШТОРМ.",
     "expect_print": [u"ШТОРМ"]},
    [
        {"q": u"Вложенный цикл — это:",
         "options": [u"цикл внутри цикла", u"два файла", u"ошибка",
                     u"функция"], "answer": 0},
        {"q": u"for i in range(3): for j in range(3) выполнится пар (i,j):",
         "options": [u"9", u"6", u"3", u"12"], "answer": 0},
        {"q": u"Отступ показывает:",
         "options": [u"вложенность блока", u"красоту", u"скорость",
                     u"имя файла"], "answer": 0},
        {"q": u"Сумма 1+2+3 равна:", "options": [u"6", u"5", u"9", u"3"],
         "answer": 0},
        {"q": u"range(0) содержит элементов:",
         "options": [u"0", u"1", u"бесконечно", u"ошибку"], "answer": 0},
    ],
)

_register(
    12, u"Фабрика деталей", u"Функции def, параметры",
    u"Создать конвейерных роботов-функций",
    u"Ручной монтаж деталей медленный. Инженер описывает действие один раз "
    u"— функцию def detail() — и робот повторяет её мгновенно.",
    _flow_linear([u"def weld(x):", u"  return x * 2", u"weld(5)"]),
    {"mode": "memory", "variables": {"деталь": "weld(5)=10"}},
    [
        {"prompt": u"Создай def hello(): print('Привет, Нова') и вызови",
         "starter": u"def hello():\n    print('Привет, Нова')\n\nhello()\n",
         "expect_print": [u"Привет, Нова"]},
        {"prompt": u"def square(n): return n*n. Выведи square(6)",
         "starter": u"", "expect_print": [u"36"]},
        {"prompt": u"Функция mass(len_, w=2) возвращает len_*w. Выведи mass(5)",
         "starter": u"", "expect_print": [u"10"]},
    ],
    {"title": u"3D-принтер корпуса", "mode": "console",
     "desc": u"Напиши def part(name): return 'ДЕТАЛЬ:' + name. "
             u"Выведи part('щит').",
     "expect_print": [u"ДЕТАЛЬ:щит"]},
    [
        {"q": u"Ключевое слово создания функции:",
         "options": ["def", "func", "sub", "lambda_fn"], "answer": 0},
        {"q": u"return нужен, чтобы:",
         "options": [u"вернуть результат вызова", u"напечатать",
                     u"остановить игру", u"создать цикл"], "answer": 0},
        {"q": u"Вызов функции greet() без скобок:",
         "options": [u"не выполнит её", u"ошибку", u"напечатает ()",
                     u"удалит"], "answer": 0},
        {"q": u"Параметр функции записывают в:",
         "options": [u"круглые скобки после имени", u"кавычки", u"отступ",
                     u"комментарий"], "answer": 0},
        {"q": u"def f(x): return x+1; f(2) =", "options": [u"3", u"2", u"x+1",
                                                          u"ошибку"],
         "answer": 0},
    ],
)

_register(
    13, u"Центр управления полётами", u"Аргументы, возврат значений",
    u"Построить цепочку функций расчёта траектории",
    u"Каждая подсистема ЦУПа — функция с входом и выходом. Результат одной "
    u"становится аргументом другой: конвейер научных вычислений.",
    _flow_linear([u"v = speed(t, s)", u"h = height(v)", u"print(h)"]),
    {"mode": "memory", "variables": {"t": 4, "s": 20, "v": 5.0, "h": 12.5}},
    [
        {"prompt": u"def perim(a, b): return 2*(a+b); напечатай perim(3,4)",
         "starter": u"", "expect_print": [u"14"]},
        {"prompt": u"def to_f(c): return c*9/5+32; выведи to_f(0)",
         "starter": u"", "expect_print": [u"32.0"]},
        {"prompt": u"f(x)=x*2, g(x)=x+5; выведи g(f(3))",
         "starter": u"", "expect_print": [u"11"]},
    ],
    {"title": u"Окно запуска", "mode": "console",
     "desc": u"def fuel(days): return days*12. Для 30 дней выведи 360.",
     "expect_print": [u"360"]},
    [
        {"q": u"Аргумент функции — это:",
         "options": [u"данные на входе", u"имя файла", u"результат",
                     u"ошибка"], "answer": 0},
        {"q": u"Функция без return возвращает:",
         "options": [u"None", u"0", u"строку", u"ошибку"], "answer": 0},
        {"q": u"g(f(3)) значит: сначала",
         "options": [u"вычислить f(3)", u"вычислить g", u"ошибку",
                     u" цикл"], "answer": 0},
        {"q": u"Сколько аргументов у len(spisok)?",
         "options": [u"1", u"2", u"0", u"3"], "answer": 0},
        {"q": u"def area(w, h=10) — значение h по умолчанию:",
         "options": [u"10", u"w", u"None", u"обязательным"], "answer": 0},
    ],
)

_register(
    14, u"Склад модулей", u"Списки list, индексы, append",
    u"Организовать склад контейнеров базы",
    u"Все грузы теперь хранятся одним списком: склад[0] — первый контейнер. "
    u"append() добавляет новые ящики, len() считает место.",
    _flow_linear([u"sklad = []", u"sklad.append('генератор')",
                  u"print(len(sklad))"]),
    {"mode": "memory",
     "lists": {"склад": ["генератор", "купол", "бур", "дрон"]}},
    [
        {"prompt": u"Создай список iz 3 предметов и выведи его",
         "starter": u"tools = ['лом', 'дрон', 'кабель']\nprint(tools)\n",
         "expect_print": [u"['лом', 'дрон', 'кабель']"]},
        {"prompt": u"Добавь 'щит' в sklad=[] и выведи len(sklad)",
         "starter": u"sklad = []\n", "expect_print": [u"1"]},
        {"prompt": u"Выведи второй элемент списка [10,20,30]",
         "starter": u"", "expect_print": [u"20"]},
    ],
    {"title": u"Инвентаризация", "mode": "console",
     "desc": u"Список из 4 модулей. Добавь 5-й 'ядро' и выведи его по "
             u"индексу 4.",
     "expect_print": [u"ядро"]},
    [
        {"q": u"Первый элемент списка имеет индекс:",
         "options": [u"0", u"1", u"-1", u"any"], "answer": 0},
        {"q": u"Добавить элемент в конец умеет:",
         "options": ["append()", "push()", "add()", "put()"], "answer": 0},
        {"q": u"len([1,2,3]) =", "options": [u"3", u"2", u"6", u"0"],
         "answer": 0},
        {"q": u"[10,20,30][1] это:", "options": [u"10", u"20", u"30", u"ошибку"],
         "answer": 1},
        {"q": u"Список создаётся:",
         "options": [u"квадратными скобками", u"круглыми", u"фигурными",
                     u"кавычками"], "answer": 0},
    ],
)

_register(
    15, u"Гидропоника", u"Циклы и списки, срезы",
    u"Полив грядок в автоматическом цикле",
    u"Оранжерея — список грядок. Робот проходит по ним циклом for, "
    u"срез [1:3] выделяет зону засухи, sum() считает воду.",
    _flow_linear([u"for bed in garden:", u"  water(bed)", u"print(sum(water))"]),
    {"mode": "memory", "lists": {"грядки": [2, 5, 3, 8, 1]}},
    [
        {"prompt": u"Просуммируй [2,5,3,8,1] через sum() — выведи 19",
         "starter": u"", "expect_print": [u"19"]},
        {"prompt": u"Выведи срез [2,5,3,8,1][1:3] ([5, 3])",
         "starter": u"", "expect_print": [u"[5, 3]"]},
        {"prompt": u"for c in [1,2,3]: печатай c*10 (10 20 30)",
         "starter": u"", "expect_print": [u"10", u"30"]},
    ],
    {"title": u"Засушливый сектор", "mode": "console",
     "desc": u"Вода [4,0,7,0,2]. Посчитай сумму (13) и выведи.",
     "expect_print": [u"13"]},
    [
        {"q": u"sp[1:3] включает элементы с индексами:",
         "options": [u"1 и 2", u"1, 2 и 3", u"только 2", u"3 и 4"],
         "answer": 0},
        {"q": u"sum([1,2,3]) =", "options": [u"6", u"123", u"3", u"0"],
         "answer": 0},
        {"q": u"for x in sp: — x принимает:",
         "options": [u"значения элементов", u"индексы", u"длину", u"0"],
         "answer": 0},
        {"q": u"max([4,9,2]) =", "options": [u"9", u"4", u"2", u"15"],
         "answer": 0},
        {"q": u"sp[-1] — это:",
         "options": [u"последний элемент", u"первый", u"длина", u"пусто"],
         "answer": 0},
    ],
)

_register(
    16, u"Карта планеты", u"Двумерные списки (матрицы)",
    u"Загрузить растровую карту территории",
    u"Спутник передал карту 5×5: список списков. Каждая клетка — 0 (равнина) "
    u"или 1 (гора). Обход двойным циклом — стандарт работы с матрицей.",
    _flow_linear([u"for row in karta:", u"  for cell in row:", u"    print(cell)"]),
    {"mode": "memory",
     "matrices": {"map": [[0, 0, 1, 0, 0], [0, 1, 1, 1, 0], [0, 0, 1, 0, 0],
                          [1, 1, 0, 0, 1], [0, 0, 0, 1, 0]]}},
    [
        {"prompt": u"Выведи элемент map[1][2] матрицы из примера (1)",
         "starter": u"map = [[0,0,1,0,0],[0,1,1,1,0],[0,0,1,0,0],"
                    u"[1,1,0,0,1],[0,0,0,1,0]]\n",
         "expect_print": [u"1"]},
        {"prompt": u"Посчитай единиц в первой строке (их 1) — выведи 1",
         "starter": u"", "expect_print": [u"1"]},
        {"prompt": u"Двойным циклом напечатай все нули строки [0,0,1] (0 0)",
         "starter": u"", "expect_print": [u"0"]},
    ],
    {"title": u"Разведка хребта", "mode": "console",
     "desc": u"map=[[1,0],[0,1]]. Выведи сумму всех клеток (2).",
     "expect_print": [u"2"]},
    [
        {"q": u"Матрица — это:",
         "options": [u"список списков", u"один большой текст", u"число",
                     u"функция"], "answer": 0},
        {"q": u"a[2][1] — доступ к:",
         "options": [u"элементу 3-й строки, 2-го столбца", u"столбцу 21",
                     u"длине", u"срезу"], "answer": 0},
        {"q": u"Для обхода матрицы нужно циклов:",
         "options": [u"два (вложенных)", u"один", u"три", u"ноль"],
         "answer": 0},
        {"q": u"len([[1,2],[3,4]]) =", "options": [u"2", u"4", u"1", u"0"],
         "answer": 0},
        {"q": u"[[0]*3]*2 создаст матрицу размером:",
         "options": [u"2×3", u"3×2", u"6×6", u"1×6"], "answer": 0},
    ],
)

# ==================================================== БЛОК 3 (17–26) PgZero
_register(
    17, u"Ровер: знакомство с ареной", u"Actor, координаты, keyboard",
    u"Научить марсоход ездить по карте",
    u"С уроков 17–34 база управляется игровым движком (эмулятор PgZero). "
    u"Ровер — объект Actor(x, y, w, h). Клавиши стрелок двигают его по холсту.",
    _flow_linear([u"actor = Actor(x,y,w,h)", u"update(dt): move",
                  u"draw(): actor.draw_self()"]),
    {"mode": "pgzero", "arena": {"speed": 4}},
    [
        {"prompt": u"Создай Actor(canvas, 10, 20, 30, 40) и выведи его pos",
         "starter": u"a = Actor(canvas, 10, 20, 30, 40)\nprint(a.pos)\n",
         "expect_print": [u"(10.0, 20.0)"]},
        {"prompt": u"Сдвинь актёр на (5, 5) методом move() и выведи x",
         "starter": u"", "expect_print": [u"15.0"]},
        {"prompt": u"Выведи ширину экрана: canvas.screen['width']",
         "starter": u"", "expect_print": None},
    ],
    {"title": u"Испытание ровера №17", "mode": "pgzero",
     "desc": u"Управление стрелками. Доведи жёлтый ровер до ракеты, не касаясь красных скал."},
    [
        {"q": u"Координаты Actor задаются:",
         "options": [u"x, y (центр)", u"ширина", u"цвет", u"скорость"],
         "answer": 0},
        {"q": u"Метод движения на смещение:",
         "options": ["move(dx, dy)", "go()", "run()", "step()"], "answer": 0},
        {"q": u"Клавиши читает объект:",
         "options": ["keyboard", "mouse", "buttons", "sys.keys"], "answer": 0},
        {"q": u"canvas.screen['width'] это:",
         "options": [u"ширина арены", u"высота", u"fps", u"вес"], "answer": 0},
        {"q": u"Отрисовка актёра вызывается методом:",
         "options": ["draw_self()", "show()", "paint()", "render()"],
         "answer": 0},
    ],
)

_register(
    18, u"Столкновение с метеоритом", u"colliderect(), коллизии",
    u"Построить систему обнаружения столкновений",
    u"Метеориты падают на базу. Метод .colliderect(other) отвечает True, "
    u"если два прямоугольника пересекаются — основа любой защиты.",
    _flow_linear([], cond=(u"a.colliderect(b)?", u"ТРЕВОГА", u"СПОКОЙНО")),
    {"mode": "pgzero", "arena": {"speed": 4}},
    [
        {"prompt": u"Два Actor 40×40 в точках (0,0) и (10,10). "
                   u"Выведи a.colliderect(b)",
         "starter": u"a = Actor(canvas, 0, 0, 40, 40)\nb = Actor(canvas, 10, 10, 40, 40)\n"
                    u"print(a.colliderect(b))\n", "expect_print": [u"True"]},
        {"prompt": u"Те же, но b в (500, 500) — выведи False",
         "starter": u"", "expect_print": [u"False"]},
        {"prompt": u"Выведи расстояние a.distance_to(b) для (0,0)->(3,4) = 5.0",
         "starter": u"", "expect_print": [u"5.0"]},
    ],
    {"title": u"Метеоритный дождь", "mode": "pgzero",
     "desc": u"Уклоняйся от красных метеоритов (стен) до спасательной капсулы."},
    [
        {"q": u"colliderect возвращает:",
         "options": [u"True/False", u"число", u"список", u"None"], "answer": 0},
        {"q": u"Пересечение происходит, когда прямоугольники:",
         "options": [u"накладываются", u"касаются краями на 0 пикселей",
                     u"далеки", u"одного цвета"], "answer": 0},
        {"q": u"Расстояние между точками считает:",
         "options": ["math.hypot", "abs", "round", "len"], "answer": 0},
        {"q": u"Стены арены реализованы как:",
         "options": [u"список Actor", u"кортеж", u"словарь", u"строка"],
         "answer": 0},
        {"q": u"Если актёр коснулся стены, игра должна:",
         "options": [u"остановить цикл и показать провал", u"игнорировать",
                     u"ускорить", u"закрыть окно"], "answer": 0},
    ],
)

_register(
    19, u"Игровой цикл", u"update() / draw(), кадры",
    u"Разобрать жизнь движка по кадрам",
    u"Движок 30 раз в секунду вызывает update(dt) (логика) и draw() "
    u"(картинка). Всё движение мира — результат этих двух функций.",
    _flow_linear([u"update(dt)", u"draw()", u"after(33ms) снова"]),
    {"mode": "pgzero", "arena": {"speed": 5}},
    [
        {"prompt": u"Сколько fps по умолчанию в эмуляторе? выведи 30",
         "starter": u"", "expect_print": [u"30"]},
        {"prompt": u"Сначала вызывается функция ___ (выведи 'update')",
         "starter": u"", "expect_print": [u"update"]},
        {"prompt": u"dt измеряется в:", "starter": u"",
         "expect_print": [u"секундах"]},
    ],
    {"title": u"Конвейер кадров", "mode": "pgzero",
     "desc": u"Дойди до цели — каждый кадр обновляет позицию. Стрелки!"},
    [
        {"q": u"update() отвечает за:",
         "options": [u"логику движения", u"отрисовку", u"звук", u"файлы"],
         "answer": 0},
        {"q": u"draw() отвечает за:",
         "options": [u"отрисовку кадра", u"физику", u"сохранение", u"ошибки"],
         "answer": 0},
        {"q": u"FPS — это:",
         "options": [u"кадров в секунду", u"пикселей в файле", u"байт в строке",
                     u"уровней силы"], "answer": 0},
        {"q": u"Цикл замыкает метод Tkinter:",
         "options": ["after()", "sleep()", "join()", "loop()"], "answer": 0},
        {"q": u"Если в draw() ошибка, движок:",
         "options": [u"остановит цикл и сообщит", u"промолчит",
                     u"ускорится", u"перезапустит ПК"], "answer": 0},
    ],
)

_register(
    20, u"Сбор кристаллов", u"Случайные предметы, счёт",
    u"Настроить генератор кристаллов энергии",
    u"random.randint() рондает кристаллы в случайных точках. При "
    u"colliderect кристалл исчезает, счёт растёт — экономика базы.",
    _flow_linear([u"spawn random", u"forbidden check", u"score += 1"]),
    {"mode": "pgzero", "arena": {"speed": 5}},
    [
        {"prompt": u"seed(7); выведи random.randint(1, 10)",
         "starter": u"random.seed(7)\nprint(random.randint(1, 10))\n",
         "expect_print": None},
        {"prompt": u"Счёт score=0; score+=1; выведи 1",
         "starter": u"", "expect_print": [u"1"]},
        {"prompt": u"list(range(3)) → выведи [0, 1, 2]",
         "starter": u"", "expect_print": [u"[0, 1, 2]"]},
    ],
    {"title": u"Поле кристаллов", "mode": "pgzero",
     "desc": u"Собери все кристаллы-энергию, избегая скал."},
    [
        {"q": u"Случайное целое даёт:",
         "options": ["random.randint(a,b)", "rand.max()", "rnd()", "choice_int()"],
         "answer": 0},
        {"q": u"seed(число) нужен для:",
         "options": [u"повторяемости случайностей", u"шифрования",
                     u"ускорения", u"цвета"], "answer": 0},
        {"q": u"score += 1 это:",
         "options": [u"увеличение счёта", u"сравнение", u"деление",
                     u"ошибку"], "answer": 0},
        {"q": u"Собранный кристалл убирают из:",
         "options": [u"списка объектов", u"переменной", u"клавиатуры",
                     u"фона"], "answer": 0},
        {"q": u"Случайный выбор элемента:",
         "options": ["random.choice(list)", "rand.get()", "list.pick()",
                     "choose.random()"], "answer": 0},
    ],
)

_register(
    21, u"Строительный дрон", u"Мышь, drag&drop, события",
    u"Собирать модули базы мышью",
    u"Дрон-строитель тащит блоки курсором мыши: событие <Button-1> захват, "
    u"<Motion> перенос, <ButtonRelease-1> установка в слот (colliderect).",
    _flow_linear([u"mouse down", u"drag block", u"release -> slot?"]),
    {"mode": "pgzero", "arena": {"speed": 6}},
    [
        {"prompt": u"Выведи 'мышь', если True and True",
         "starter": u"", "expect_print": [u"мышь"]},
        {"prompt": u"pos=(100,200); выведи pos[0] (100)",
         "starter": u"", "expect_print": [u"100"]},
        {"prompt": u"Создай tuple (1,2) и выведи его",
         "starter": u"", "expect_print": [u"(1, 2)"]},
    ],
    {"title": u"Монтаж ангара", "mode": "pgzero",
     "desc": u"Стрелками загони строительный блок в жёлтый слот."},
    [
        {"q": u"Клик левой кнопкой — событие:",
         "options": ["<Button-1>", "<Click>", "<Mouse-L>", "<Press-A>"],
         "answer": 0},
        {"q": u"Движение мыши отслеживает:",
         "options": ["<Motion>", "<Move>", "<Slide>", "<DragEvent>"],
         "answer": 0},
        {"q": u"event.x, event.y дают:",
         "options": [u"координаты курсора", u"скорость", u"номер кнопки",
                     u"dpi"], "answer": 0},
        {"q": u"Кортеж отличается от списка тем, что:",
         "options": [u"неизменяемый", u"длиннее", u"только чисел",
                     u"медленнее"], "answer": 0},
        {"q": u"«Отпустить» блок помогает событие:",
         "options": ["<ButtonRelease-1>", "<Up>", "<Free>", "<Stop>"],
         "answer": 0},
    ],
)

_register(
    22, u"Энергосеть", u"Словари dict, ключи",
    u"Свести баланс потребителей базы в словаре",
    u"Каждый модуль — запись «имя: мощность». Словарь power['реактор']=500 "
    u"позволяет мгновенно найти нужного потребителя.",
    _flow_linear([u"power = {}", u"power[key] = v", u"print(power[key])"]),
    {"mode": "memory",
     "variables": {"power": "{'реактор': 500, 'куполь': 120, 'дрон': 80}"}},
    [
        {"prompt": u"Создай d={'a':1,'b':2}; выведи d['b']",
         "starter": u"", "expect_print": [u"2"]},
        {"prompt": u"Добавь ключ 'c' со значением 3, выведи len(d) → 3",
         "starter": u"", "expect_print": [u"3"]},
        {"prompt": u"d.get('zzz', 0) должно вывести 0",
         "starter": u"", "expect_print": [u"0"]},
    ],
    {"title": u"Перегрузка сети", "mode": "console",
     "desc": u"power={...}. Посчитай сумму values() и выведи 700.",
     "expect_print": [u"700"]},
    [
        {"q": u"Словарь задаётся скобками:",
         "options": ["{}", "[]", "()", "<>"], "answer": 0},
        {"q": u"Пары словаря состоят из:",
         "options": [u"ключа и значения", u"двух чисел", u"индексов",
                     u"строк"], "answer": 0},
        {"q": u"b['x'] при отсутствии ключа x:",
         "options": [u"KeyError", u"None", u"0", u"создаст 1"], "answer": 0},
        {"q": u"Безопасный поиск значения:",
         "options": ["d.get(k, 0)", "d.find(k)", "d[k]?", "d.search(k)"],
         "answer": 0},
        {"q": u"list(d.values()) вернёт:",
         "options": [u"все значения", u"все ключи", u"длину", u"сортировку"],
         "answer": 0},
    ],
)

_register(
    23, u"Радиопередатчик", u"Строки, f-строки, методы",
    u"Собрать протокол обмена с Орбитальной Станцией",
    u"Сообщения формируются шаблонами: f'Стыковка через {t} сек'. "
    u"upper(), split(), replace() — инструментальная лента текстовика.",
    _flow_linear([u"msg = f'...' ", u"msg.upper()", u"send(msg)"]),
    {"mode": "memory", "variables": {"msg": "стыковка T+10"}},
    [
        {"prompt": u"t=10; выведи f'СТЫКОВКА T+{t}'",
         "starter": u"t = 10\nprint(f'СТЫКОВКА T+{t}')\n",
         "expect_print": [u"СТЫКОВКА T+10"]},
        {"prompt": u"Выведи 'нова'.upper()", "starter": u"",
         "expect_print": [u"NOVA"]},
        {"prompt": u"'a,b,c'.split(',') → выведи ['a', 'b', 'c']",
         "starter": u"", "expect_print": [u"['a', 'b', 'c']"]},
    ],
    {"title": u"Помехи в эфире", "mode": "console",
     "desc": u"Закодировал сообщение 'SOS ' заменой пробела на '*', "
             u"выведи 'SOS*' (replace).",
     "expect_print": [u"SOS*"]},
    [
        {"q": u"f-строка нужна для:",
         "options": [u"вставки переменных в текст", u"формата файлов",
                     u"быстрого чтения", u"шифрования"], "answer": 0},
        {"q": u"'abc'.upper() вернёт:", "options": ["ABC", "abc", "Abc",
                                                    "CBA"], "answer": 0},
        {"q": u"split() разбивает строку на:",
         "options": [u"список частей", u"числа", u"словарь", u"файл"],
         "answer": 0},
        {"q": u"replace('a','b') :",
         "options": [u"заменяет подстроку", u"удаляет строку", u"складывает",
                     u"сортирует"], "answer": 0},
        {"q": u"len('Нова') =", "options": [u"4", u"3", u"8", u"2"],
         "answer": 0},
    ],
)

_register(
    24, u"Медицинский отсек", u"Функции + словари + списки",
    u"Автоматизировать бортовой медсканер",
    u"Медсканер хранит пациентов списком словарей [{'имя':..., 'пульс':...}]. "
    u"Функция scan(pacients) возвращает тех, у кого пульс вне нормы.",
    _flow_linear([u"def scan(lst):", u"  for p in lst:", u"    if p['пульс']>100",
                  u"      alert.append(p)"]),
    {"mode": "memory",
     "lists": [{"имя": "Аня", "пульс": 72}, {"имя": "Виктор", "пульс": 118}]},
    [
        {"prompt": u"Верни из функции ['Виктор'] — пациенты с пульсом>100",
         "starter": u"pats = [{'name':'Аня','pulse':72},"
                    u"{'name':'Виктор','pulse':118}]\n",
         "expect_print": [u"Виктор"]},
        {"prompt": u"len([{},{},{}]) → выведи 3", "starter": u"",
         "expect_print": [u"3"]},
        {"prompt": u"Выведи 'норма', если пульс 80 < 100",
         "starter": u"", "expect_print": [u"норма"]},
    ],
    {"title": u"Эпидемия в модуле C", "mode": "console",
     "desc": u"Список из 4 больных. Функция sick() возвращает число "
             u"пульс>100. Выведи 2.",
     "expect_print": [u"2"]},
    [
        {"q": u"Список словарей удобен для:",
         "options": [u"таблиц records", u"рисования", u"звука", u"циклов"],
         "answer": 0},
        {"q": u"p['пульс'] достаёт:",
         "options": [u"значение по ключу", u"индекс", u"срез", u"длину"],
         "answer": 0},
        {"q": u"alert.append(x) :",
         "options": [u"добавит x в конец", u"удалит x", u"найдёт x",
                     u"отсортирует"], "answer": 0},
        {"q": u"Функция с параметром lst получает:",
         "options": [u"данные извне", u"только числа", u"ничего",
                     u"файл"], "answer": 0},
        {"q": u"Фильтрация обычно идёт внутри:",
         "options": [u"for + if", u"print", u"import", u"try"], "answer": 0},
    ],
)

_register(
    25, u"Терраформ-станция", u"Обработка исключений try/except",
    u"Защитить станцию от сбоев датчиков",
    u"Датчик может прислать мусор вместо числа. try/except перехватывает "
    u"ValueError и ZeroDivisionError — станция продолжает работу.",
    _flow_linear([], cond=(u"try удался?", u"данные приняты",
                           u"except → резерв")),
    {"mode": "memory", "variables": {"датчик": "'--'", "защита": "try/except"}},
    [
        {"prompt": u"try: int('abc') except ValueError: print('СБОЙ')",
         "starter": u"try:\n    int('abc')\nexcept ValueError:\n"
                    u"    print('СБОЙ')\n", "expect_print": [u"СБОЙ"]},
        {"prompt": u"Заверни 10/0 в try/except ZeroDivisionError, печатай 'РЕЗЕРВ'",
         "starter": u"", "expect_print": [u"РЕЗЕРВ"]},
        {"prompt": u"try успешный: except не сработает → выведи 'ЧИСТО'",
         "starter": u"", "expect_print": [u"ЧИСТО"]},
    ],
    {"title": u"Шторм помех", "mode": "console",
     "desc": u"Читает значения ['12','--','8']; нечисловые пропускай через "
             u"try. Выведи сумму 20.",
     "expect_print": [u"20"]},
    [
        {"q": u"try/except защищает от:",
         "options": [u"исключений (ошибок времени выполнения)", u"опечаток "
                     u"в комментариях", u"долгих имён", u"циклов"],
         "answer": 0},
        {"q": u"ValueError возникает при:",
         "options": [u"int('привет')", u"delims na nol", u"indeks 99",
                     u"importe os"], "answer": 0},
        {"q": u"Блок except выполняют, когда:",
         "options": [u"в try произошла ошибка", u"всё хорошо", u"нет "
                     u"переменных", u"программа закрылась"], "answer": 0},
        {"q": u"except ZeroDivisionError ловит ошибку:",
         "options": [u"деления на 0", u"умножения", u"сложения", u"чтения"],
         "answer": 0},
        {"q": u"Без try/except ошибка в программе:",
         "options": [u"остановит выполнение", u"будет проигнорирована",
                     u"исправится сама", u"удалит файл"], "answer": 0},
    ],
)

_register(
    26, u"Обсерватория", u"Модуль math, формулы",
    u"Рассчитать орбиту станции наблюдения",
    u"math.sqrt(), math.pi, math.floor/ceil — научный арсенал. Орбита "
    u"строится по формулам, а не на глаз.",
    _flow_linear([u"import math", u"r = math.sqrt(area/math.pi)",
                  u"print(round(r, 2))"]),
    {"mode": "memory", "variables": {"pi": 3.141592653589793, "sqrt81": 9.0}},
    [
        {"prompt": u"Выведи math.sqrt(81)", "starter": u"import math\n",
         "expect_print": [u"9.0"]},
        {"prompt": u"math.ceil(4.1) → выведи 5", "starter": u"import math\n",
         "expect_print": [u"5"]},
        {"prompt": u"Длина окружности r=5: 2*math.pi*r, округли до 2 знаков "
                    u"(31.42)", "starter": u"", "expect_print": [u"31.42"]},
    ],
    {"title": u"Гравитационная аномалия", "mode": "console",
     "desc": u"F = m*a (m=12, a=9.8 через round(F,1)). Выведи 117.6.",
     "expect_print": [u"117.6"]},
    [
        {"q": u"math.sqrt(16) =", "options": [u"4.0", u"8", u"256", u"2"],
         "answer": 0},
        {"q": u"math.pi примерно:", "options": [u"3.14", u"2.71", u"1.41",
                                                u"0.57"], "answer": 0},
        {"q": u"floor(7.9) =", "options": [u"7", u"8", u"7.9", u"0"],
         "answer": 0},
        {"q": u"round(2.567, 2) =", "options": [u"2.57", u"2.56", u"3",
                                                u"2.567"], "answer": 0},
        {"q": u"Подключают модуль командой:",
         "options": ["import math", "using math", "include math", "load math"],
         "answer": 0},
    ],
)

# ==================================================== БЛОК 4 (27–34) ФИНАЛ
_register(
    27, u"Метеозащита купола", u"random, симуляция событий",
    u"Настроить предсказание пылевых бурь",
    u"Буря приходит случайно. Моделируем сутки: random.random()<0.3 — шторм. "
    u"Если щиты ниже порога — ремонт. Теория вероятностей в деле.",
    _flow_linear([u"day in range(10)", u"storm = random()<0.3",
                  u"if storm: shields -= 10"]),
    {"mode": "pgzero", "arena": {"speed": 5}},
    [
        {"prompt": u"seed(1); random.random() < 1 → выведи True",
         "starter": u"random.seed(1)\nprint(random.random() < 1)\n",
         "expect_print": [u"True"]},
        {"prompt": u"Смодели 5 бросков randint(1,6), выведи сумму",
         "starter": u"random.seed(3)\ns = 0\nfor i in range(5):\n"
                    u"    s += random.randint(1, 6)\nprint(s)\n",
         "expect_print": None},
        {"prompt": u"shields=100, буря сняла 15. Выведи 85",
         "starter": u"", "expect_print": [u"85"]},
    ],
    {"title": u"Пылевая буря", "mode": "pgzero",
     "desc": u"Доберись до генератора щита сквозь метель частиц (скал)."},
    [
        {"q": u"random.random() выдаёт число из:",
         "options": [u"[0, 1)", u"[1, 100]", u"целые", u"строки"], "answer": 0},
        {"q": u"Вероятность события 30% задают проверкой:",
         "options": ["random.random() < 0.3", "random() == 0.3",
                     "rand(30)", "chance(0.3)"], "answer": 0},
        {"q": u"seed нужен, чтобы:",
         "options": [u"эксперимент повторялся", u"ускорить", u"запомнить "
                     u"имена", u"закрыть окна"], "answer": 0},
        {"q": u" randint(1,6) может выдать:",
         "options": [u"6", u"0", u"7", u"6.5"], "answer": 0},
        {"q": u"Моделирование случайных процессов называется:",
         "options": [u"симуляция Монте-Карло", u"компиляция", u"парсинг",
                     u"рендеринг"], "answer": 0},
    ],
)

_register(
    28, u"Генератор кислорода", u"Алгоритмы, накопитель (accumulator)",
    u"Вывести O2 из ледяных недр",
    u"Электролизёр выдаёт порцию кислорода каждую минуту. Накопитель total "
    u"+= rate — классический алгоритмический приём суммирования.",
    _flow_linear([u"total = 0", u"for min in range(60):", u"  total += rate",
                  u"print(total)"]),
    {"mode": "memory", "variables": {"rate": 3, "total": 180}},
    [
        {"prompt": u"Накопи сумму чисел 1..10 (55)",
         "starter": u"total = 0\nfor i in range(1, 11):\n    total += i\n"
                    u"print(total)\n", "expect_print": [u"55"]},
        {"prompt": u"Среднее арифметическое [2,4,6] → 4",
         "starter": u"", "expect_print": [u"4"]},
        {"prompt": u"Произведение 1..5 → 120", "starter": u"",
         "expect_print": [u"120"]},
    ],
    {"title": u"Пуск электролиза", "mode": "console",
     "desc": u"За 24 минуты по 7 литров (24*7). Выведи 168.",
     "expect_print": [u"168"]},
    [
        {"q": u"Накопитель перед циклом обычно:",
         "options": [u"обнуляют", u"удаляют", u"печатают", u"умножают"],
         "answer": 0},
        {"q": u"Среднее = сумма :", "options": [u"количество", u"минимум",
                                                u"максимум", u"длину строки"],
         "answer": 0},
        {"q": u"total += rate аналогично:",
         "options": ["total = total + rate", "total = rate", "total == rate",
                     "total - rate"], "answer": 0},
        {"q": u"Алгоритм — это:",
         "options": [u"точный план решения", u"язык", u"ошибка", u"файл"],
         "answer": 0},
        {"q": u"range(1, 11) включает:",
         "options": [u"1..10", u"1..11", u"0..10", u"2..11"], "answer": 0},
    ],
)

_register(
    29, u"Складские роботы", u"Сортировка данных, min/max",
    u"Навести порядок на складе контейнеров",
    u"Роботы сортируют ящики по весу: sorted(), min(), max(), реверс. "
    u"Лёгкие — вверх, тяжёлые — к полу.",
    _flow_linear([u"weight = [...]", u"sorted(weight)", u"print(order)"]),
    {"mode": "memory", "lists": {"веса": [42, 17, 88, 5, 63]}},
    [
        {"prompt": u"Отсортируй [42,17,88,5,63] и выведи список",
         "starter": u"", "expect_print": [u"[5, 17, 42, 63, 88]"]},
        {"prompt": u"Выведи max() списка весов (88)", "starter": u"",
         "expect_print": [u"88"]},
        {"prompt": u"sorted(sp, reverse=True) начнётся с 88 — выведи первый",
         "starter": u"", "expect_print": [u"88"]},
    ],
    {"title": u"Инспекция склада", "mode": "console",
     "desc": u"Веса [42,17,88,5,63]. Выведи медиану после сортировки (42).",
     "expect_print": [u"42"]},
    [
        {"q": u"sorted() возвращает:",
         "options": [u"новый отсортированный список", u"изменяет строку",
                     u"число", u"None"], "answer": 0},
        {"q": u"reverse=True означает:",
         "options": [u"по убыванию", u"наоборот строку", u"удвоить",
                     u"паузу"], "answer": 0},
        {"q": u"min([9,3,7]) =", "options": [u"3", u"9", u"7", u"19"],
         "answer": 0},
        {"q": u"Медиана — это:",
         "options": [u"средний элемент сортировки", u"максимум", u"сумма",
                     u"длина"], "answer": 0},
        {"q": u"sp.sort() в отличие от sorted():",
         "options": [u"сортирует на месте", u"удаляет список", u"создаёт "
                     u"копию", u"не работает"], "answer": 0},
    ],
)

_register(
    30, u"Ядро реактора", u"Рекурсия и границы",
    u"Активировать ядро делением секций",
    u"Ядро реактора делит энергию пополам до уровня стабильности. "
    u"Функция зовёт сама себя — рекурсия. Обязателен базовый случай!",
    _flow_linear([], cond=(u"n <= 1?", u"return 1", u"n * core(n-1)")),
    {"mode": "memory", "variables": {"core(5)": 120, "шагов": 5}},
    [
        {"prompt": u"factorial(4) через рекурсию → 24",
         "starter": u"def fact(n):\n    if n <= 1:\n        return 1\n"
                    u"    return n * fact(n - 1)\nprint(fact(4))\n",
         "expect_print": [u"24"]},
        {"prompt": u"Сумма 1..5 рекурсией → 15", "starter": u"",
         "expect_print": [u"15"]},
        {"prompt": u"Без базового случая рекурсия вызовет:",
         "starter": u"try:\n    def bad(): return bad()\n    bad()\n"
                    u"except RecursionError:\n    print('STOP')\n",
         "expect_print": [u"STOP"]},
    ],
    {"title": u"Каскад активации", "mode": "console",
     "desc": u"core(n) = 2*core(n-1), core(0)=1. Выведи core(6) = 64.",
     "expect_print": [u"64"]},
    [
        {"q": u"Рекурсия — функция, которая:",
         "options": [u"вызывает сама себя", u"удалена", u"пишет в файл",
                     u"требует цикла"], "answer": 0},
        {"q": u"Базовый случай нужен, чтобы:",
         "options": [u"остановить вызовы", u"ускорить импорт", u"скрыть "
                     u"ошибку", u"занять память"], "answer": 0},
        {"q": u"fact(3) =", "options": [u"6", u"3", u"9", u"1"], "answer": 0},
        {"q": u"Слишком глубокая рекурсия даёт:",
         "options": ["RecursionError", "SyntaxError", "KeyError", "Timeout"],
         "answer": 0},
        {"q": u"Любую рекурсию можно заменить:",
         "options": [u"циклом", u"словарём", u"срезов", u"print"],
         "answer": 0},
    ],
)

_register(
    31, u"Метеоритная оборона", u"Игровая арка: враги, HP, счёт",
    u"Запустить лазерную турель базы",
    u"Небо над городом закрывают метеориты. Простая аркада: враг падает, "
    u"лазер (Actor) перехватывает по colliderect, у базы HP, у игрока счёт.",
    _flow_linear([u"spawn meteor", u"laser.colliderect?", u"score += 1", ]),
    {"mode": "pgzero", "arena": {"speed": 7}},
    [
        {"prompt": u"hp=3; при попадании hp-=1. Выведи 2",
         "starter": u"hp = 3\nhp -= 1\nprint(hp)\n", "expect_print": [u"2"]},
        {"prompt": u"list(range(0, 10, 3)) → [0, 3, 6, 9]", "starter": u"",
         "expect_print": [u"[0, 3, 6, 9]"]},
        {"prompt": u"Условие поражения: hp <= 0 → выведи 'ПАДЕНИЕ'",
         "starter": u"hp = 0\n", "expect_print": [u"ПАДЕНИЕ"]},
    ],
    {"title": u"Босс: Рой осколков", "mode": "pgzero",
     "desc": u"Перехвати все жёлтые осколки лазером-ровером. "
             u"Столкновение со скалой — провал щита."},
    [
        {"q": u"HP персонажа хранят в:",
         "options": [u"переменной/словаре", u"фоне", u"шрифте", u"курсорe"],
         "answer": 0},
        {"q": u"Перехват снаряда проверяют через:",
         "options": ["colliderect()", "len()", "type()", "split()"],
         "answer": 0},
        {"q": u"Счёт побед увеличивают так:",
         "options": ["score += 1", "score == 1", "score -= 1", "print(score)"],
         "answer": 0},
        {"q": u"Врагов обычно хранят в:",
         "options": [u"списке объектов", u"строке", u"числе", u"модуле"],
         "answer": 0},
        {"q": u"Game over наступает, когда:",
         "options": [u"hp <= 0", u"score > 0", u"fps < 5", u"лист пуст "
                     u"всегда"], "answer": 0},
    ],
)

_register(
    32, u"Городская сеть", u"Графы связей, словари списков",
    u"Соединить районы города оптоволокном",
    u"Районы — узлы, кабели — рёбра. Структура graph={'центр': ['вокзал', "
    u"'порт'], ...}. Обход в ширину считает минимальные километры кабеля.",
    _flow_linear([u"graph = {...}", u"queue = [start]", u"visit neighbors"]),
    {"mode": "memory",
     "variables": {"центр": "['вокзал', 'порт']", "вокзал": "['ферма']"}},
    [
        {"prompt": u"Словарь смежности: выведи graph['центр']",
         "starter": u"graph = {'центр': ['вокзал', 'порт']}#",
         "expect_print": [u"['вокзал', 'порт']"]},
        {"prompt": u"Сколько рёбер у {'a':['b','c'],'b':['c']}? выведи 3",
         "starter": u"", "expect_print": [u"3"]},
        {"prompt": u"obhod: for nb in graph['центр']: печатай nb",
         "starter": u"", "expect_print": [u"вокзал", u"порт"]},
    ],
    {"title": u"Магистраль к порту", "mode": "console",
     "desc": u"Кратчайший путь центр→ферма длина 2. Выведи 2.",
     "expect_print": [u"2"]},
    [
        {"q": u"Граф состоит из:",
         "options": [u"вершин и рёбер", u"только чисел", u"строк",
                     u"ошибок"], "answer": 0},
        {"q": u"Смежность районов удобнее хранить в:",
         "options": [u"словаре списков", u"кортеже символов", u"float",
                     u"функции"], "answer": 0},
        {"q": u"Обход «в ширину» идёт по:",
         "options": [u"очереди соседей", u"стеку углубления", u"файлу",
                     u"клавишам"], "answer": 0},
        {"q": u"Ребро соединяет:",
         "options": [u"две вершины", u"два файла", u"цикл и if",
                     u"две строки"], "answer": 0},
        {"q": u"Путь длиной 2 означает:",
         "options": [u"2 ребра между районами", u"2 метра кабеля",
                     u"2 ошибки", u"2 кадра"], "answer": 0},
    ],
)

_register(
    33, u"Диспетчерская", u"Итоговый проект: интеграция систем",
    u"Свести все системы города в один дашборд",
    u"Энергия, кислород, щиты, металл, жильё — всё считается функциями и "
    u"живёт в одном словаре status. Диспетчерская печатает сводку.",
    _flow_linear([u"status = collect()", u"for k,v in status.items():",
                  u"  print(k, v)"]),
    {"mode": "memory",
     "variables": {"энергия": 940, "кислород": 98, "щиты": 100,
                   "металл": 750, "жильё": 12}},
    [
        {"prompt": u"Выведи пары словарь status.items() построчно",
         "starter": u"status = {'энергия': 940, 'кислород': 98}\n",
         "expect_print": [u"энергия 940"]},
        {"prompt": u"Функция ready(status) вернёт True, если все > 50",
         "starter": u"", "expect_print": [u"True"]},
        {"prompt": u"Посчитай сумму ресурсов словаря → выведи число",
         "starter": u"", "expect_print": None},
    ],
    {"title": u"Готовность города", "mode": "console",
     "desc": u"Собери статус из 4 систем и выведи 'ГОТОВ', если минимум > 90.",
     "expect_print": [u"ГОТОВ"]},
    [
        {"q": u"status.items() перебирает:",
         "options": [u"пары (ключ, значение)", u"ключи", u"значения",
                     u"длины"], "answer": 0},
        {"q": u"Дашборд — это:",
         "options": [u"панель показателей", u"вид шрифта", u"тип цикла",
                     u"файл сохранений"], "answer": 0},
        {"q": u"all(x > 50 for x in vals) вернёт True, когда:",
         "options": [u"все значения > 50", u"хотя бы одно", u"первое",
                     u"список пуст"], "answer": 0},
        {"q": u"Минимум списка считает:",
         "options": ["min()", "low()", "floor()", "first()"], "answer": 0},
        {"q": u"Интеграция систем означает:",
         "options": [u"системы обмениваются данными", u"все в одном файле "
                     u"навсегда", u"отключение лишнего", u"переименование"],
         "answer": 0},
    ],
)

_register(
    34, u"Посадка корабля переселенцев", u"Финальная миссия, защитные проверки",
    u"Принять корабль колонистов и завершить программу",
    u"Через 34 урока Нова-Терра готова. Задача финала: проверить готовность "
    u"всех систем (try/except, словари, циклы) и рассчитать посадочную "
    u"траекторию корабля. После успешной посадки — город встречает гостей.",
    _flow_linear([u"check systems", u"all ok?", u"traj = calc()",
                  u"print('ДОБРО ПОЖАЛОВАТЬ')"]),
    {"mode": "pgzero", "arena": {"speed": 6}},
    [
        {"prompt": u"systems={'shield':True,'o2':True,'fuel':True}. "
                   u"Выведи all(systems.values())",
         "starter": u"", "expect_print": [u"True"]},
        {"prompt": u"Высота h=1000, снижение 25/сек: while h>0 печатай шаги. "
                   u"Последняя строка 0",
         "starter": u"", "expect_print": [u"0"]},
        {"prompt": u"Выведи 'ДОБРО ПОЖАЛОВАТЬ, НОВА-ТЕРРА!'",
         "starter": u"", "expect_print": [u"ДОБРО ПОЖАЛОВАТЬ, НОВА-ТЕРРА!"]},
    ],
    {"title": u"ФИНАЛ: Корабль «Переселенец-1»", "mode": "pgzero",
     "desc": u"Проведи маяк посадки сквозь поле астероидов к космодрому. "
             u"Это финальная миссия курса!"},
    [
        {"q": u"all([...]) истинно, когда:",
         "options": [u"все элементы True", u"один True", u"список непустой",
                     u"есть None"], "answer": 0},
        {"q": u"Плавное снижение обеспечивает:",
         "options": [u"цикл с уменьшением высоты", u"один print",
                     u"словарь", u"import"], "answer": 0},
        {"q": u"Финал проекта — это:",
         "options": [u"посадка корабля переселенцев", u"удаление базы",
                     u"переустановка ПК", u"контрольная без задач"],
         "answer": 0},
        {"q": u"Сколько уроков в полном курсе «Нова-Терра»?",
         "options": [u"34", u"10", u"17", u"50"], "answer": 0},
        {"q": u"Главный вывод курса: программирование — это:",
         "options": [u"пошаговое решение больших задач маленькими",
                     u"заучивание", u"удача", u"только математика"],
         "answer": 0},
    ],
    xp=150,
)


def get_level_description(number):
    """Вернуть словарь-описание уровня 1..34 (или None)."""
    if 1 <= number <= len(LEVELS):
        return LEVELS[number - 1]
    return None
