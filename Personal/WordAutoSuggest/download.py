import requests
import os


def save_dictionary():
    file_path = "/usr/share/dict/words"
    if os.path.exists(file_path):
        with open(file_path, "r") as source_file:
            words = source_file.read()
        with open("words.txt", "w") as destination_file:
            destination_file.write(words)
    else:
        print(f"Source file {file_path} does not exist.")


if __name__ == "__main__":
    save_dictionary()
    print("Dictionary downloaded successfully.")