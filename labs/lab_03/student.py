from utils import FIELDS, LABELS


class Student:
    def __init__(self, name, phone, email, group):
        self.name = name
        self.phone = phone
        self.email = email
        self.group = group

    def validate(self):
        for field, label in zip(FIELDS, LABELS):
            value = getattr(self, field)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"Поле «{label}» має бути непорожнім рядком.")
            setattr(self, field, value.strip())
        return self

    def to_dict(self):
        return {field: getattr(self, field) for field in FIELDS}

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise TypeError("Дані студента мають бути словником.")
        if set(data) != set(FIELDS):
            raise ValueError("Неправильний набір полів студента.")
        return cls(*(data[field] for field in FIELDS)).validate()

    def __str__(self):
        return f"{self.name} | {self.phone} | {self.email} | {self.group}"

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.to_dict() == other.to_dict()

    def __repr__(self):
        return (
            f"Student({self.name!r}, {self.phone!r}, "
            f"{self.email!r}, {self.group!r})"
        )
