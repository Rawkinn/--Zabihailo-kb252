"""Відсортований телефонний довідник студентів із чотирма полями."""

FIELDS = ("name", "phone", "email", "group")
LABELS = ("ПІБ", "Телефон", "Email", "Група")
CANCEL_COMMAND = "/cancel"


def validate_student(student):
    """Перевіряє поля та повертає окремий нормалізований словник."""
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


def add_student(students, student):
    """Додає копію запису за ПІБ, без урахування регістру."""
    record = validate_student(student)
    position = 0
    name_key = record["name"].casefold()
    while position < len(students):
        if students[position]["name"].casefold() > name_key:
            break
        position += 1
    students.insert(position, record)
    return position


def delete_student(students, index):
    """Видаляє запис за індексом, що починається з нуля."""
    check_index(students, index)
    return students.pop(index)


def edit_student(students, index, changes):
    """Перевіряє зміни, видаляє старий запис і додає новий у порядок."""
    check_index(students, index)
    if any(field not in FIELDS for field in changes):
        raise ValueError("Невідоме поле запису.")
    updated = students[index].copy()
    updated.update(changes)
    record = validate_student(updated)
    delete_student(students, index)
    return add_student(students, record)


def print_students(students):
    if not students:
        print("Довідник порожній.")
        return
    rows = [[str(i), *(student[field] for field in FIELDS)]
            for i, student in enumerate(students, 1)]
    headers = ["№", *LABELS]
    widths = [max(len(row[i]) for row in [headers, *rows])
              for i in range(len(headers))]
    print(" | ".join(text.ljust(widths[i])
                     for i, text in enumerate(headers)))
    print("-+-".join("-" * width for width in widths))
    for row in rows:
        print(" | ".join(text.ljust(widths[i])
                         for i, text in enumerate(row)))


def read_student(current=None):
    """Збирає всі поля до зміни довідника; None означає скасування."""
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


def choose_student(students):
    print_students(students)
    if not students:
        return None
    while True:
        text = input("Номер запису (/cancel — скасувати): ").strip()
        if text.casefold() == CANCEL_COMMAND:
            return None
        try:
            index = int(text) - 1
            check_index(students, index)
            return index
        except (ValueError, IndexError):
            print(f"Помилка: введіть номер від 1 до {len(students)}.")


def main():
    students = []
    print("Телефонний довідник студентів")
    try:
        while True:
            print("\n1 — додати; 2 — змінити; 3 — видалити;")
            print("4 — показати довідник; 0 — вихід.")
            command = input("Оберіть дію: ").strip().casefold()
            if command in ("0", "q", "exit", "вихід"):
                break
            elif command == "1":
                record = read_student()
                if record is None:
                    print("Додавання скасовано.")
                else:
                    add_student(students, record)
                    print("Запис додано.")
            elif command == "2":
                index = choose_student(students)
                if index is not None:
                    record = read_student(students[index])
                    if record is None:
                        print("Зміну скасовано.")
                    else:
                        edit_student(students, index, record)
                        print("Запис змінено; порядок збережено.")
            elif command == "3":
                index = choose_student(students)
                if index is not None:
                    deleted = delete_student(students, index)
                    print("Видалено:", deleted["name"])
            elif command == "4":
                print_students(students)
            else:
                print("Невідома дія. Оберіть пункт від 0 до 4.")
    except (EOFError, KeyboardInterrupt):
        print("\nВведення завершено.")
    print("Роботу довідника завершено.")


if __name__ == "__main__":
    main()
