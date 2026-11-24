import operations
from calculator import Calculator


def main():
    calculator = Calculator()
    print("Калькулятор через ООП")
    print("Для завершення введіть exit, quit, q або вихід.")
    while True:
        data = operations.request_data()
        if data is None:
            break
        a, operation, b = data
        try:
            result = calculator.calculate(a, operation, b)
        except ZeroDivisionError:
            print("Помилка: ділити на нуль не можна.")
            continue
        except ValueError as error:
            print("Помилка:", error)
            continue
        print(f"Результат: {result:g}")
    print("Роботу калькулятора завершено.")


if __name__ == "__main__":
    main()
