class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Ділити на нуль не можна.")
        return a / b

    def calculate(self, a, operation, b):
        if operation == "+":
            return self.add(a, b)
        if operation == "-":
            return self.subtract(a, b)
        if operation == "*":
            return self.multiply(a, b)
        if operation == "/":
            return self.divide(a, b)
        raise ValueError("Невідома операція.")
