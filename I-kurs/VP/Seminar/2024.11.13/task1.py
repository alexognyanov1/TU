def generate_dict(word):
    result = {}
    for _, char in enumerate(word):
        result[char] = word.replace(char, "")
    return result


word = "aasdf"
print(generate_dict(word))
