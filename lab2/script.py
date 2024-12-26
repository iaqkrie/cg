import matplotlib.pyplot as plt

def bresenham_circle(cx, cy, radius):
    """Алгоритм Брезенхема для растеризации окружности"""
    points = []
    x = 0
    y = radius
    d = 3 - 2 * radius

    def add_symmetric_points(cx, cy, x, y, points):
        """Добавляет симметричные точки окружности"""
        points.extend([
            (cx + x, cy + y), (cx - x, cy + y),
            (cx + x, cy - y), (cx - x, cy - y),
            (cx + y, cy + x), (cx - y, cy + x),
            (cx + y, cy - x), (cx - y, cy - x)
        ])

    add_symmetric_points(cx, cy, x, y, points)

    while x < y:
        if d < 0:
            d = d + 4 * x + 6
        else:
            d = d + 4 * (x - y) + 10
            y -= 1
        x += 1
        add_symmetric_points(cx, cy, x, y, points)
    return points

def plot_circle(points, title):
    """Функция для отрисовки окружности"""
    x, y = zip(*points)
    plt.figure(figsize=(6, 6))
    plt.scatter(x, y, c='blue', s=10)
    plt.title(title)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    # Ввод координат центра и радиуса
    cx, cy = map(int, input("Введите координаты центра окружности (cx cy): ").split())
    radius = int(input("Введите радиус окружности: "))

    # Алгоритм Брезенхема для окружности
    circle_points = bresenham_circle(cx, cy, radius)
    plot_circle(circle_points, "Алгоритм Брезенхема для окружности")
