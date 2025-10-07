import os
import re
import logging
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("API key not found. Please set GEMINI_API_KEY in your .env file.")
    exit()


logging.basicConfig(filename='gemini_api.log', level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')


def send_prompt(prompt, max_tokens=5000, temperature=0.3, top_p=0.2):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

    conf = {
        'max_output_tokens': max_tokens,
        'temperature': temperature,
        'top_p': top_p
    }
    try:
        response = model.generate_content(
            prompt,
            generation_config=conf
        )
        return response.text if response else None
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        return None


def find_files_without_tags_or_description(folder_path):
    files_to_update = []
    for root, _, files in os.walk(folder_path):
        if root == folder_path:
            continue
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                    has_description = re.search(r'# Description:.*', content)
                    has_tags = re.search(r'# Tags:.*', content)
                    if not has_description or not has_tags:
                        files_to_update.append(
                            (file_path, not has_description, not has_tags))
    return files_to_update


def generate_tags_and_description(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    prompt = f"Write a description and tags following this pattern: \"# Description: This script <does something>.\n# Tags: File Backup, Logging\" for the following Python script:\n\n{content}. Separate the description and tags with a newline. Do not include any tags that describe which language and libraries are used."
    return send_prompt(prompt)


def get_tags_and_description(split_new_content):
    new_description = next((line for line in split_new_content if line.startswith(
        '# Description')), split_new_content[0])

    new_tags = next((line for line in split_new_content if line.startswith(
        '# Tags')), split_new_content[1])

    return (new_description, new_tags)


def update_file_with_tags_and_description(file_path, tags_and_description, needs_description, needs_tags):
    split_new_content = tags_and_description.splitlines()
    new_description, new_tags = get_tags_and_description(split_new_content)

    print(new_description)
    print(new_tags)

    with open(file_path, 'r') as f:
        content = f.read()

    new_content = content

    if needs_description:
        new_content = f"{new_description}\n{new_content}"

    if needs_tags:
        nc = new_content.splitlines()

        new_content = f"{nc[0]}\n{new_tags}\n\n" + '\n'.join(nc[1:])

    with open(file_path, 'w') as f:
        f.write(new_content)


def generate_tags(folder_path="."):
    files_to_update = find_files_without_tags_or_description(folder_path)

    for file_path, needs_description, needs_tags in files_to_update:
        print("Generating tags and description for file: ", file_path)
        print("Needs description: ", needs_description)
        print("Needs tags: ", needs_tags)
        tags_and_description = generate_tags_and_description(
            file_path)

        if tags_and_description:
            update_file_with_tags_and_description(
                file_path, tags_and_description, needs_description, needs_tags)
            print(f"Updated {file_path} with tags and description.")
        else:
            print(f"Failed to generate tags and description for {file_path}.")


if __name__ == "__main__":
    generate_tags()
