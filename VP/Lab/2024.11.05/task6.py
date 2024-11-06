# Description: This script implements a Caesar cipher for text encryption.
# Tags: Lab, Python, Caesar Cipher, Encryption

def ceasar_cipher(text: str, shift: int) -> str:
    result = ""
    for i in range(len(text)):
        char = text[i]
        if char.isupper():
            result += chr((ord(char) + shift - 65) % 26 + 65)
        else:
            result += chr((ord(char) + shift - 97) % 26 + 97)
    return result


print(ceasar_cipher("abc", 1))
