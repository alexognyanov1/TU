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
