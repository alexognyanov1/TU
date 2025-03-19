#include <stdio.h>

void reverseArray(int arr[], int n) {
  int start = 0;
  int end = n - 1;
  while (start < end) {
    int temp = arr[start];
    arr[start] = arr[end];
    arr[end] = temp;
    start++;
    end--;
  }
}

int main() {
  int n;
  printf("Enter the number of elements: ");
  scanf("%d", &n);

  int arr[n];
  printf("Enter the elements: ");
  for (int i = 0; i < n; i++) {
    scanf("%d", &arr[i]);
  }

  reverseArray(arr, n);

  printf("Reversed array: ");
  for (int i = 0; i < n; i++) {
    printf("%d ", arr[i]);
  }
  printf("\n");

  return 0;
}