# Description: This script finds the longest repeating sequence of numbers within a given list. It iterates through the list, comparing adjacent elements. If they are equal, they are added to the current sequence. If they are different, the current sequence is compared to the maximum sequence, and the longer one is kept. The process continues until the end of the list, and the final maximum sequence is returned.
# Tags: Sequence Analysis, Repetition Detection, Algorithm

def longest_repeating_sequence(numbers):
    if not numbers:
        return []

    max_sequence = []
    current_sequence = [numbers[0]]

    for i in range(1, len(numbers)):
        if numbers[i] == numbers[i - 1]:
            current_sequence.append(numbers[i])
        else:
            if len(current_sequence) > len(max_sequence):
                max_sequence = current_sequence
            current_sequence = [numbers[i]]

    if len(current_sequence) > len(max_sequence):
        max_sequence = current_sequence

    return max_sequence


numbers = [1, 2, 2]
print(longest_repeating_sequence(numbers))
