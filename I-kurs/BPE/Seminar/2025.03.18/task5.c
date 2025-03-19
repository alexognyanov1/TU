#include <stdio.h>

void swap(int *a, int *b) {
  int temp = *a;
  *a = *b;
  *b = temp;
}

void sort(int arr[], int n) {
  for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
      if (arr[i] < arr[j]) {
        swap(&arr[i], &arr[j]);
      }
    }
  }
}

int main() {
  int n, k;
  printf("Enter n: ");
  scanf("%d", &n);
  printf("Enter elements: ");
  int arr[n];
  for (int i = 0; i < n; i++) {
    scanf("%d", &arr[i]);
  }

  printf("Enter k:");
  scanf("%d", &k);
  while (k > n || k <= 0) {
    printf("Invalid. Enter k:");
    scanf("%d", &k);
  }
  sort(arr, n);

  printf("%d\n", arr[k - 1]);
  return 0;
}