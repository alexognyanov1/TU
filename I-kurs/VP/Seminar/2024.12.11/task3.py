# Description: This script checks if three given side lengths can form a triangle. It handles invalid inputs such as non-numeric values and sides with lengths less than or equal to zero.  The script then applies the triangle inequality theorem to determine if a triangle can be constructed.
# Tags: Triangle Inequality Theorem, Geometry, Validation, Input Checking

class TriangleChecker:
    def __init__(self, a, b, c):
        self.sides = [a, b, c]

    def is_triangle(self):
        if not all(isinstance(side, (int, float)) for side in self.sides):
            return "Трябва да въведете само числа!"
        if any(side <= 0 for side in self.sides):
            return "Нищо няма да работи с отрицателни числа!"
        a, b, c = sorted(self.sides)
        if a + b > c:
            return "Ура, можете да построите триъгълник!"
        else:
            return "Жалко, но не можете да направите триъгълник от това!"


triangle = TriangleChecker(5, 10, 5)
print(triangle.is_triangle())