from tags import generate_tags
from markdown import generate_markdown

if __name__ == "__main__":
    folder_path = "."
    generate_tags(folder_path)
    generate_markdown(folder_path)
