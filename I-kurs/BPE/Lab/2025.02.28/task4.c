#include <stdio.h>

int isPalindrome(int num) {
  int reversed = 0, original = num, remainder;

  while (num != 0) {
    remainder = num % 10;
    reversed = reversed * 10 + remainder;
    num /= 10;
  }

  return original == reversed;
}

int main() {
  int num;
  printf("Въведете число: ");
  scanf("%d", &num);

  if (isPalindrome(num)) {
    printf("Числото е палиндром.\n");
  } else {
    printf("Числото не е палиндром.\n");
  }

  return 0;
}