import random

CHOICES = ["stone", "scissor", "paper"]
EXIT_COMMANDS = ("exit", "quit", "q", "вихід")


def read_choice():
    while True:
        try:
            choice = input("Ваш вибір (stone, scissor, paper): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return None
        if choice in EXIT_COMMANDS:
            return None
        if choice in CHOICES:
            return choice
        print("Помилка: введіть stone, scissor або paper.")


def get_result(player, computer):
    if player == computer:
        return "Нічия."
    if player == "stone" and computer == "scissor":
        return "Ви перемогли!"
    if player == "scissor" and computer == "paper":
        return "Ви перемогли!"
    if player == "paper" and computer == "stone":
        return "Ви перемогли!"
    return "Переміг комп'ютер."


def main():
    print("Гра: камінь, ножиці, папір")
    print("Для завершення введіть exit, quit, q або вихід.")
    while True:
        player = read_choice()
        if player is None:
            break
        computer = random.choice(CHOICES)
        print("Вибір комп'ютера:", computer)
        print(get_result(player, computer))
    print("Гру завершено.")


if __name__ == "__main__":
    main()
