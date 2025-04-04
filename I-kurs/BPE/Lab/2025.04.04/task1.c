#include <stdio.h>
#include <stdlib.h>

int main() {
  int n, m;

  scanf("%d %d", &n, &m);

  int *arr1 = (int *)malloc(sizeof(int) * n);
  int *arr2 = (int *)malloc(sizeof(int) * m);

  for (int i = 0; i < n; i++) {
    scanf("%d", &arr1[i]);
  }

  for (int i = 0; i < m; i++) {
    scanf("%d", &arr2[i]);
  }

  int sum1 = 0;
  int sum2 = 0;
  for (int i = 0; i < n; i++) {
    sum1 += arr1[i];
  }

  for (int i = 0; i < m; i++) {
    sum2 += arr2[i];
  }

  printf("Sum1: %d\nAvg1: %f\n\n", sum1, (double)sum1 / n);
  printf("Sum2: %d\nAvg2: %f", sum2, (double)sum2 / n);

  free(arr1);
  free(arr2);
}