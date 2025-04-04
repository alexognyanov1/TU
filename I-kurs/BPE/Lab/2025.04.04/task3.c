#include <stdio.h>
#include <stdlib.h>

int main() {
  int n;
  scanf("%d", &n);

  int *arr = (int *)malloc(sizeof(int) * n);

  for (int i = 0; i < n; i++) {
    scanf("%d", &arr[i]);
  }

  printf("Element value to remove: ");
  int val;
  scanf("%d", &val);

  int index = -1;
  for (int i = 0; i < n; i++) {
    if (arr[i] == val) {
      index = i;
      break;
    }
  }

  if (index != -1) {
    printf("Element found, removing\n");
    for (int i = index; i < n - 1; i++) {
      arr[index] = arr[index + 1];
    }

    n--;
    arr = realloc(arr, sizeof(int) * n);
  } else {
    printf("Element not found\n");
  }

  printf("Array: \n");

  for (int i = 0; i < n; i++) {
    printf("%d ", arr[i]);
  }
  free(arr);
}