# Description: This script removes the shortest and longest words from a given sentence.
# Tags: String Manipulation, Word Processing

def remove_shortest_and_longest(sentence):
    words = sentence.split()
    if len(words) < 3:
        return sentence

    shortest_word = min(words, key=len)
    longest_word = max(words, key=len)

    words.remove(shortest_word)
    words.remove(longest_word)

    return ' '.join(words)


sentence = "asdf asdfasdfasdf asdf123 asdF123"
result = remove_shortest_and_longest(sentence)
print(result)
