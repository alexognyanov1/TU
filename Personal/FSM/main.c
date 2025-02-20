#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_WORD_LENGTH 100

int total_numbers = 0;
int integer_constants = 0;
int unsigned_integers = 0;
int octal_numbers = 0;
int hex_numbers = 0;
int floating_points = 0;

int is_integer_constant(const char *word) {
  int i = 0;
  if (word[i] == '+' || word[i] == '-') {
    i++;
  }
  if (!isdigit(word[i])) {
    return 0;
  }
  while (isdigit(word[i])) {
    i++;
  }
  if (word[i] == 'U' || word[i] == 'u') {
    unsigned_integers++;
    i++;
  }
  if (word[i] == '\0') {
    return 1;
  }
  return 0;
}

int is_octal_constant(const char *word) {
  if (word[0] != '0' || !isdigit(word[1])) {
    return 0;
  }
  for (int i = 1; word[i] != '\0'; i++) {
    if (word[i] < '0' || word[i] > '7') {
      return 0;
    }
  }
  return 1;
}

int is_hex_constant(const char *word) {
  if (strlen(word) < 3 || word[0] != '0' ||
      (word[1] != 'x' && word[1] != 'X')) {
    return 0;
  }
  for (int i = 2; word[i] != '\0'; i++) {
    if (!isxdigit(word[i])) {
      return 0;
    }
  }
  return 1;
}

int is_floating_point(const char *word) {
  int i = 0, has_dot = 0, has_exponent = 0;
  if (word[i] == '+' || word[i] == '-') {
    i++;
  }
  while (isdigit(word[i])) {
    i++;
  }
  if (word[i] == '.') {
    has_dot = 1;
    i++;
  }
  while (isdigit(word[i])) {
    i++;
  }
  if (word[i] == 'e' || word[i] == 'E') {
    has_exponent = 1;
    i++;
    if (word[i] == '+' || word[i] == '-') {
      i++;
    }
    if (!isdigit(word[i])) {
      return 0;
    }
    while (isdigit(word[i])) {
      i++;
    }
  }
  if (word[i] == 'f' || word[i] == 'F' || word[i] == 'l' || word[i] == 'L') {
    i++;
  }
  if ((has_dot || has_exponent) && word[i] == '\0') {
    return 1;
  }
  return 0;
}

void process_word(const char *word) {
  if (is_integer_constant(word)) {
    integer_constants++;
  } else if (is_octal_constant(word)) {
    octal_numbers++;
  } else if (is_hex_constant(word)) {
    hex_numbers++;
  } else if (is_floating_point(word)) {
    floating_points++;
  } else {
    return;
  }
  total_numbers++;
}

void read_file(const char *filename) {
  FILE *file = fopen(filename, "r");
  if (!file) {
    perror("Error opening file");
    exit(EXIT_FAILURE);
  }
  char word[MAX_WORD_LENGTH];
  while (fscanf(file, "%s", word) == 1) {
    process_word(word);
  }
  fclose(file);
}

void print_results() {
  printf("Total numeric constants: %d\n", total_numbers);
  printf("Integer constants: %d\n", integer_constants);
  printf("Unsigned integers: %d\n", unsigned_integers);
  printf("Octal numbers: %d\n", octal_numbers);
  printf("Hexadecimal numbers: %d\n", hex_numbers);
  printf("Floating-point numbers: %d\n", floating_points);
}

int main(int argc, char *argv[]) {
  if (argc != 2) {
    printf("Usage: %s <filename>\n", argv[0]);
    return EXIT_FAILURE;
  }
  read_file(argv[1]);
  print_results();
  return EXIT_SUCCESS;
}
