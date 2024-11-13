# Description: This script demonstrates various set operations in Python, including union, difference, intersection, element removal, and clearing sets. It also shows how to create sets from user input.
# Tags: Set Operations, Union, Difference, Intersection, Element Removal, Set Creation 

def create_set():
    n = int(input("Enter the number of elements in the set: "))
    s = set()
    for _ in range(n):
        element = int(input("Enter an element: "))
        s.add(element)
    return s


def main():
    set1 = {1, 2, 3, 4, 5}

    set2 = {4, 5, 6, 7, 8}
    print(f"Size of the first set: {len(set1)}")
    print(f"Size of the second set: {len(set2)}")

    union_set = set1.union(set2)
    print(f"Union of the sets: {union_set}")

    difference_set = set1.difference(set2)
    print(f"Difference of the sets (set1 - set2): {difference_set}")

    intersection_set = set1.intersection(set2)
    print(f"Intersection of the sets: {intersection_set}")

    element_to_remove = 3
    set1.discard(element_to_remove)
    print(f"First set after removing {element_to_remove}: {set1}")

    set1.clear()
    set2.clear()
    print("Both sets have been cleared.")
    print(f"First set: {set1}")
    print(f"Second set: {set2}")


if __name__ == "__main__":
    main()