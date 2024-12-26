import cv2
import numpy as np
from matplotlib import pyplot as plt

def apply_low_pass_filter(image, radius):
    """Применяет фильтр низких частот: размытие за пределами круга радиуса R."""
    # Создаем маску: область внутри круга - 1, за пределами - 0
    rows, cols = image.shape[:2]
    center = (cols // 2, rows // 2)
    mask = np.zeros((rows, cols), dtype=np.uint8)
    cv2.circle(mask, center, radius, 255, -1)

    # Применяем Гауссово размытие
    blurred = cv2.GaussianBlur(image, (15, 15), 0)

    # Комбинируем: область вне круга - размытая, внутри - оригинал
    result = np.copy(image)
    result[mask == 0] = blurred[mask == 0]

    return result

def apply_high_pass_filter(image, threshold):
    """Применяет фильтр высоких частот: повышает резкость в районе пикселей с яркостью > T."""
    # Преобразуем изображение в оттенки серого
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Находим области с яркостью выше порога
    mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)[1]

    # Применяем фильтр резкости (ядро повышения резкости)
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]], dtype=np.float32)
    sharpened = cv2.filter2D(image, -1, kernel)

    # Комбинируем: для маски (> T) используем резкое изображение, остальное оставляем оригинальным
    result = np.copy(image)
    result[mask > 0] = sharpened[mask > 0]

    return result

def main():
    # Загружаем изображение
    image_path = "input.jpg"
    image = cv2.imread(image_path)
    if image is None:
        print("Ошибка: изображение не найдено.")
        return

    # Ввод параметров
    radius = int(input("Введите радиус R для фильтра низких частот: "))
    threshold = int(input("Введите порог T для фильтра высоких частот: "))

    # Применяем фильтры
    low_pass_result = apply_low_pass_filter(image, radius)
    high_pass_result = apply_high_pass_filter(image, threshold)

    # Отображаем результаты
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 3, 1)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title("Исходное изображение")
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.imshow(cv2.cvtColor(low_pass_result, cv2.COLOR_BGR2RGB))
    plt.title(f"Фильтр низких частот (R={radius})")
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.imshow(cv2.cvtColor(high_pass_result, cv2.COLOR_BGR2RGB))
    plt.title(f"Фильтр высоких частот (T={threshold})")
    plt.axis('off')

    plt.tight_layout()
    plt.show()

    # Сохранение результатов
    cv2.imwrite("low_pass_result.png", low_pass_result)
    cv2.imwrite("high_pass_result.png", high_pass_result)
    print("Результаты сохранены как 'low_pass_result.png' и 'high_pass_result.png'.")

if __name__ == "__main__":
    main()
