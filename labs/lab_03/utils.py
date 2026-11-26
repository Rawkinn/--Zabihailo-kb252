FIELDS = ("name", "phone", "email", "group")
LABELS = ("ПІБ", "Телефон", "Email", "Група")
CANCEL_COMMAND = "/cancel"
EXIT_COMMANDS = ("0", "q", "exit", "вихід")


def read_text(prompt):
    return input(prompt).strip()


def is_cancel(value):
    return value.casefold() == CANCEL_COMMAND


def is_exit(value):
    return value.casefold() in EXIT_COMMANDS
