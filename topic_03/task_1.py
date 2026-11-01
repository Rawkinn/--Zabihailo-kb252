import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from topic_02.task_3 import calculate


EXIT_COMMANDS = ("exit", "quit", "q", "вихід")


def read_text(prompt):
    text = input(prompt).strip()
    if text.lower() in EXIT_COMMANDS:
        return None
    return text


def read_number(prompt):
    text = read_text(prompt)
    if text is None:
        return None
    try:
        return float(text)
    except ValueError:
        raise ValueError("Потрібно вводити числа.") from None


def main():
    print("Калькулятор із повторним введенням")
    print("Для завершення введіть exit, quit, q або вихід.")
    while True:
        try:
            a = read_number("Перше число: ")
            if a is None:
                break
            operation = read_text("Операція (+, -, *, /): ")
            if operation is None:
                break
            b = read_number("Друге число: ")
            if b is None:
                break
            result = calculate(a, operation, b)
            print(f"Результат: {result:g}")
        except (ValueError, ZeroDivisionError) as error:
            print("Помилка:", error)
        except (EOFError, KeyboardInterrupt):
            print()
            break
    print("Роботу калькулятора завершено.")


if __name__ == "__main__":
    main()
