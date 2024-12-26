import matplotlib.pyplot as plt

def dda_algorithm(x1, y1, x2, y2):
    """Алгоритм ЦДА"""
    points = []
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))
    x_inc = dx / steps
    y_inc = dy / steps
    x, y = x1, y1
    for _ in range(int(steps) + 1):
        points.append((round(x), round(y)))
        x += x_inc
        y += y_inc
    return points

def bresenham_algorithm(x1, y1, x2, y2):
    """Алгоритм Брезенхема"""
    points = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x2 > x1 else -1
    sy = 1 if y2 > y1 else -1
    err = dx - dy
    x, y = x1, y1
    while True:
        points.append((x, y))
        if x == x2 and y == y2:
            break
        e2 = err * 2
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy
    return points

def bresenham_integer_algorithm(x1, y1, x2, y2):
    """Целочисленный алгоритм Брезенхема"""
    points = []
    dx = x2 - x1
    dy = y2 - y1
    sx = 1 if dx > 0 else -1
    sy = 1 if dy > 0 else -1
    dx, dy = abs(dx), abs(dy)
    if dx > dy:
        err = dx // 2
        while x1 != x2:
            points.append((x1, y1))
            err -= dy
            if err < 0:
                y1 += sy
                err += dx
            x1 += sx
        points.append((x1, y1))
    else:
        err = dy // 2
        while y1 != y2:
            points.append((x1, y1))
            err -= dx
            if err < 0:
                x1 += sx
                err += dy
            y1 += sy
        points.append((x1, y1))
    return points

def plot_line(points, title):
    """Функция для отрисовки линии"""
    x, y = zip(*points)
    plt.plot(x, y, marker='o', color='blue', linestyle='-', markersize=3)
    plt.title(title)
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    # Ввод координат
    x1, y1 = map(int, input("Введите координаты начальной точки (x1 y1): ").split())
    x2, y2 = map(int, input("Введите координаты конечной точки (x2 y2): ").split())

    # Алгоритм ЦДА
    dda_points = dda_algorithm(x1, y1, x2, y2)
    plot_line(dda_points, "Алгоритм ЦДА")

    # Алгоритм Брезенхема
    bresenham_points = bresenham_algorithm(x1, y1, x2, y2)
    plot_line(bresenham_points, "Алгоритм Брезенхема")

    # Целочисленный алгоритм Брезенхема
    bresenham_int_points = bresenham_integer_algorithm(x1, y1, x2, y2)
    plot_line(bresenham_int_points, "Целочисленный алгоритм Брезенхема")
