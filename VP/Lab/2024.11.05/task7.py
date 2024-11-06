# Description: This script generates Pascal's triangle up to a specified number of rows.
# Tags: Lab, Python, Pascal's Triangle, Mathematics

def pascal_triangle(rows):
    triangle = []
    for i in range(rows):
        triangle.append([1] * (i + 1))
        for j in range(1, i):
            triangle[i][j] = triangle[i - 1][j - 1] + triangle[i - 1][j]
    return triangle


n = 10
t = pascal_triangle(n)

for row in t:
    print(row)
