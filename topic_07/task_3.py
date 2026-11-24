class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"{self.name}, вік: {self.age}"


students = [
    Student("Олена", 20),
    Student("Андрій", 19),
    Student("Марія", 21),
    Student("Богдан", 18),
]

for student in sorted(students, key=lambda student: student.name):
    print(student)
