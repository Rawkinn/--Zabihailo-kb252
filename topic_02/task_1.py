import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from topic_01.task_3 import get_discriminant


def get_roots(a, b, c):
    if a == 0:
        raise ValueError("Коефіцієнт a не може дорівнювати нулю.")

    discriminant = get_discriminant(a, b, c)
    if discriminant > 0:
        x1 = (-b + math.sqrt(discriminant)) / (2 * a)
        x2 = (-b - math.sqrt(discriminant)) / (2 * a)
        return x1, x2
    elif discriminant == 0:
        return (-b / (2 * a),)
    else:
        return ()


def main():
    print("Квадратне рівняння ax² + bx + c = 0")
    try:
        a = float(input("Введіть a: "))
        b = float(input("Введіть b: "))
        c = float(input("Введіть c: "))
    except ValueError:
        print("Помилка: потрібно вводити числа.")
        return

    try:
        roots = get_roots(a, b, c)
    except ValueError as error:
        print("Помилка:", error)
        return

    print(f"Дискримінант: {get_discriminant(a, b, c):g}")
    if len(roots) == 2:
        print(f"Два корені: x1 = {roots[0]:g}, x2 = {roots[1]:g}")
    elif len(roots) == 1:
        print(f"Один корінь: x = {roots[0]:g}")
    else:
        print("Дійсних коренів немає.")


if __name__ == "__main__":
    main()
