#include <stdio.h>
#include <stdlib.h>

void print_backwards(char *bin, int index) {
  for (int i = index; i >= 0; i--) {
    printf("%c", bin[i]);
  }
  printf("\n");
}

char *binary_conversion(int n) {
  int curr_index = 0;
  char *binary = (char *)malloc(sizeof(char) * 32);

  while (n >= 1) {
    binary[curr_index] = '0' + n % 2;
    curr_index++;
    n /= 2;
  }
  binary[curr_index] = '\0';

  print_backwards(binary, curr_index);

  return binary;
}

int main() {
  int number;
  printf("Enter a number: ");
  scanf("%d", &number);

  char *binary = binary_conversion(number);

  free(binary);

  return 0;
}