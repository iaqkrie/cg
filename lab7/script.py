import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

def scale_and_rotate_image(image, size, target_width, target_height, rotation_angle=45):
    """Масштабирует, поворачивает и позиционирует изображение."""
    width, height = size
    cx, cy = width // 2, height // 2  # Центр изображения

    # Масштабируем изображение до прямоугольника
    resized_image = image.resize((target_width, target_height), resample=Image.Resampling.LANCZOS)

    # Поворачиваем изображение на заданный угол
    rotated_image = resized_image.rotate(rotation_angle, expand=True)

    # Смещение: центрируем верхний край изображения в центре координат
    rotated_width, rotated_height = rotated_image.size
    position = (cx - rotated_width // 2, cy - rotated_height // 4)

    # Создаем новый холст с белым фоном и размещаем изображение
    new_image = Image.new("RGBA", size, "white")
    new_image.paste(rotated_image, position, rotated_image if rotated_image.mode == "RGBA" else None)

    return new_image

def draw_axes(image, color="black"):
    """Рисует оси координат на изображении."""
    draw = ImageDraw.Draw(image)
    width, height = image.size
    cx, cy = width // 2, height // 2

    # Горизонтальная ось
    draw.line([(0, cy), (width, cy)], fill=color, width=2)
    # Вертикальная ось
    draw.line([(cx, 0), (cx, height)], fill=color, width=2)

def draw_cosine_function(image, color="red"):
    """Рисует график cos(x) на изображении."""
    draw = ImageDraw.Draw(image)
    width, height = image.size

    # Генерируем точки для графика
    x_values = np.linspace(0, width, 1000)
    y_values = height // 2 - (np.cos((x_values / width) * 4 * np.pi) * (height // 4))  # Масштабирование cos(x)

    # Соединяем точки
    points = [(x, y) for x, y in zip(x_values, y_values)]
    draw.line(points, fill=color, width=2)

def main():
    # Размер итогового изображения
    size = (400, 400)

    # Задаём размеры прямоугольника (например, 80x40 пикселей)
    target_width, target_height = 80, 40

    # Загружаем изображение
    input_path = "input.jpg"
    try:
        original_image = Image.open(input_path).convert("RGBA")
    except FileNotFoundError:
        print("Файл изображения не найден. Пожалуйста, загрузите файл.")
        return

    # Обрабатываем изображение
    final_image = scale_and_rotate_image(original_image, size, target_width, target_height)

    # Рисуем оси координат
    draw_axes(final_image)

    # Рисуем график cos(x)
    draw_cosine_function(final_image)

    # Отображаем результат
    plt.imshow(final_image)
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    main()
