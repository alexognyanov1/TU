#include <stdio.h>

int main() {
  int arr[20] = {0};
  int count = 0;
  int num, index;

  while (count < 10) {
    scanf("%d", &arr[count]);
    count++;
  }

  while (count < 20) {
    scanf("%d", &num);
    if (num == 0) {
      break;
    }
    scanf("%d", &index);
    if (index < 0 || index > count) {
      printf("Error: Index out of bounds. Please enter a valid index.\n");
      continue;
    }
    for (int i = count; i > index; i--) {
      arr[i] = arr[i - 1];
    }
    arr[index] = num;
    count++;
  }

  for (int i = 0; i < count; i++) {
    printf("%d ", arr[i]);
  }

  printf("\n");

  return 0;
}