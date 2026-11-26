import csv
import os
import tempfile
from pathlib import Path

from student import Student
from student_list import StudentList
from utils import FIELDS


class StudentStorage:
    def __init__(self, filename):
        self.path = Path(filename)

    def load(self):
        students = StudentList()
        with self.path.open(encoding="utf-8-sig", newline="") as source:
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
                    students.add(Student.from_dict(row))
            except (csv.Error, ValueError) as error:
                raise ValueError(
                    f"Помилка в рядку CSV {reader.line_num}: {error}"
                ) from error
        return students

    def save(self, students):
        if not isinstance(students, StudentList):
            raise TypeError("Очікується об'єкт StudentList.")
        records = [student.validate().to_dict() for student in students]
        records.sort(key=lambda student: student["name"].casefold())
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8-sig", newline="",
                dir=self.path.parent, prefix=self.path.name + ".",
                suffix=".tmp", delete=False,
            ) as destination:
                temporary = Path(destination.name)
                writer = csv.DictWriter(destination, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(records)
            os.replace(temporary, self.path)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
