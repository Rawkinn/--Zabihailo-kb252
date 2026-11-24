EXIT_COMMANDS = ("exit", "quit", "q", "вихід")


def read_text(prompt):
    text = input(prompt).strip()
    if text.lower() in EXIT_COMMANDS:
        return None
    return text


def request_data():
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
