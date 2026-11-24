import requests

URL = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
CURRENCIES = ["EUR", "USD", "PLN"]
EXIT_COMMANDS = ("exit", "quit", "q", "вихід")


def get_rates():
    response = requests.get(URL, timeout=10)
    response.raise_for_status()
    rates = {}
    for item in response.json():
        if item["cc"] in CURRENCIES:
            rates[item["cc"]] = item["rate"]
    return rates


def main():
    try:
        rates = get_rates()
    except requests.RequestException as error:
        print("Помилка запиту до НБУ:", error)
        return

    print("Курси НБУ:")
    for currency in CURRENCIES:
        print(f"{currency}: {rates[currency]} грн")

    while True:
        amount_text = input("Сума: ").strip()
        if amount_text.lower() in EXIT_COMMANDS:
            break
        try:
            amount = float(amount_text)
        except ValueError:
            print("Помилка: сума має бути числом.")
            continue
        if amount <= 0:
            print("Помилка: сума має бути більшою за нуль.")
            continue

        currency = input("Валюта (EUR, USD, PLN): ").strip().upper()
        if currency.lower() in EXIT_COMMANDS:
            break
        if currency not in CURRENCIES:
            print("Помилка: підтримуються EUR, USD і PLN.")
            continue

        result = amount * rates[currency]
        print(f"{amount:g} {currency} = {result:.2f} грн")

    print("Роботу конвертера завершено.")


if __name__ == "__main__":
    main()
