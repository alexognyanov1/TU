# Description: This script calculates the area of a square or a circle based on user input.  It handles potential errors such as invalid shape type or incorrect input format.
# Tags: Area Calculation, Geometry, Shape, Square, Circle, User Input, Error Handling

import math


class Shape:
    def __init__(self, shape_type):
        self.shape_type = shape_type

    def area(self):
        return 0


class Square(Shape):
    def __init__(self, side_length):
        super().__init__('Square')
        self.side_length = side_length

    def area(self):
        return self.side_length ** 2


class Circle(Shape):
    def __init__(self, radius):
        super().__init__('Circle')
        self.radius = radius

    def area(self):
        return math.pi * (self.radius ** 2)


def main():
    try:
        shape_type = input(
            "Enter the shape type (Square/Circle): ").strip().capitalize()
        if shape_type == 'Square':
            side_length = float(input("Enter the side length of the square: "))
            shape = Square(side_length)
        elif shape_type == 'Circle':
            radius = float(input("Enter the radius of the circle: "))
            shape = Circle(radius)
        else:
            raise ValueError("Invalid shape type")

        print(f"The area of the {shape_type} is: {shape.area()}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()