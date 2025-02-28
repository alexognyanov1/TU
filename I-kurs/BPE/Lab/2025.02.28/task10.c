#include <stdio.h>

int is_prime(int num) {
  if (num <= 1) {
    return 0;
  }
  for (int i = 2; i * i <= num; i++) {
    if (num % i == 0) {
      return 0;
    }
  }
  return 1;
}

int main() {
  int number;
  printf("Enter a number: ");
  scanf("%d", &number);

  if (is_prime(number)) {
    printf("The number %d is prime.\n", number);
  } else {
    printf("The number %d is not prime.\n", number);
  }

  return 0;
}