from prettytable import PrettyTable
from math import sqrt

def dichotomy_search(f, a:int|float, b:int|float, delta:int|float = 1e-5, tol:int|float=1e-4):
    """
    Метод дихотомии (деления пополам)

    δ (delta) > 0
    :return:
    """

    call_count=0
    def call_func(x):
        # Считаем количество вызова математической функции в ходе выполнения алгоритма
        nonlocal call_count
        call_count+=1
        return f(x)

    if delta <= 0:
        raise ValueError("delta должно быть положительным")
    if b <= a:
        if a == b:
            raise ValueError("Промежуток не может быть нулевым. A != B")
        else:
            # Меняем переменные местами
            a = a + b
            b = a - b # b = a_0
            a = a - b # a = b_0

    result_table = PrettyTable()
    result_table.field_names = ["Iter","x⃰ ", "F(x⃰)", "Tol", "current A", "current B", "current C", "current D"]

    iter = 0
    # Условие выхода из цикла неявное, прописано внутри цикла
    while True:
        iter += 1
        c = ((a + b) - delta) / 2
        d = ((a + b) + delta) / 2

        result_table.add_row([
            iter,
            round((a + b) / 2, 5),
            round(f((a + b) / 2), 5),
            round(abs((b - a) / 2), 5),
            round(a, 5), round(b, 5),
            round(c, 5), round(d, 5)
        ])

        # Условие выхода из цикла
        if abs(b - a) <= 2 * tol:
            break

        if call_func(c) <= call_func(d):
            b = d
        else:
            a = c

    x_min = (a + b) / 2

    # Извлекаем траекторию x и погрешность из таблицы
    convergence = [row[1] for row in result_table._rows]
    tolerance = [row[3] for row in result_table._rows]

    print("\033[1m\033[32m\033[40m{}".format("м. Дихотомии (итерационный результат):"))
    print(f"\033[0m\033[40m{result_table}")
    print("\033[1m\033[38m\033[40m{}".format(f"\nДостигнут минимум f(x) = {round(f(x_min), 5)} в точке x = {round(x_min, 5)}"
                                             f"\t|\t eps: {abs(b-a)/2}"))
    print("\033[3m\033[35m\033[40m{}".format(f"Вызовов функции: {call_count}"))

    return convergence, tolerance

def golden_ratio_search(f, a:int|float, b:int|float, tol:int|float=1e-4):
    """
    Метод золотого сечения

    :return:
    """
    def call_func(x):
        # Считаем количество вызова математической функции в ходе выполнения алгоритма
        nonlocal call_count
        call_count += 1
        return f(x)

    if b <= a:
        if a == b:
            raise ValueError("Промежуток не может быть нулевым. A != B")
        else:
            # Меняем переменные местами
            a = a + b
            b = a - b  # b = a_0
            a = a - b  # a = b_0

    call_count = 0

    result_table = PrettyTable()
    result_table.field_names = ["Iter","x⃰ ", "F(x⃰)", "Tol", "current A", "current B", "current C", "current D"]

    iter = 0
    c = ((3 - sqrt(5)) * (b - a)) / 2 + a
    d = ((sqrt(5) - 1) * (b - a)) / 2 + a
    f_c = call_func(c)
    f_d = call_func(d)

    # Условие выхода из цикла неявное, прописано внутри цикла
    while True:
        iter += 1
        result_table.add_row([
            iter,
            round((a + b) / 2, 5),
            round(f((a + b) / 2), 5),
            round(abs((b - a) / 2), 5),
            round(a, 5), round(b, 5),
            round(c, 5), round(d, 5)
        ])

        # Условие выхода из цикла
        if abs(b - a) <= 2 * tol:
            break

        if f_c <= f_d:
            b = d
            d = c
            c = ((3 - sqrt(5)) * (b - a)) / 2 + a
            f_d = f_c
            f_c = call_func(c)

        else:
            a = c
            c = d
            d = ((sqrt(5)-1) * (b - a)) / 2 + a
            f_c = f_d
            f_d = call_func(d)

    x_min = (a+b)/2

    # Извлекаем траекторию x и погрешность из таблицы
    convergence = [row[1] for row in result_table._rows]
    tolerance = [row[3] for row in result_table._rows]

    print("\033[1m\033[32m\033[40m{}".format("м. Золотого Сечения (итерационный результат)"))
    print(f"\033[0m\033[40m{result_table}")
    print("\033[1m\033[38m\033[40m{}".format(
        f"\nДостигнут минимум f(x) = {round(f(x_min), 5)} в точке x = {round(x_min, 5)}"
        f"\t|\t eps: {abs(b - a) / 2}"))
    print("\033[3m\033[35m\033[40m{}".format(f"Вызовов функции: {call_count}"))

    return convergence, tolerance

def directional_search(f, x0: float, h: float = 0.01, tol: float = 1e-4):
    """
    Алгоритм направленного поиска

    :param f:
    :param x0:
    :param h:
    :param tol:
    :return:
    """

    call_count = 0
    def call_func(x):
        # Считаем количество вызова математической функции в ходе выполнения алгоритма
        nonlocal call_count
        call_count += 1
        return f(x)

    def get_phase(h):
        return "Расширение" if h > 0 else "Уточнение"


    if h <= tol:
        raise ValueError("Шаг должен быть больше погрешности. h > tol")

    x_prev = x0
    f_prev = call_func(x_prev)
    iter_count = 0

    result_table = PrettyTable()
    result_table.field_names = ["Iter", "x⃰ ", "F(x⃰)", "|h|", "Фаза"]

    # Первая запись
    result_table.add_row([
        iter_count,
        round(x_prev, 6),
        round(f_prev, 6),
        round(abs(h), 6),
        get_phase(h)
    ])

    while abs(h) > tol:
        x_new = x_prev + h
        f_new = call_func(x_new)

        if f_new < f_prev:
            x_prev, f_prev = x_new, f_new
            h *= 1.2
        else:
            h *= -0.5  # уменьшаем шаг и меняем направление

        iter_count += 1
        result_table.add_row([
            iter_count,
            round(x_prev, 6),
            round(f_prev, 6),
            round(abs(h), 6),
            get_phase(h)
        ])

    # Извлекаем траекторию x и погрешность из таблицы
    convergence = [row[1] for row in result_table._rows]
    tolerance = [row[3] for row in result_table._rows]

    # Печать таблицы и результат
    print("\033[1m\033[32m\033[40mМетод направленного поиска (итерационный результат):\033[0m")
    print(f"\033[0m\033[40m{result_table}")
    print("\033[1m\033[38m\033[40m{}".format(
        f"\nДостигнут минимум f(x) = {round(x_prev, 5)} в точке x = {round(f_prev, 5)}"
        f"\t|\t eps: {abs(h)}"))
    print("\033[3m\033[35m\033[40m{}".format(f"Вызовов функции: {call_count}"))

    return convergence, tolerance

def sectant_search(f, df, x0:int|float, x1:int|float, tol:int|float=1e-4):
    """
    Метод секущих (хорд)

    :param f: гладкая функция
    :param df: производная функции
    :param x0:
    :param x1:
    :param tol: допустимая погрешность
    :return convergence: список приближений
    """

    call_count = 0
    def call_dfunc(x):
        nonlocal call_count
        call_count += 1
        return df(x)

    result_table = PrettyTable()
    result_table.field_names = ["Iter", "x⃰ ", "F(x⃰)", "df(x⃰)","|x0-x1|","x0", "x1", "d0", "d1"]

    iter_count = 0
    result_table.add_row(
        [iter_count, "-", "-", "-", "-", round(x0, 5),
         round(x1, 5), round(df(x0), 5), round(df(x1), 5)])

    # В качестве критерия остановки можно использовать abs(x1-x0)
    while abs(call_dfunc(x1)) > tol:
        iter_count += 1
        d0, d1 = call_dfunc(x0), call_dfunc(x1)
        x0, x1 = x1, x1 - (d1 * (x1 - x0) / (d1 - d0))
        result_table.add_row([iter_count, round(x1, 4), round(f(x1), 4), round(df(x1), 10), round(abs(x0-x1), 10), round(x0, 4),round(x1, 4),round(df(x0), 4),round(df(x1), 4)])

    convergence = [row[1] for row in result_table._rows]
    tolerance = [row[3] for row in result_table._rows]

    print("\033[1m\033[32m\033[40mМетод хорд] (итерационный результат):\033[0m")
    print(f"\033[0m\033[40m{result_table}")
    print("\033[1m\033[38m\033[40m{}".format(
        f"\nДостигнут минимум f(x) = {round(f(x1), 5)} в точке x = {round(x1, 5)}"
        f"\t|\t eps: {abs(df(x1))}"))
    print("\033[3m\033[35m\033[40m{}".format(f"Вызовов функции: {call_count}"))

    return convergence, tolerance