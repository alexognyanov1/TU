#include <stdio.h>
#include <stdlib.h>

void create_binary_file(const char *filename) {
  FILE *file = fopen(filename, "wb");
  if (!file) {
    perror("Error opening file");
    exit(EXIT_FAILURE);
  }

  int numbers[] = {1, 2, 3, 4, 5, 6, 7, 8};
  size_t count = sizeof(numbers) / sizeof(numbers[0]);

  fwrite(numbers, sizeof(int), count, file);
  fclose(file);
}

void count_even_odd(const char *filename) {
  FILE *file = fopen(filename, "rb");
  if (!file) {
    perror("Error opening file");
    exit(EXIT_FAILURE);
  }

  int number, even_count = 0, odd_count = 0;
  while (fread(&number, sizeof(int), 1, file)) {
    if (number % 2 == 0)
      even_count++;
    else
      odd_count++;
  }

  fclose(file);
  printf("Even numbers: %d\n", even_count);
  printf("Odd numbers: %d\n", odd_count);
}

void sort_and_write_to_text(const char *binary_filename,
                            const char *text_filename) {
  FILE *binary_file = fopen(binary_filename, "rb");
  if (!binary_file) {
    perror("Error opening binary file");
    exit(EXIT_FAILURE);
  }

  fseek(binary_file, 0, SEEK_END);
  long file_size = ftell(binary_file);
  fseek(binary_file, 0, SEEK_SET);

  size_t count = file_size / sizeof(int);
  int *numbers = malloc(file_size);
  if (!numbers) {
    perror("Memory allocation failed");
    fclose(binary_file);
    exit(EXIT_FAILURE);
  }

  fread(numbers, sizeof(int), count, binary_file);
  fclose(binary_file);

  for (size_t i = 0; i < count - 1; i++) {
    for (size_t j = i + 1; j < count; j++) {
      if (numbers[i] > numbers[j]) {
        int temp = numbers[i];
        numbers[i] = numbers[j];
        numbers[j] = temp;
      }
    }
  }

  FILE *text_file = fopen(text_filename, "w");
  if (!text_file) {
    perror("Error opening text file");
    free(numbers);
    exit(EXIT_FAILURE);
  }

  for (size_t i = 0; i < count; i++) {
    fprintf(text_file, "%d\n", numbers[i]);
  }

  fclose(text_file);
  free(numbers);
}

int main() {
  const char *binary_filename = "numbers.bin";
  const char *text_filename = "sorted_numbers.txt";

  create_binary_file(binary_filename);

  count_even_odd(binary_filename);

  sort_and_write_to_text(binary_filename, text_filename);

  return 0;
}