#include <stdio.h>
#include <stdlib.h>

int main() {
  int n;
  scanf("%d", &n);

  int *arr = (int *)malloc(sizeof(int) * n);

  for (int i = 0; i < n; i++) {
    scanf("%d", &arr[i]);
  }

  printf("Do you want to add more elements? (Y/N) ");

  char choice;
  scanf(" %c", &choice);
  printf("\n");

  if (choice == 'Y') {
    int m;

    scanf("%d", &m);

    n += m;

    arr = realloc(arr, sizeof(int) * n);

    for (int i = n - m; i < n; i++) {
      scanf("%d", &arr[i]);
    }
  }
  printf("Array:\n");

  for (int i = 0; i < n; i++) {
    printf("%d ", arr[i]);
  }

  free(arr);
}