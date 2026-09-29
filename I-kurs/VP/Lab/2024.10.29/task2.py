import os
import random
import string
import csv

DIRECTORY = os.path.abspath(__file__ + "/../task2")
NUMBER_RANDOM_FILES = 10


def generate_random_string(length: int) -> str:
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def create_file(file_name: str, extension: str, content: str):
    with open(f"{DIRECTORY}/{file_name}.{extension}", "w") as file:
        file.write(content)


def generate_files():
    if not os.path.exists(DIRECTORY):
        os.makedirs(DIRECTORY)

    for _ in range(NUMBER_RANDOM_FILES):
        create_file(generate_random_string(10),
                    generate_random_string(3), generate_random_string(10))


def traverse_dir():
    dir_list = [f for f in os.listdir(
        DIRECTORY) if os.path.isfile(DIRECTORY + "/" + f)]
    ext_dict = {}

    for file in dir_list:
        extension = file.split(".")[-1]
        if extension not in ext_dict:
            ext_dict[extension] = []

        ext_dict[extension].append(file)

    for i in ext_dict:
        if not os.path.exists(DIRECTORY + "/" + i):
            os.makedirs(DIRECTORY + "/" + i)

        files = ext_dict[i]

        for filename in files:
            src = DIRECTORY + "/" + filename
            dest = DIRECTORY + "/" + i + "/" + filename
            if src != dest:
                try:
                    os.rename(src, dest)
                except OSError as e:
                    print(f"Error moving file {filename}: {e}")


def log_file_info():
    with open(f"{DIRECTORY}/file_log.csv", "w", newline='') as csvfile:
        fieldnames = ['name', 'extension', 'size',
                      'creation_date', 'modification_date']
        writer = csv.DictWriter(
            csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for root, _, files in os.walk(DIRECTORY):
            for file in files:
                if file == 'file_log.csv':
                    continue
                file_path = os.path.join(root, file)
                file_stat = os.stat(file_path)
                writer.writerow({
                    'name': os.path.splitext(file)[0],
                    'extension': os.path.splitext(file)[1][1:],
                    'size': file_stat.st_size,
                    'creation_date': file_stat.st_ctime,
                    'modification_date': file_stat.st_mtime
                })


generate_files()
traverse_dir()
log_file_info()
