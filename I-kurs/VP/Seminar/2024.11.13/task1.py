# Description: This script takes a string as input and generates a dictionary where each key is a character from the string and the corresponding value is the string with that character removed.
# Tags: String Manipulation, Dictionary Creation

def generate_dict(word):
    result = {}
    for _, char in enumerate(word):
        result[char] = word.replace(char, "")
    return result


word = "aasdf"
print(generate_dict(word))
