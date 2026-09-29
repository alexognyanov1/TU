import os
import numpy as np

root = {"char": None, "children": np.full(26, None)}


def construct_tree():
    curr = root
    with open("words.txt", "r") as file:
        word = file.readline().strip().replace(
            " ", "").replace("-", "").replace("'", "")

        while word:
            for char in word:
                if char.isupper():
                    char = char.lower()
                index = ord(char) - ord('a')
                if curr["children"][index] is None:
                    curr["children"][index] = {
                        "char": char, "children": np.full(26, None)}

                curr = curr["children"][index]

            word = file.readline().strip().replace(
                " ", "").replace("-", "").replace("'", "")

    return root


def check_word(word):
    curr = root
    for char in word:
        if char.isupper():
            char = char.lower()
        index = ord(char) - ord('a')
        if curr["children"][index] is None:
            return False
        curr = curr["children"][index]

    return True


if __name__ == "__main__":
    if not os.path.exists("words.txt"):
        print("Error: 'words.txt' file not found.")
    else:
        tree = construct_tree()
        print("Binary tree constructed successfully.")
        while True:
            word = input().strip()
            if word.lower() == "exit":
                break
            print(check_word(word.lower()))
        print("Exiting the program.")