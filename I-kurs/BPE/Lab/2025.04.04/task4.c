#include <stdio.h>
#include <stdlib.h>

void bubble_sort(int *arr, int n) {
  for (int i = 0; i < n; i++) {
    for (int j = i; j < n; j++) {
      if (arr[i] > arr[j]) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
      }
    }
  }
}

int main() {
  int n, m;

  scanf("%d %d", &n, &m);

  int *arr1 = (int *)malloc(sizeof(int) * n);
  int *arr2 = (int *)malloc(sizeof(int) * m);

  int *arr3 = (int *)malloc(sizeof(int) * (n + m));

  for (int i = 0; i < n; i++) {
    scanf("%d", &arr1[i]);
  }

  for (int i = 0; i < m; i++) {
    scanf("%d", &arr2[i]);
  }

  for (int i = 0; i < n + m; i++) {
    arr3[i] = i < n ? arr1[i] : arr2[i - n];
  }

  printf("Array1: ");
  for (int i = 0; i < n; i++) {
    printf("%d ", arr1[i]);
  }
  printf("\n");

  printf("Array2: ");
  for (int i = 0; i < m; i++) {
    printf("%d ", arr2[i]);
  }
  printf("\n");

  bubble_sort(arr3, n + m);

  printf("Sorted merged array: ");
  for (int i = 0; i < n + m; i++) {
    printf("%d ", arr3[i]);
  }
  printf("\n");

  free(arr1);
  free(arr2);
  free(arr3);
}