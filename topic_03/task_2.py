def demonstrate_list_methods():
    numbers = [3, 1, 2]
    print("Початковий список:", numbers)

    numbers.extend([4, 5])
    print("extend([4, 5]):", numbers)
    numbers.append(6)
    print("append(6):", numbers)
    numbers.insert(1, 10)
    print("insert(1, 10):", numbers)
    numbers.remove(10)
    print("remove(10):", numbers)
    numbers.sort()
    print("sort():", numbers)
    numbers.reverse()
    print("reverse():", numbers)

    copied = numbers.copy()
    print("copy():", copied)
    copied.append(99)
    print("Копія після append(99):", copied)
    print("Оригінал після зміни копії:", numbers)

    numbers.clear()
    print("clear():", numbers)


if __name__ == "__main__":
    demonstrate_list_methods()
