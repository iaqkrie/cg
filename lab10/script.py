import cv2
import numpy as np
from matplotlib import pyplot as plt

def apply_affine_transformation(image, transformation_matrix, interpolation):
    """
    Применяет аффинное преобразование к изображению с заданной матрицей и методом интерполяции.
    """
    rows, cols = image.shape[:2]
    transformed = cv2.warpAffine(image, transformation_matrix, (cols, rows), flags=interpolation)
    return transformed

def main():
    # Загружаем изображение
    image_path = "input.jpg"
    image = cv2.imread(image_path)
    if image is None:
        print("Ошибка: изображение не найдено.")
        return

    rows, cols = image.shape[:2]

    # Аффинные преобразования
    # 1. Масштабирование
    scale_x = float(input("Введите коэффициент масштабирования по оси X: "))
    scale_y = float(input("Введите коэффициент масштабирования по оси Y: "))
    scaling_matrix = np.array([[scale_x, 0, 0],
                                [0, scale_y, 0]], dtype=np.float32)

    # 2. Поворот
    angle = float(input("Введите угол поворота (в градусах): "))
    rotation_matrix = cv2.getRotationMatrix2D((cols // 2, rows // 2), angle, 1)

    # 3. Скос
    skew_x = float(input("Введите коэффициент скоса по оси X: "))
    skew_y = float(input("Введите коэффициент скоса по оси Y: "))
    skew_matrix = np.array([[1, skew_x, 0],
                            [skew_y, 1, 0]], dtype=np.float32)

    # Применение преобразований с различными методами интерполяции
    interpolation_methods = {
        "Ближайший сосед": cv2.INTER_NEAREST,
        "Линейная интерполяция": cv2.INTER_LINEAR,
        "Кубическая интерполяция": cv2.INTER_CUBIC
    }

    # Отображение результатов
    plt.figure(figsize=(12, 12))
    plt.subplot(3, 4, 1)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title("Исходное изображение")
    plt.axis('off')

    idx = 2
    for name, interpolation in interpolation_methods.items():
        # Масштабирование
        scaled_image = apply_affine_transformation(image, scaling_matrix, interpolation)
        plt.subplot(3, 4, idx)
        plt.imshow(cv2.cvtColor(scaled_image, cv2.COLOR_BGR2RGB))
        plt.title(f"Масштабирование\n({name})")
        plt.axis('off')
        idx += 1

        # Поворот
        rotated_image = apply_affine_transformation(image, rotation_matrix, interpolation)
        plt.subplot(3, 4, idx)
        plt.imshow(cv2.cvtColor(rotated_image, cv2.COLOR_BGR2RGB))
        plt.title(f"Поворот\n({name})")
        plt.axis('off')
        idx += 1

        # Скос
        skewed_image = apply_affine_transformation(image, skew_matrix, interpolation)
        plt.subplot(3, 4, idx)
        plt.imshow(cv2.cvtColor(skewed_image, cv2.COLOR_BGR2RGB))
        plt.title(f"Скос\n({name})")
        plt.axis('off')
        idx += 1

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
