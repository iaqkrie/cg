import numpy as np
from PIL import Image

def affine_transform(image, scale=(1, 1), translate=(0, 0)):
    """Аффинное преобразование: масштабирование и перенос."""
    width, height = image.size
    new_width = int(width * scale[0])
    new_height = int(height * scale[1])

    # Создаём пустое изображение
    transformed_image = Image.new("RGB", (new_width, new_height))
    pixels_original = image.load()
    pixels_transformed = transformed_image.load()

    # Преобразование координат
    for x in range(new_width):
        for y in range(new_height):
            src_x = int((x - translate[0]) / scale[0])
            src_y = int((y - translate[1]) / scale[1])
            if 0 <= src_x < width and 0 <= src_y < height:
                pixels_transformed[x, y] = pixels_original[src_x, src_y]
    
    return transformed_image

def inverse_affine_transform(image, scale=(1, 1), translate=(0, 0), original_size=(0, 0)):
    """Обратное аффинное преобразование."""
    width, height = original_size
    transformed_width, transformed_height = image.size

    # Создаём пустое изображение
    restored_image = Image.new("RGB", (width, height))
    pixels_transformed = image.load()
    pixels_restored = restored_image.load()

    # Преобразование координат
    for x in range(width):
        for y in range(height):
            src_x = int(x * scale[0] + translate[0])
            src_y = int(y * scale[1] + translate[1])
            if 0 <= src_x < transformed_width and 0 <= src_y < transformed_height:
                pixels_restored[x, y] = pixels_transformed[src_x, src_y]
    
    return restored_image

def nonlinear_transform(image):
    """Нелинейное преобразование: i = 2^x', j = y'."""
    width, height = image.size
    new_width = int(2 ** (width - 1).bit_length())  # Определяем минимальную степень 2
    new_height = height

    # Создаём пустое изображение
    transformed_image = Image.new("RGB", (new_width, new_height))
    pixels_original = image.load()
    pixels_transformed = transformed_image.load()

    # Преобразование координат
    for x in range(width):
        for y in range(height):
            transformed_x = int(2 ** x) if 2 ** x < new_width else new_width - 1
            transformed_y = y
            pixels_transformed[transformed_x, transformed_y] = pixels_original[x, y]
    
    return transformed_image

def main():
    # Пути к файлам
    input_image_path = "input.jpg"
    affine_transformed_path = "affine_transformed.jpg"
    restored_image_path = "restored_image.jpg"
    nonlinear_transformed_path = "nonlinear_transformed.jpg"

    # Чтение изображения
    image = Image.open(input_image_path).convert("RGB")

    # Аффинные преобразования (масштабирование и перенос)
    scale = (1.5, 1.5)  # Масштабирование по X и Y
    translate = (50, 50)  # Перенос на 50 пикселей вправо и вниз
    affine_transformed_image = affine_transform(image, scale, translate)
    affine_transformed_image.save(affine_transformed_path)
    print(f"Аффинное преобразование выполнено, результат сохранён в {affine_transformed_path}")

    # Восстановление изображения
    restored_image = inverse_affine_transform(affine_transformed_image, scale, translate, image.size)
    restored_image.save(restored_image_path)
    print(f"Исходное изображение восстановлено, результат сохранён в {restored_image_path}")

    # Нелинейное преобразование
    nonlinear_transformed_image = nonlinear_transform(image)
    nonlinear_transformed_image.save(nonlinear_transformed_path)
    print(f"Нелинейное преобразование выполнено, результат сохранён в {nonlinear_transformed_path}")

if __name__ == "__main__":
    main()
