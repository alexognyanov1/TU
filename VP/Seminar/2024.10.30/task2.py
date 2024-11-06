# Description: This script finds the minimum, maximum, and average of a list of numbers.
# Tags: Lab, Python, List Operations, Statistics

n = int(input())

numbers = []

for i in range(n):
    numbers.append(int(input()))

print("min " + str(min(numbers)))
print("max " + str(max(numbers)))
print("avg " + str(sum(numbers) / len(numbers)))
