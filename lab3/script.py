from PIL import Image

def invert_pixel(pixel):
    """Инверсия цвета одного пикселя (R, G, B)."""
    r, g, b = pixel
    return 255 - r, 255 - g, 255 - b

def invert_image(image):
    """Попиксельная обработка: инверсия цветов всего изображения."""
    width, height = image.size
    pixels = image.load()

    for x in range(width):
        for y in range(height):
            pixels[x, y] = invert_pixel(pixels[x, y])

    return image

def blend_images(image1, image2, alpha=0.5):
    """
    Наложение двух изображений вручную.
    - image1, image2: изображения одинакового размера.
    - alpha: коэффициент смешивания (0 - только image1, 1 - только image2).
    """
    if image1.size != image2.size:
        raise ValueError("Размеры изображений должны совпадать!")

    width, height = image1.size
    pixels1 = image1.load()
    pixels2 = image2.load()

    # Результирующее изображение
    blended_image = Image.new("RGB", (width, height))
    blended_pixels = blended_image.load()

    for x in range(width):
        for y in range(height):
            r1, g1, b1 = pixels1[x, y]
            r2, g2, b2 = pixels2[x, y]

            # Смешивание цветов пикселей
            blended_pixels[x, y] = (
                int(r1 * (1 - alpha) + r2 * alpha),
                int(g1 * (1 - alpha) + g2 * alpha),
                int(b1 * (1 - alpha) + b2 * alpha)
            )

    return blended_image

def main():
    # Пути к файлам
    input_image1_path = "input1.jpg"
    input_image2_path = "input2.jpg"
    output_inverted_path = "inverted_image.jpg"
    output_blended_path = "blended_image.jpg"

    # Чтение изображений
    image1 = Image.open(input_image1_path).convert("RGB")
    image2 = Image.open(input_image2_path).convert("RGB")

    # Попиксельная обработка: инверсия цветов
    inverted_image = invert_image(image1.copy())
    inverted_image.save(output_inverted_path)
    print(f"Обработанное изображение сохранено как {output_inverted_path}")

    # Наложение изображений
    blended_image = blend_images(image1, image2, alpha=0.5)
    blended_image.save(output_blended_path)
    print(f"Наложенное изображение сохранено как {output_blended_path}")

if __name__ == "__main__":
    main()
