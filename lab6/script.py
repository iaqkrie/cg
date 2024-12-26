import matplotlib.pyplot as plt

# Кодовые области для алгоритма Коэна-Сазерленда
INSIDE = 0  # Внутри окна
LEFT = 1    # Слева от окна
RIGHT = 2   # Справа от окна
BOTTOM = 4  # Ниже окна
TOP = 8     # Выше окна

def compute_out_code(x, y, x_min, x_max, y_min, y_max):
    """Вычисляет кодовую область точки."""
    code = INSIDE
    if x < x_min:  # Слева от окна
        code |= LEFT
    elif x > x_max:  # Справа от окна
        code |= RIGHT
    if y < y_min:  # Ниже окна
        code |= BOTTOM
    elif y > y_max:  # Выше окна
        code |= TOP
    return code

def cohen_sutherland_clip(x1, y1, x2, y2, x_min, x_max, y_min, y_max):
    """Алгоритм Коэна-Сазерленда для отсечения отрезков."""
    out_code1 = compute_out_code(x1, y1, x_min, x_max, y_min, y_max)
    out_code2 = compute_out_code(x2, y2, x_min, x_max, y_min, y_max)
    accept = False

    while True:
        if not (out_code1 | out_code2):
            # Если оба конца внутри окна
            accept = True
            break
        elif out_code1 & out_code2:
            # Если оба конца снаружи окна в одном регионе
            break
        else:
            # Отсечь часть отрезка
            x, y = 0, 0
            out_code_out = out_code1 if out_code1 else out_code2

            if out_code_out & TOP:
                x = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1)
                y = y_max
            elif out_code_out & BOTTOM:
                x = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1)
                y = y_min
            elif out_code_out & RIGHT:
                y = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1)
                x = x_max
            elif out_code_out & LEFT:
                y = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1)
                x = x_min

            if out_code_out == out_code1:
                x1, y1 = x, y
                out_code1 = compute_out_code(x1, y1, x_min, x_max, y_min, y_max)
            else:
                x2, y2 = x, y
                out_code2 = compute_out_code(x2, y2, x_min, x_max, y_min, y_max)

    if accept:
        return [(x1, y1), (x2, y2)]
    else:
        return None

def plot_clipping(lines, x_min, x_max, y_min, y_max):
    """Отображение отсечённых отрезков."""
    fig, ax = plt.subplots()

    # Рисуем окно
    ax.plot([x_min, x_max, x_max, x_min, x_min], 
            [y_min, y_min, y_max, y_max, y_min], 'r-', label='Окно')

    # Рисуем исходные отрезки
    for line in lines:
        x1, y1, x2, y2 = line
        ax.plot([x1, x2], [y1, y2], 'b--', label='Исходный отрезок' if line == lines[0] else "")

    # Отсекаем и рисуем отсечённые отрезки
    for line in lines:
        x1, y1, x2, y2 = line
        clipped_line = cohen_sutherland_clip(x1, y1, x2, y2, x_min, x_max, y_min, y_max)
        if clipped_line:
            (cx1, cy1), (cx2, cy2) = clipped_line
            ax.plot([cx1, cx2], [cy1, cy2], 'g-', label='Отсечённый отрезок' if line == lines[0] else "")

    ax.legend()
    ax.set_xlim(min(x_min, -10), max(x_max, 10))
    ax.set_ylim(min(y_min, -10), max(y_max, 10))
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True)
    plt.show()

def main():
    # Ввод данных
    n = int(input("Введите количество отрезков: "))
    lines = []
    for i in range(n):
        x1, y1 = map(float, input(f"Введите координаты начала отрезка {i + 1} (x1 y1): ").split())
        x2, y2 = map(float, input(f"Введите координаты конца отрезка {i + 1} (x2 y2): ").split())
        lines.append((x1, y1, x2, y2))

    x_min, y_min = map(float, input("Введите координаты нижнего левого угла окна (x_min y_min): ").split())
    x_max, y_max = map(float, input("Введите координаты верхнего правого угла окна (x_max y_max): ").split())

    # Отображение отсечения
    plot_clipping(lines, x_min, x_max, y_min, y_max)

if __name__ == "__main__":
    main()
