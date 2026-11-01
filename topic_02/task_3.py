"""Калькулятор із використанням match та case (Python 3.10+)."""


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Ділити на нуль не можна.")
    return a / b


def calculate(a, operation, b):
    match operation:
        case "+":
            return add(a, b)
        case "-":
            return subtract(a, b)
        case "*":
            return multiply(a, b)
        case "/":
            return divide(a, b)
        case _:
            raise ValueError(
                "Невідома операція. Використовуйте +, -, * або /."
            )


def main():
    print("Калькулятор match")
    try:
        a = float(input("Перше число: "))
        operation = input("Операція (+, -, *, /): ").strip()
        b = float(input("Друге число: "))
    except ValueError:
        print("Помилка: потрібно вводити числа.")
        return

    try:
        result = calculate(a, operation, b)
        print(f"Результат: {result:g}")
    except (ValueError, ZeroDivisionError) as error:
        print("Помилка:", error)


if __name__ == "__main__":
    main()
