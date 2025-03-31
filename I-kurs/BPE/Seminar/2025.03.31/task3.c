#include <stdio.h>

void print_arr(int *arr, int n, int m) {
  printf("\n\n");
  for (int i = 0; i < n; i++) {
    for (int j = 0; j < m; j++) {
      printf("%d ", *(arr + (i * n + j)));
    }
    printf("\n");
  }
}

int main() {
  int n, m;

  scanf("%d %d", &n, &m);

  int arr[n][m];

  for (int i = 0; i < n; i++) {
    for (int j = 0; j < m; j++) {
      scanf("%d", &arr[i][j]);
    }
  }

  print_arr(&arr[0][0], n, m);
  int temp[m];
  for (int i = 0; i < m; i++) {
    temp[i] = arr[0][i];
  }

  for (int i = 0; i < m; i++) {
    arr[0][i] = arr[n - 1][i];
  }

  for (int i = 0; i < m; i++) {
    arr[n - 1][i] = temp[i];
  }

  print_arr(&arr[0][0], n, m);
}