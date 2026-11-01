"""Пошук позиції вставки у список, відсортований за зростанням."""


def find_insert_position(sorted_list, value):
    """Повертає індекс перед першим елементом, не меншим за value."""
    left = 0
    right = len(sorted_list)
    while left < right:
        middle = (left + right) // 2
        if sorted_list[middle] < value:
            left = middle + 1
        else:
            right = middle
    return left


def main():
    numbers = [1, 3, 5, 7, 9]
    print("Відсортований список:", numbers)
    try:
        value = int(input("Новий цілий елемент: "))
    except ValueError:
        print("Помилка: потрібно ввести ціле число.")
        return
    position = find_insert_position(numbers, value)
    print("Позиція вставки (індексація з 0):", position)
    numbers.insert(position, value)
    print("Список після вставки:", numbers)


if __name__ == "__main__":
    main()
