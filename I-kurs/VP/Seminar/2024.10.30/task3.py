# Description: This script calculates the area and perimeter of different geometric shapes based on user input.
# Tags: Geometry

def calculate_square():
    side = float(input("Enter the side length of the square: "))
    area = side ** 2
    perimeter = 4 * side
    return area, perimeter


def calculate_rectangle():
    length = float(input("Enter the length of the rectangle: "))
    width = float(input("Enter the width of the rectangle: "))
    area = length * width
    perimeter = 2 * (length + width)
    return area, perimeter


def calculate_right_triangle():
    base = float(input("Enter the base length of the right triangle: "))
    height = float(input("Enter the height of the right triangle: "))
    hypotenuse = (base ** 2 + height ** 2) ** 0.5
    area = 0.5 * base * height
    perimeter = base + height + hypotenuse
    return area, perimeter


def main():
    print("Choose a figure to calculate its area and perimeter:")
    print("1. Square")
    print("2. Rectangle")
    print("3. Right Triangle")
    choice = input("Enter the number of your choice: ")

    if choice == '1':
        area, perimeter = calculate_square()
    elif choice == '2':
        area, perimeter = calculate_rectangle()
    elif choice == '3':
        area, perimeter = calculate_right_triangle()
    else:
        print("Invalid choice")
        return

    print(f"Area: {area}")
    print(f"Perimeter: {perimeter}")


if __name__ == "__main__":
    main()
