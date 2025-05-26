from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np


def default_chart(f):
    x = np.linspace(-2, 2, 400)
    y = f(x)

    fig, ax = plt.subplots()
    ax.plot(x, y, label="y = 19x⁴ + 10x² + 10x")
    ax.legend(loc='lower right')

    # Перемещение осей в центр
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')

    # Удаление верхней и правой осей
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    # Стрелки на концах осей
    ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
    ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)

    # Сетка и подписи
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_title("График исходной функции")
    ax.set_xlim([-3, 3])
    ax.set_ylim([-4, 15])
    plt.show()

def conv_tol_chart(f, conv_array: list, tol: list, method: str):
    # Создаем фигуру с constrained_layout=True
    fig = plt.figure(constrained_layout=True, figsize=(14, 6))
    gs = fig.add_gridspec(2, 2, width_ratios=[2.5, 1], height_ratios=[1, 1])

    x_range = np.linspace(-2, 2, 400)
    y_range = f(x_range)

    # Цветовая карта для стрелок итераций
    colors = plt.cm.viridis(np.linspace(0, 1, len(conv_array)))

    # === График 1: обычная функция + 6 первых итераций ===
    ax1 = fig.add_subplot(gs[:, 0])
    ax1.plot(x_range, y_range, label="y = 19x⁴ + 10x² + 10x", color='steelblue')
    ax1.set_title(f"Приближения : {method} (первые 6)")

    for i, x_i in enumerate(conv_array[:6]):
        y_i = f(x_i)
        ax1.plot(x_i, y_i, marker='*', color=colors[i], markersize=12)
        ax1.annotate(
            f"{i}",
            xy=(x_i, y_i),
            xytext=(x_i, y_i + 0.15 * (i + 1)),
            arrowprops=dict(arrowstyle='->', color=colors[i]),
            fontsize=9,
            color=colors[i],
            ha='center'
        )
    ax1.spines['left'].set_position('zero')
    ax1.spines['bottom'].set_position('zero')
    ax1.spines['right'].set_color('none')
    ax1.spines['top'].set_color('none')
    ax1.plot(1, 0, ">k", transform=ax1.get_yaxis_transform(), clip_on=False)
    ax1.plot(0, 1, "^k", transform=ax1.get_xaxis_transform(), clip_on=False)
    ax1.grid(True, linestyle='--', alpha=0.5)
    ax1.set_xlim([-2, 2])
    ax1.set_ylim([-3, 6])
    ax1.legend(loc='lower right')

    # === График 2: все приближения (фокус на экстремум) ===
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(x_range, y_range, label="y = 19x⁴ + 10x² + 10x", color='steelblue')
    ax2.set_title("Все приближения (масштаб для лучшей видимости)")

    for i, x_i in enumerate(conv_array):
        y_i = f(x_i)
        ax2.plot(x_i, y_i, marker='*', color=colors[i], markersize=10)
        ax2.annotate(
            f"{i}",
            xy=(x_i, y_i),
            xytext=(x_i + 0.01, y_i - 0.02),
            arrowprops=dict(arrowstyle='->', color=colors[i]),
            fontsize=8,
            color=colors[i],
            ha='left'
        )
    ax2.set_xlim([-0.5, 0])
    ax2.set_ylim([-2.1, -1.7])
    ax2.grid(True, linestyle='--', alpha=0.5)
    ax2.spines['left'].set_position('zero')
    ax2.spines['bottom'].set_position('zero')
    ax2.spines['right'].set_color('none')
    ax2.spines['top'].set_color('none')
    ax2.plot(1, 0, ">k", transform=ax2.get_yaxis_transform(), clip_on=False)
    ax2.plot(0, 1, "^k", transform=ax2.get_xaxis_transform(), clip_on=False)
    ax2.set_xlabel("x")

    # === График 3: логарифмическая ошибка ===
    ax3 = fig.add_subplot(gs[1, 1])
    # Создаем ось X как номера итераций (начиная с 1)
    ax3.plot(range(1, len(tol)+1), tol, marker='o', color='darkorange', label='|current tolerance|')
    ax3.set_yscale('log')
    ax3.set_title("Сходимость по погрешности (log scale)")
    ax3.set_xlabel("Итерация")
    ax3.set_ylabel("Ошибка")
    ax3.grid(True, which='both', linestyle='--', alpha=0.5)
    ax3.legend()


    # Сохраняем картинку
    plt.savefig(f"charts_png/{({'м. Дихотомии':'dichotomy', 'м. Золотого сечения':'goldenratio', 'м. Направленного поиска':'directional', 'м. Хорд':'sectant'})[method]}.png",
                dpi=150)
    plt.close()