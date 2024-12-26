import matplotlib.pyplot as plt
import numpy as np

def inside(p, edge_start, edge_end):
    """Проверяет, находится ли точка внутри отсекателя относительно ребра."""
    return (edge_end[0] - edge_start[0]) * (p[1] - edge_start[1]) - (edge_end[1] - edge_start[1]) * (p[0] - edge_start[0]) >= 0

def intersect(s, p, edge_start, edge_end):
    """Находит точку пересечения двух отрезков."""
    dx1, dy1 = p[0] - s[0], p[1] - s[1]
    dx2, dy2 = edge_end[0] - edge_start[0], edge_end[1] - edge_start[1]
    det = dx1 * dy2 - dy1 * dx2

    if det == 0:
        return None  # Отрезки параллельны

    t = ((s[0] - edge_start[0]) * dy2 - (s[1] - edge_start[1]) * dx2) / det
    return s[0] + t * dx1, s[1] + t * dy1

def sutherland_hodgman(subject_polygon, clip_polygon):
    """Реализует алгоритм Сазерленда-Ходжмана для отсечения многоугольника."""
    output_list = subject_polygon

    for i in range(len(clip_polygon)):
        edge_start = clip_polygon[i]
        edge_end = clip_polygon[(i + 1) % len(clip_polygon)]
        input_list = output_list
        output_list = []

        s = input_list[-1]  # Последняя точка из входного списка

        for p in input_list:
            if inside(p, edge_start, edge_end):
                if not inside(s, edge_start, edge_end):
                    output_list.append(intersect(s, p, edge_start, edge_end))
                output_list.append(p)
            elif inside(s, edge_start, edge_end):
                output_list.append(intersect(s, p, edge_start, edge_end))
            s = p

    return output_list

def draw_polygon(polygon, color='blue', linestyle='-', fill=False):
    """Рисует многоугольник."""
    if len(polygon) > 0:
        polygon = np.array(polygon + [polygon[0]])  # Замыкаем контур
        if fill:
            plt.fill(polygon[:, 0], polygon[:, 1], color=color, alpha=0.5)
        else:
            plt.plot(polygon[:, 0], polygon[:, 1], linestyle, color=color, linewidth=1.5)

def main():
    # Ввод координат многоугольника
    n = int(input("Введите количество вершин многоугольника: "))
    print("Введите координаты вершин многоугольника (x y):")
    subject_polygon = [tuple(map(float, input(f"Вершина {i+1}: ").split())) for i in range(n)]

    # Ввод отсеивающего окна
    m = int(input("Введите количество вершин отсеивающего окна: "))
    print("Введите координаты вершин отсеивающего окна (x y):")
    clip_polygon = [tuple(map(float, input(f"Вершина {i+1}: ").split())) for i in range(m)]

    # Выполняем отсечение
    clipped_polygon = sutherland_hodgman(subject_polygon, clip_polygon)

    # Рисуем результат
    plt.figure(figsize=(8, 8))
    plt.title("Отсечение многоугольника выпуклым окном")

    # Исходный многоугольник (пунктирная линия)
    draw_polygon(subject_polygon, color='gray', linestyle='--', fill=False)

    # Отсекающее окно
    draw_polygon(clip_polygon, color='orange', linestyle='-', fill=False)

    # Отсечённая часть многоугольника (закрашенная область)
    if clipped_polygon:
        draw_polygon(clipped_polygon, color='green', fill=True)

    # Добавляем оси и сетку
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

if __name__ == "__main__":
    main()
