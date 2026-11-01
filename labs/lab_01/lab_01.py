"""Розширення наданого lab_01.py: чотири поля та зміна запису."""

FIELDS = ("name", "phone", "email", "group")
LABELS = ("ПІБ", "Телефон", "Email", "Група")
CANCEL_COMMAND = "/cancel"

# Початковий відсортований list із прикладу викладача.
list = [
    {"name": "Bob", "phone": "0631234567",
     "email": "bob@example.com", "group": "КБ-252"},
    {"name": "Emma", "phone": "0631234567",
     "email": "emma@example.com", "group": "КБ-252"},
    {"name": "Jon", "phone": "0631234567",
     "email": "jon@example.com", "group": "КБ-252"},
    {"name": "Zak", "phone": "0631234567",
     "email": "zak@example.com", "group": "КБ-252"},
]


def validate_student(student):
    """Перевіряє чотири поля та повертає окремий словник."""
    result = {}
    for field, label in zip(FIELDS, LABELS):
        value = student.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Поле «{label}» має бути непорожнім рядком.")
        result[field] = value.strip()
    return result


def check_index(students, index):
    if type(index) is not int or not 0 <= index < len(students):
        raise IndexError("Неправильний номер запису.")


def printAllList(records=None):
    """Розширений вивід початкової функції: номер і всі чотири поля."""
    records = list if records is None else records
    if not records:
        print("Довідник порожній.")
        return
    headers = ("№", *LABELS)
    rows = [(str(i), *(item[field] for field in FIELDS))
            for i, item in enumerate(records, 1)]
    widths = [max(len(row[i]) for row in [headers, *rows])
              for i in range(len(headers))]
    print(" | ".join(value.ljust(widths[i])
                     for i, value in enumerate(headers)))
    print("-+-".join("-" * width for width in widths))
    for elem in rows:
        strForPrint = " | ".join(value.ljust(widths[i])
                                  for i, value in enumerate(elem))
        print(strForPrint)


def read_student(current=None):
    print("Для скасування введіть /cancel у будь-якому полі.")
    if current is not None:
        print("Порожнє введення залишає поточне значення.")
    record = {}
    for field, label in zip(FIELDS, LABELS):
        while True:
            suffix = f" [{current[field]}]" if current is not None else ""
            value = input(f"{label}{suffix}: ").strip()
            if value.casefold() == CANCEL_COMMAND:
                return None
            if not value and current is not None:
                value = current[field]
            if value:
                record[field] = value
                break
            print("Помилка: поле не може бути порожнім.")
    return validate_student(record)


def choose_student(students, allowed=None):
    """Вибір номера; allowed обмежує вибір знайденими однаковими ПІБ."""
    require_dataset(students)
    printAllList(students)
    if not students:
        return None
    while True:
        text = input("Номер запису (/cancel — скасувати): ").strip()
        if text.casefold() == CANCEL_COMMAND:
            return None
        try:
            index = int(text) - 1
            check_index(students, index)
            if allowed is not None and index not in allowed:
                raise ValueError("Цей номер має інший ПІБ.")
            return index
        except (ValueError, IndexError):
            print("Помилка: оберіть номер потрібного запису з таблиці.")


def find_student(students, name):
    """Пошук за ім'ям із початкового deleteElement, з уточненням дубля."""
    positions = []
    for position, item in enumerate(students):
        if name.casefold() == item["name"].casefold():
            positions.append(position)
    if not positions:
        print("Запис не знайдено.")
        return None
    if len(positions) == 1:
        return positions[0]
    print("Є кілька однакових ПІБ. Уточніть номер запису.")
    return choose_student(students, positions)


def addNewElement(newItem=None, records=None):
    """Додавання з початковим пошуком insertPosition циклом for."""
    records = list if records is None else records
    interactive = newItem is None
    if interactive:
        newItem = read_student()
        if newItem is None:
            print("Додавання скасовано.")
            return None
    newItem = validate_student(newItem)
    name = newItem["name"].casefold()
    insertPosition = 0
    for item in records:
        if name >= item["name"].casefold():
            insertPosition += 1
        else:
            break
    records.insert(insertPosition, newItem)
    if interactive:
        print("Запис додано.")
    return insertPosition


def deleteElement(name=None, records=None, index=None):
    """Видалення за ПІБ; індекс використовується для точного вибору."""
    records = list if records is None else records
    interactive = index is None
    if interactive:
        if name is None:
            name = input("Введіть ПІБ для видалення: ").strip()
        if name.casefold() == CANCEL_COMMAND:
            print("Видалення скасовано.")
            return None
        deletePosition = find_student(records, name)
        if deletePosition is None:
            return None
    else:
        check_index(records, index)
        deletePosition = index
    deleted = records[deletePosition]
    del records[deletePosition]
    if interactive:
        print("Видалено:", deleted["name"])
    return deleted


def updateElement(name=None, newItem=None, records=None, index=None):
    """Заповнена функція викладача: перевірка, видалення і вставка."""
    records = list if records is None else records
    interactive = newItem is None
    if index is None:
        if name is None:
            name = input("Введіть ПІБ для зміни: ").strip()
        if name.casefold() == CANCEL_COMMAND:
            print("Зміну скасовано.")
            return None
        index = find_student(records, name)
        if index is None:
            return None
    check_index(records, index)
    if interactive:
        newItem = read_student(records[index])
        if newItem is None:
            print("Зміну скасовано.")
            return None
    if any(field not in FIELDS for field in newItem):
        raise ValueError("Невідоме поле запису.")
    updated = records[index].copy()
    updated.update(newItem)
    updated = validate_student(updated)
    deleteElement(records=records, index=index)
    position = addNewElement(updated, records)
    if interactive:
        print("Запис змінено; порядок збережено.")
    return position


# Сумісний інтерфейс для CSV і тестів лабораторної роботи 2.
# Усі операції делегують саме функціям наданого початкового коду.
def require_dataset(students):
    if students is None:
        raise ValueError("Потрібно передати явний список записів.")


def add_student(students, student):
    require_dataset(students)
    if student is None:
        raise ValueError("Потрібно передати запис студента.")
    return addNewElement(student, students)


def delete_student(students, index):
    require_dataset(students)
    check_index(students, index)
    return deleteElement(records=students, index=index)


def edit_student(students, index, changes):
    require_dataset(students)
    check_index(students, index)
    if changes is None:
        raise ValueError("Потрібно передати словник змін.")
    return updateElement(newItem=changes, records=students, index=index)


def print_students(students):
    require_dataset(students)
    return printAllList(students)


def main():
    print("Телефонний довідник студентів")
    try:
        while True:
            chouse = input(
                "Дія [C додати, U змінити, D видалити, P показати, X вихід]: "
            ).strip().upper()
            match chouse:
                case "C":
                    addNewElement()
                    printAllList()
                case "U":
                    updateElement()
                case "D":
                    deleteElement()
                case "P":
                    printAllList()
                case "X":
                    break
                case _:
                    print("Невідома дія. Оберіть C, U, D, P або X.")
    except (EOFError, KeyboardInterrupt):
        print("\nВведення завершено.")
    print("Роботу довідника завершено.")


if __name__ == "__main__":
    main()
