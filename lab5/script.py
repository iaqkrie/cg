import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3DCollection


def create_cube():
    """Создаёт вершины и рёбра каркасного куба."""
    vertices = np.array([
        [-1, -1, -1],
        [-1, -1,  1],
        [-1,  1, -1],
        [-1,  1,  1],
        [ 1, -1, -1],
        [ 1, -1,  1],
        [ 1,  1, -1],
        [ 1,  1,  1],
    ])

    edges = [
        (0, 1), (0, 2), (0, 4),  # Из вершины 0
        (1, 3), (1, 5),  # Из вершины 1
        (2, 3), (2, 6),  # Из вершины 2
        (3, 7),  # Из вершины 3
        (4, 5), (4, 6),  # Из вершины 4
        (5, 7),  # Из вершины 5
        (6, 7)   # Из вершины 6
    ]

    return vertices, edges


def create_dodecahedron():
    """Создаёт вершины и рёбра каркасного додекаэдра."""
    phi = (1 + np.sqrt(5)) / 2  # Золотое сечение

    # Вершины додекаэдра
    vertices = np.array([
        [-1, -1, -1], [1, -1, -1], [-1, 1, -1], [1, 1, -1],  # Нижняя и верхняя основания
        [-1, -1, 1], [1, -1, 1], [-1, 1, 1], [1, 1, 1],  # Нижняя и верхняя основания
        [0, -1/phi, -phi], [0, -1/phi, phi], [0, 1/phi, -phi], [0, 1/phi, phi],  # Углы
        [-1/phi, -phi, 0], [1/phi, -phi, 0], [-1/phi, phi, 0], [1/phi, phi, 0], 
        [-phi, 0, -1/phi], [phi, 0, -1/phi], [-phi, 0, 1/phi], [phi, 0, 1/phi]
    ])

    # Рёбра додекаэдра (индексы вершин)
    edges = [
        (0, 8), (0, 12), (0, 16),  # Из вершины 0
        (1, 8), (1, 13), (1, 17),  # Из вершины 1
        (2, 10), (2, 14), (2, 16), # Из вершины 2
        (3, 10), (3, 15), (3, 17), # Из вершины 3
        (4, 9), (4, 12), (4, 18),  # Из вершины 4
        (5, 9), (5, 13), (5, 19),  # Из вершины 5
        (6, 11), (6, 14), (6, 18), # Из вершины 6
        (7, 11), (7, 15), (7, 19), # Из вершины 7
        (8, 10), (9, 11), (12, 13), (14, 15), (16, 18), (17, 19) # Рёбра между соседними вершинами
    ]

    return vertices, edges


def plot_polyhedron(vertices, edges, ax, color="blue"):
    """Рисует каркасное изображение многогранника и подписывает вершины."""
    lines = [(vertices[start], vertices[end]) for start, end in edges]
    line_collection = Line3DCollection(lines, colors=color, linewidths=1)

    ax.add_collection3d(line_collection)

    # Подписываем вершины
    for i, vertex in enumerate(vertices):
        ax.text(vertex[0], vertex[1], vertex[2], f"{i}", color="red", fontsize=10, ha='right')

    ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2], color="red", s=10)


def main():
    # Создаём фигуру
    fig = plt.figure(figsize=(10, 5))

    # Добавляем график для куба
    ax_cube = fig.add_subplot(121, projection="3d")
    vertices_cube, edges_cube = create_cube()
    plot_polyhedron(vertices_cube, edges_cube, ax_cube, color="blue")
    ax_cube.set_title("Куб")
    ax_cube.set_box_aspect([1, 1, 1])

    # Добавляем график для додекаэдра
    ax_dodecahedron = fig.add_subplot(122, projection="3d")
    vertices_dodecahedron, edges_dodecahedron = create_dodecahedron()
    plot_polyhedron(vertices_dodecahedron, edges_dodecahedron, ax_dodecahedron, color="green")
    ax_dodecahedron.set_title("Додекаэдр")
    ax_dodecahedron.set_box_aspect([1, 1, 1])

    # Установка пределов для осей
    for ax in [ax_cube, ax_dodecahedron]:
        ax.set_xlim([-2, 2])
        ax.set_ylim([-2, 2])
        ax.set_zlim([-2, 2])
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

    # Отображаем графики
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
