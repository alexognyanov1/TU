# Description: This script counts the frequency of numbers in an initial list, then calculates the product of each unique number and its frequency, storing these results in a new list.
# Tags: Frequency Counting, Data Aggregation, List Processing

a = [5, 10, 15, 8, 6, 12, 20, 3, 3, 7]
lookup = [0] * (max(a) + 1)
res = []

for i in range(len(a)):
    lookup[a[i]] += 1

print(lookup)

for i in range(len(lookup)):
    if lookup[i] == 0:
        continue
    res.append([i * lookup[i]])

print(res)