# Description: This script generates a nested array of random integers, prints it, and then removes a specified row and column from the array.
# Tags: Array Manipulation, Matrix Operations, Random Number Generation

import random


def generate_nested_array(n, m):
    return [[random.randint(10, 100) for _ in range(m)] for _ in range(n)]


def pretty_print_matrix(matrix):
    for row in matrix:
        print(" ".join(f"{num:3}" for num in row))

    print()


def remove_row(matrix, row_index):
    if 0 <= row_index < len(matrix):
        del matrix[row_index]
    else:
        print("Row index out of range")


def remove_column(matrix, col_index):
    if matrix and 0 <= col_index < len(matrix[0]):
        for row in matrix:
            del row[col_index]
    else:
        print("Column index out of range")


n = 5
m = 4
nested_array = generate_nested_array(n, m)
pretty_print_matrix(nested_array)

remove_row(nested_array, 0)
pretty_print_matrix(nested_array)

remove_column(nested_array, 0)
pretty_print_matrix(nested_array)
