#include <stdio.h>
#include <stdlib.h>

int main() {
  int *arr = (int *)malloc(sizeof(int) * 7);
  int a;

  for (int i = 0; i < 7; i++) {
    scanf("%d", &a);
    arr[i] = a;
  }

  int max = 0;
  for (int i = 0; i < 7; i++) {
    if (max < arr[i]) {
      max = arr[i];
    }
  }

  printf("%d", max);
  free(arr);
  return 0;
}