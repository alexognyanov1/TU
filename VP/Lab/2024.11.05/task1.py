# Description: This script calculates the area of different geometric shapes based on user input.
# Tags: Geometry

def square_area(side):
    return side * side


def rectangle_area(length, width):
    return length * width


def triangle_area(base, height):
    return (base * height) / 2


def calculate_area():
    print("Изберете фигура:")
    print("1 - квадрат")
    print("2 - правоъгълник")
    print("3 - правоъгълен триъгълник")

    choice = int(input())

    if choice == 1:
        side = float(input("Въведете дължина на страната: "))
        print(f"Лицето на квадрата е: {square_area(side)}")
    elif choice == 2:
        length = float(input("Въведете дължина: "))
        width = float(input("Въведете ширина: "))
        print(f"Лицето на правоъгълника е: {rectangle_area(length, width)}")
    elif choice == 3:
        base = float(input("Въведете основа: "))
        height = float(input("Въведете височина: "))
        print(f"Лицето на триъгълника е: {triangle_area(base, height)}")
    else:
        print("Невалиден избор!")


if __name__ == "__main__":
    calculate_area()
