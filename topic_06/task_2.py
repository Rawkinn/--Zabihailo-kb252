students = [
    {"name": "Олена", "grade": 90},
    {"name": "Андрій", "grade": 75},
    {"name": "Петро", "grade": 95},
    {"name": "Марія", "grade": 88},
    {"name": "Богдан", "grade": 75},
]

by_name = sorted(students, key=lambda student: student["name"])
by_grade = sorted(students, key=lambda student: student["grade"])

print("За іменем:")
for student in by_name:
    print(student)

print("За оцінкою:")
for student in by_grade:
    print(student)
