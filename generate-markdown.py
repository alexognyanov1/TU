import os
from collections import defaultdict
import subprocess


def extract_metadata(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        description = None
        tags = None
        for line in lines:
            if line.startswith("# Description:"):
                description = line.strip().replace("# Description:", "").strip()
            elif line.startswith("# Tags:"):
                tags = line.strip().replace("# Tags:", "").strip().split(", ")
            if description and tags:
                break
        return description, tags


def generate_markdown(folder_path):
    tag_dict = defaultdict(list)

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                description, tags = extract_metadata(file_path)
                if tags:
                    for tag in tags:
                        tag_dict[tag].append(file_path)

    markdown_file_path = os.path.join(folder_path, 'README.md')
    with open(markdown_file_path, 'w') as md_file:
        md_file.write("# Tags Summary\n\n")
        md_file.write("| Tag | Files |\n")
        md_file.write("| --- | ----- |\n")
        for tag in sorted(tag_dict.keys()):
            file_links = ", ".join(
                [f"[{os.path.relpath(path, folder_path)}]({os.path.relpath(path, folder_path)})" for path in tag_dict[tag]])
            md_file.write(f"| {tag} | {file_links} |\n")

        md_file.write("\n## Directory Structure\n\n")
        md_file.write("```\n")
        tree_result = subprocess.run(
            ["tree", folder_path], capture_output=True, text=True)
        md_file.write(tree_result.stdout)
        md_file.write("```\n")


if __name__ == "__main__":
    folder_path = "."
    generate_markdown(folder_path)
