import csv
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from labs.lab_01.lab_01 import (
    FIELDS,
    add_student,
    choose_student,
    delete_student,
    edit_student,
    print_students,
    read_student,
    validate_student,
)


def load_students(filename):
    students = []
    with open(filename, encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source, strict=True)
        try:
            if reader.fieldnames is None:
                raise ValueError("CSV не містить заголовка.")
            headers = [
                name.strip().casefold() for name in reader.fieldnames
            ]
            if len(headers) != len(set(headers)):
                raise ValueError("Заголовки CSV не можуть повторюватися.")
            if set(headers) != set(FIELDS):
                raise ValueError(
                    "Потрібні стовпці: name, phone, email, group."
                )
            reader.fieldnames = headers
            for row in reader:
                if None in row or any(
                    value is None for value in row.values()
                ):
                    raise ValueError("Неправильна кількість полів у CSV.")
                add_student(students, row)
        except (csv.Error, ValueError) as error:
            raise ValueError(
                f"Помилка в рядку CSV {reader.line_num}: {error}"
            ) from error
    return students


def save_students(filename, students):
    records = [validate_student(student) for student in students]
    records.sort(key=lambda student: student["name"].casefold())
    path = Path(filename)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8-sig", newline="",
            dir=path.parent, prefix=path.name + ".", suffix=".tmp",
            delete=False,
        ) as destination:
            temporary = Path(destination.name)
            writer = csv.DictWriter(destination, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(records)
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def run_menu(students):
    try:
        while True:
            print("\n1 — додати; 2 — змінити; 3 — видалити;")
            print("4 — показати довідник; 0 — вихід.")
            command = input("Оберіть дію: ").strip().casefold()
            if command in ("0", "q", "exit", "вихід"):
                return
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


def main(argv=None):
    arguments = sys.argv[1:] if argv is None else list(argv)
    if len(arguments) != 1:
        print("Використання: python lab_02.py <file.csv>")
        return 2
    filename = Path(arguments[0])
    try:
        students = load_students(filename)
    except (OSError, ValueError) as error:
        print("Помилка завантаження:", error)
        return 1
    print("Телефонний довідник студентів із CSV")
    print("Завантажено записів:", len(students))
    run_menu(students)
    try:
        save_students(filename, students)
    except (OSError, ValueError) as error:
        print("Не вдалося зберегти дані:", error)
        return 1
    print("Дані збережено:", filename)
    print("Роботу довідника завершено.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
