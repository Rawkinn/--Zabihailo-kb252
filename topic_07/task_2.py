class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __str__(self):
        return f"{self.author}. {self.title}"


book = Book("Кобзар", "Тарас Шевченко")

print(book)
print("Назва:", book.title)
print("Автор:", book.author)
