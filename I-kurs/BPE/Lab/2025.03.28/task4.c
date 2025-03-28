#include <stdio.h>

int main() {
  int n;
  int m;
  scanf("%d %d", &n, &m);

  int arr[n][m];

  for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
      if (i % 2 == 0) {
        arr[i][j] = (i * n) + j;
      } else {
        arr[i][n - j - 1] = (i * n) + j;
      }
    }
  }

  for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
      printf("%d ", arr[i][j]);
    }
    printf("\n");
  }
}