"""Перевірка методів словників та оператора del."""


def demonstrate_dict_methods():
    marks = {"Python": 85, "Математика": 90}
    print("Початковий словник:", marks)

    marks.update({"Python": 95, "Англійська": 88})
    print("update():", marks)
    del marks["Математика"]
    print("del marks['Математика']:", marks)
    print("keys():", list(marks.keys()))
    print("values():", list(marks.values()))
    print("items():", list(marks.items()))
    marks.clear()
    print("clear():", marks)


if __name__ == "__main__":
    demonstrate_dict_methods()
