def modify_list(numbers, threshold):
    for i in range(len(numbers)):
        if numbers[i] > threshold:
            numbers[i] = 0
    return numbers


def test_modify_list():
    test_list = [1, 5, 3, 8, 2, 9, 4]
    threshold = 5
    print(f"Original list: {test_list}")
    print(f"Threshold: {threshold}")
    modified_list = modify_list(test_list.copy(), threshold)
    print(f"Modified list: {modified_list}")


if __name__ == "__main__":
    test_modify_list()
