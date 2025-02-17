#include <stdio.h>

int main() {
  const char* numbers[] = {
    "one", "two", "three", "four", "five",
    "six", "seven", "eight", "nine", "ten"
  };

  for (int i = 0; i < 10; i++) {
    printf("%s\n", numbers[i]);
  }

  return 0;
}