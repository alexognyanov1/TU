# Description: This script implements a Caesar cipher for text encryption.
# Tags: Lab, Python, Caesar Cipher, Encryption

def find_longest_word(sentence):
    words = sentence.split(' ')

    if len(words) == 0:
        return None

    word_lenghts = [len(word) for word in words]

    return words[word_lenghts.index(max(word_lenghts))]


if __name__ == "__main__":
    sentence = input("Enter a sentence: ")
    print(f"The longest word is: {find_longest_word(sentence)}")
