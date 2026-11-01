"""Калькулятор з обробкою винятків під час введення та ділення."""

EXIT_COMMANDS = ("exit", "quit", "q", "вихід")


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        print("Помилка: ділити на нуль не можна.")
        return None


def read_text(prompt):
    text = input(prompt).strip()
    if text.lower() in EXIT_COMMANDS:
        return None
    return text


def request_data():
    """Запитує операнди й операцію та обробляє помилки введення."""
    while True:
        try:
            first = read_text("Перше число: ")
            if first is None:
                return None
            a = float(first)
            operation = read_text("Операція (+, -, *, /): ")
            if operation is None:
                return None
            if operation not in ("+", "-", "*", "/"):
                print("Помилка: невідома операція. Введіть +, -, * або /.")
                continue
            second = read_text("Друге число: ")
            if second is None:
                return None
            b = float(second)
            return a, operation, b
        except ValueError:
            print("Помилка: потрібно вводити числа.")
        except (EOFError, KeyboardInterrupt):
            print()
            return None


def calculate(a, operation, b):
    if operation == "+":
        return add(a, b)
    elif operation == "-":
        return subtract(a, b)
    elif operation == "*":
        return multiply(a, b)
    elif operation == "/":
        return divide(a, b)
    else:
        raise ValueError("Невідома операція.")


def main():
    print("Калькулятор з обробкою винятків")
    print("Для завершення введіть exit, quit, q або вихід.")
    while True:
        data = request_data()
        if data is None:
            break
        a, operation, b = data
        result = calculate(a, operation, b)
        if result is not None:
            print(f"Результат: {result:g}")
    print("Роботу калькулятора завершено.")


if __name__ == "__main__":
    main()
