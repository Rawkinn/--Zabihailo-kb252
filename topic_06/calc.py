from datetime import datetime
from pathlib import Path

import operations

LOG_FILE = Path(__file__).with_name("calc.log")


def write_log(a, operation, b, result):
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        file.write(f"[{time}] {a:g} {operation} {b:g} = {result}\n")


def main():
    print("Калькулятор із логуванням")
    print("Для завершення введіть exit, quit, q або вихід.")
    while True:
        data = operations.request_data()
        if data is None:
            break
        a, operation, b = data
        try:
            result = operations.calculate(a, operation, b)
        except ZeroDivisionError:
            print("Помилка: ділити на нуль не можна.")
            write_log(a, operation, b, "помилка: ділення на нуль")
            continue
        except ValueError as error:
            print("Помилка:", error)
            continue
        print(f"Результат: {result:g}")
        write_log(a, operation, b, f"{result:g}")
    print("Роботу калькулятора завершено.")


if __name__ == "__main__":
    main()
