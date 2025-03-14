#include <math.h>
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

  float avg = sum / 7.0;

  int index = 0;
  int minDiff = fabs(avg - arr[0]);
  for (int i = 1; i < 7; i++) {
    int diff = fabs(avg - arr[i]);
    if (diff < minDiff) {
      index = i;
      minDiff = diff;
    }
  }

  printf("val: %d\nindex: %d", arr[index], index);

  free(arr);
  return 0;
}