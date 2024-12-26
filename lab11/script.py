import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def calculate_bezier_curve(control_points, num_points=100):
    """Рассчитать точки кривой Безье для заданных контрольных точек."""
    n = len(control_points) - 1
    t_values = np.linspace(0, 1, num_points)
    curve_points = np.zeros((num_points, 2))
    for i in range(num_points):
        t = t_values[i]
        point = np.zeros(2)
        for k in range(n + 1):
            bernstein = (math.comb(n, k) * (t ** k) * ((1 - t) ** (n - k)))
            point += bernstein * control_points[k]
        curve_points[i] = point
    return curve_points

def calculate_bezier_surface(control_grid, u_steps=10, v_steps=10):
    """Рассчитать точки поверхности Безье."""
    rows, cols = control_grid.shape[:2]
    u_values = np.linspace(0, 1, u_steps)
    v_values = np.linspace(0, 1, v_steps)
    surface_points = np.zeros((u_steps, v_steps, 3))

    for i, u in enumerate(u_values):
        for j, v in enumerate(v_values):
            point = np.zeros(3)
            for m in range(rows):
                for n in range(cols):
                    bernstein_u = (math.comb(rows - 1, m) * (u ** m) * ((1 - u) ** (rows - 1 - m)))
                    bernstein_v = (math.comb(cols - 1, n) * (v ** n) * ((1 - v) ** (cols - 1 - n)))
                    point += bernstein_u * bernstein_v * control_grid[m, n]
            surface_points[i, j] = point

    return surface_points

def plot_bezier_curve(control_points, curve_points):
    """Отобразить кривую Безье и её контрольные точки."""
    plt.figure(figsize=(8, 6))
    plt.plot(control_points[:, 0], control_points[:, 1], 'ro-', label="Контрольные точки")
    plt.plot(curve_points[:, 0], curve_points[:, 1], 'b-', label="Кривая Безье")
    plt.legend()
    plt.title("Кубическая кривая Безье")
    plt.grid()
    plt.show()

def plot_bezier_surface(control_grid, surface_points):
    """Отобразить поверхность Безье и её контрольную сетку."""
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Отобразить контрольную сетку
    for i in range(control_grid.shape[0]):
        ax.plot(control_grid[i, :, 0], control_grid[i, :, 1], control_grid[i, :, 2], 'ro-')
    for j in range(control_grid.shape[1]):
        ax.plot(control_grid[:, j, 0], control_grid[:, j, 1], control_grid[:, j, 2], 'ro-')

    # Отобразить поверхность
    X = surface_points[:, :, 0]
    Y = surface_points[:, :, 1]
    Z = surface_points[:, :, 2]
    ax.plot_surface(X, Y, Z, color='b', alpha=0.6)

    ax.set_title("Поверхность Безье")
    plt.show()

def calculate_doosabin_surface(vertices, num_iterations=1):
    """Рассчитать точки поверхности Ду-Сабина (схема упрощена)."""
    faces = []
    for i in range(len(vertices)):
        v0 = vertices[i]
        v1 = vertices[(i + 1) % len(vertices)]
        faces.append((v0 + v1) / 2)

    for _ in range(num_iterations):
        new_faces = []
        for i in range(len(faces)):
            v0 = faces[i]
            v1 = faces[(i + 1) % len(faces)]
            new_faces.append((v0 + v1) / 2)
        faces = new_faces

    return np.array(faces)

def plot_doosabin_surface(vertices, result):
    """Отобразить поверхность Ду-Сабина."""
    plt.figure(figsize=(8, 6))
    plt.plot(vertices[:, 0], vertices[:, 1], 'ro-', label="Исходные вершины")
    plt.plot(result[:, 0], result[:, 1], 'b-', label="Поверхность Ду-Сабина")
    plt.legend()
    plt.title("Поверхность Ду-Сабина")
    plt.grid()
    plt.show()

def main():
    while True:
        print("\nВыберите действие:")
        print("1. Построение кривой Безье")
        print("2. Построение поверхности Безье")
        print("3. Построение поверхности Ду-Сабина")
        print("4. Выход")

        choice = input("Введите номер действия: ")

        if choice == "1":
            n = int(input("Введите количество контрольных точек: "))
            control_points = []
            for i in range(n):
                x, y = map(float, input(f"Введите координаты вершины {i + 1} (x y): ").split())
                control_points.append((x, y))
            control_points = np.array(control_points)

            num_points = int(input("Введите количество точек на кривой: "))
            curve_points = calculate_bezier_curve(control_points, num_points)
            plot_bezier_curve(control_points, curve_points)

        elif choice == "2":
            rows = int(input("Введите количество строк контрольной сетки: "))
            cols = int(input("Введите количество столбцов контрольной сетки: "))
            control_grid = []
            for i in range(rows):
                row = []
                for j in range(cols):
                    x, y, z = map(float, input(f"Введите координаты вершины ({i}, {j}) (x y z): ").split())
                    row.append((x, y, z))
                control_grid.append(row)
            control_grid = np.array(control_grid)

            u_steps = int(input("Введите количество шагов по U: "))
            v_steps = int(input("Введите количество шагов по V: "))
            surface_points = calculate_bezier_surface(control_grid, u_steps, v_steps)
            plot_bezier_surface(control_grid, surface_points)

        elif choice == "3":
            n = int(input("Введите количество вершин: "))
            vertices = []
            for i in range(n):
                x, y = map(float, input(f"Введите координаты вершины {i + 1} (x y): ").split())
                vertices.append((x, y))
            vertices = np.array(vertices)

            iterations = int(input("Введите количество итераций: "))
            result = calculate_doosabin_surface(vertices, iterations)
            plot_doosabin_surface(vertices, result)

        elif choice == "4":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
