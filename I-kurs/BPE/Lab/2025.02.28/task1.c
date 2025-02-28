#include <stdio.h>

int main() {
  int number;

  printf("Enter an integer: ");
  scanf("%d", &number);

  if (number % 2 == 0) {
    printf("The number is even.\n");
  } else {
    printf("The number is odd.\n");
  }

  if (number > 0) {
    printf("The number is positive.\n");
  } else if (number < 0) {
    printf("The number is negative.\n");
  } else {
    printf("The number is zero.\n");
  }

  if (number % 3 == 0 && number % 5 == 0) {
    printf("The number is divisible by both 3 and 5.\n");
  } else {
    printf("The number is not divisible by both 3 and 5.\n");
  }

  return 0;
}