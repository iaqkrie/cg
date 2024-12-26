import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Функции для построения сцены
def draw_scene(ax, scale=10):
    """Рисует координатные оси и масштабную сетку."""
    # Координатные оси
    ax.quiver(0, 0, 0, scale, 0, 0, color='r', label='X')
    ax.quiver(0, 0, 0, 0, scale, 0, color='g', label='Y')
    ax.quiver(0, 0, 0, 0, 0, scale, color='b', label='Z')

    # Сетка
    grid_range = np.linspace(-scale, scale, 11)
    for g in grid_range:
        ax.plot([g, g], [-scale, scale], [0, 0], color='gray', alpha=0.5)
        ax.plot([-scale, scale], [g, g], [0, 0], color='gray', alpha=0.5)
        ax.plot([-scale, scale], [0, 0], [g, g], color='gray', alpha=0.5)

    ax.set_xlim([-scale, scale])
    ax.set_ylim([-scale, scale])
    ax.set_zlim([-scale, scale])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()

# Функция для построения объекта
def create_prism(base_vertices, height):
    """Создает призму на основе базовых вершин и высоты."""
    base = np.array(base_vertices)
    top = base + np.array([0, 0, height])
    vertices = np.vstack((base, top))

    # Соединение вершин для рёбер
    edges = []
    n = len(base)
    for i in range(n):
        edges.append((i, (i + 1) % n))  # Рёбра основания
        edges.append((i + n, (i + 1) % n + n))  # Рёбра верхней грани
        edges.append((i, i + n))  # Рёбра между основаниями

    return vertices, edges

# Функции для расчета коэффициентов плоскости
def calculate_plane_coefficients(vertices, face_indices):
    """Рассчитывает коэффициенты плоскости для заданной грани."""
    p1, p2, p3 = [vertices[i] for i in face_indices]
    normal = np.cross(p2 - p1, p3 - p1)
    a, b, c = normal
    d = -np.dot(normal, p1)
    return a, b, c, d

def check_face_visibility(vertices, face_indices, observer):
    """Проверяет видимость плоскости из заданной точки наблюдения."""
    a, b, c, d = calculate_plane_coefficients(vertices, face_indices)
    normal = np.array([a, b, c])
    observer_vector = observer - vertices[face_indices[0]]
    dot_product = np.dot(normal, observer_vector)
    return dot_product < 0  # Лицевая грань, если отрицательно

# Основная программа
def main():
    # Инициализация фигуры
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # 1. Построение сцены
    scale = 10
    draw_scene(ax, scale)

    # 2. Построение объекта
    base_vertices = [(0, 0, 0), (2, 0, 0), (2, 2, 0), (0, 2, 0)]  # Основание
    height = 3
    vertices, edges = create_prism(base_vertices, height)

    # 3. Расчет плоскостей и проверка видимости
    faces = [(0, 1, 4), (1, 2, 5), (2, 3, 6), (3, 0, 7)]
    observer = np.array([3, 3, 3])  # Точка наблюдения
    for face in faces:
        visible = check_face_visibility(vertices, face, observer)
        print(f"Грань {face} {'лицевая' if visible else 'нелицевая'}.")

    # 4. Отображение объекта
    for edge in edges:
        x = [vertices[edge[0]][0], vertices[edge[1]][0]]
        y = [vertices[edge[0]][1], vertices[edge[1]][1]]
        z = [vertices[edge[0]][2], vertices[edge[1]][2]]
        ax.plot(x, y, z, color='b')

    plt.show()

# Запуск программы
if __name__ == "__main__":
    main()
