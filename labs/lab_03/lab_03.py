import sys

from storage import StudentStorage
from student import Student
from utils import (
    CANCEL_COMMAND,
    FIELDS,
    LABELS,
    is_cancel,
    is_exit,
    read_text,
)


def read_student(current=None):
    print(f"Для скасування введіть {CANCEL_COMMAND} у будь-якому полі.")
    if current is not None:
        print("Порожнє введення залишає поточне значення.")
    values = {}
    for field, label in zip(FIELDS, LABELS):
        while True:
            suffix = (
                f" [{getattr(current, field)}]"
                if current is not None else ""
            )
            value = read_text(f"{label}{suffix}: ")
            if is_cancel(value):
                return None
            if not value and current is not None:
                value = getattr(current, field)
            if value:
                values[field] = value
                break
            print("Помилка: поле не може бути порожнім.")
    return Student.from_dict(values)


def print_students(students):
    if len(students) == 0:
        print("Довідник порожній.")
        return
    headers = ("№", *LABELS)
    rows = [
        (str(index), *(getattr(student, field) for field in FIELDS))
        for index, student in enumerate(students, 1)
    ]
    widths = [
        max(len(row[column]) for row in [headers, *rows])
        for column in range(len(headers))
    ]
    def format_row(values):
        return " | ".join(
            value.ljust(widths[i]) for i, value in enumerate(values)
        )

    print(format_row(headers))
    print("-+-".join("-" * width for width in widths))
    for row in rows:
        print(format_row(row))


def choose_student(students):
    print_students(students)
    if len(students) == 0:
        return None
    while True:
        text = read_text(
            f"Номер запису ({CANCEL_COMMAND} для скасування): "
        )
        if is_cancel(text):
            return None
        try:
            index = int(text) - 1
            if not 0 <= index < len(students):
                raise IndexError
            return index
        except (ValueError, IndexError):
            print("Помилка: оберіть номер потрібного запису з таблиці.")


def run_menu(students):
    try:
        while True:
            print("\n1 - додати; 2 - змінити; 3 - видалити;")
            print("4 - показати довідник; 0 - вихід.")
            command = read_text("Оберіть дію: ").casefold()
            if is_exit(command):
                return
            if command == "1":
                student = read_student()
                if student is None:
                    print("Додавання скасовано.")
                else:
                    students.add(student)
                    print("Запис додано.")
            elif command == "2":
                index = choose_student(students)
                if index is not None:
                    student = read_student(students[index])
                    if student is None:
                        print("Зміну скасовано.")
                    else:
                        students.edit(index, student.to_dict())
                        print("Запис змінено; порядок збережено.")
            elif command == "3":
                index = choose_student(students)
                if index is not None:
                    deleted = students.delete(index)
                    print("Видалено:", deleted.name)
            elif command == "4":
                print_students(students)
            else:
                print("Невідома дія. Оберіть пункт від 0 до 4.")
    except (EOFError, KeyboardInterrupt):
        print("\nВведення завершено.")


def main(argv=None):
    arguments = sys.argv[1:] if argv is None else list(argv)
    if len(arguments) != 1:
        print("Використання: python lab_03.py <file.csv>")
        return 2
    storage = StudentStorage(arguments[0])
    try:
        students = storage.load()
    except (OSError, ValueError) as error:
        print("Помилка завантаження:", error)
        return 1
    print("Телефонний довідник студентів на класах")
    print("Завантажено записів:", len(students))
    run_menu(students)
    try:
        storage.save(students)
    except (OSError, ValueError) as error:
        print("Не вдалося зберегти дані:", error)
        return 1
    print("Дані збережено:", storage.path)
    print("Роботу довідника завершено.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
