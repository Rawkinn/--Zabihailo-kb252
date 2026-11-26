from student import Student


class StudentList:
    def __init__(self, students=None):
        self._students = []
        for student in students or []:
            self.add(student)

    def __len__(self):
        return len(self._students)

    def __iter__(self):
        return iter(self._students)

    def __getitem__(self, index):
        return self._students[index]

    def __eq__(self, other):
        if not isinstance(other, StudentList):
            return NotImplemented
        return self._students == other._students

    def _check_index(self, index):
        if type(index) is not int or not 0 <= index < len(self._students):
            raise IndexError("Неправильний номер запису.")

    def _insert_position(self, name, records=None):
        records = self._students if records is None else records
        key = name.casefold()
        position = 0
        for student in records:
            if key >= student.name.casefold():
                position += 1
            else:
                break
        return position

    def add(self, student):
        if not isinstance(student, Student):
            raise TypeError("Очікується об'єкт Student.")
        student.validate()
        position = self._insert_position(student.name)
        self._students.insert(position, student)
        return position

    def delete(self, index):
        self._check_index(index)
        return self._students.pop(index)

    def edit(self, index, changes):
        self._check_index(index)
        if not isinstance(changes, dict):
            raise TypeError("Зміни мають бути словником.")
        data = self._students[index].to_dict()
        data.update(changes)
        updated = Student.from_dict(data)
        remaining = self._students[:index] + self._students[index + 1:]
        position = self._insert_position(updated.name, remaining)
        remaining.insert(position, updated)
        self._students = remaining
        return position

    def find(self, name):
        key = name.casefold()
        return [
            index for index, student in enumerate(self._students)
            if student.name.casefold() == key
        ]

    def to_dicts(self):
        return [student.to_dict() for student in self._students]
