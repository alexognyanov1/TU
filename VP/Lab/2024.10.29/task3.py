# Description: This script generates a visual representation of a directory structure.
# Tags: Lab, Python, Directory Tree, File Sizes

import os
import argparse


def generate_tree(root_path, max_depth=None, show_sizes=False):
    def tree(dir_path, prefix='', depth=0):
        if max_depth is not None and depth > max_depth:
            return
        contents = os.listdir(dir_path)
        pointers = ['├── '] * (len(contents) - 1) + ['└── ']
        for pointer, name in zip(pointers, contents):
            path = os.path.join(dir_path, name)
            if os.path.isdir(path):
                print(prefix + pointer + name)
                extension = '│   ' if pointer == '├── ' else '    '
                tree(path, prefix + extension, depth + 1)
            else:
                size = f" ({os.path.getsize(path)} bytes)" if show_sizes else ""
                print(prefix + pointer + name + size)

    print(os.path.basename(root_path))
    tree(root_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a visual representation of a directory structure.")
    parser.add_argument(
        "root_path", help="Root directory path to start the tree.")
    parser.add_argument("--max_depth", type=int, default=None,
                        help="Maximum depth to traverse.")
    parser.add_argument("--show_sizes", action="store_true",
                        help="Show file sizes.")

    args = parser.parse_args()
    generate_tree(args.root_path, args.max_depth, args.show_sizes)
