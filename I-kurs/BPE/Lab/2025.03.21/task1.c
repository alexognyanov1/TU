#include <stdio.h>

int string_length(const char *str) {
  int length = 0;
  while (str[length] != '\0') {
    length++;
  }
  return length;
}

int main() {
  const char *testStr = "asdf";
  printf("Length of the string: %d\n", string_length(testStr));
  return 0;
}