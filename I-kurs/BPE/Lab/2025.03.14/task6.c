#include <stdio.h>
#include <stdlib.h>

int main() {
  int *arr = (int *)malloc(sizeof(int) * 7);
  int a;

  for (int i = 0; i < 7; i++) {
    scanf("%d", &a);
    arr[i] = a;
  }

  int sum = 0;
  for (int i = 0; i < 7; i++) {
    sum += arr[i];
  }

  printf("%f\n", sum / 7.0);
  free(arr);
  return 0;
}