def get_discriminant(a, b, c):
    return b**2 - 4 * a * c

if __name__ == "__main__":
    d = get_discriminant(1, -3, 2)
    print("Дискримінант:", d)
