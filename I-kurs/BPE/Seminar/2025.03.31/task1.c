#include <stdio.h>

int main() {
  int is_ascending_rows = 1;
  int is_descending_cols = 1;

  int n, m;

  scanf("%d %d", &n, &m);

  int arr[n][m];

  for (int i = 0; i < n; i++) {
    for (int j = 0; j < m; j++) {
      scanf("%d", &arr[i][j]);
    }
  }

  for (int i = 0; i < n; i++) {
    for (int j = 0; j < m - 1; j++) {
      if (arr[i][j] > arr[i][j + 1]) {
        is_ascending_rows = 0;
        break;
      }
    }
  }

  for (int j = 0; j < m; j++) {
    for (int i = 0; i < n - 1; i++) {
      if (arr[i][j] < arr[i + 1][j]) {
        is_descending_cols = 0;
        break;
      }
    }
  }

  if (is_ascending_rows == 1) {
    printf("Rows ascending\n");
  } else {
    printf("Rows not ascending\n");
  }

  if (is_descending_cols == 1) {
    printf("Columns descending\n");
  } else {
    printf("Columns not descending\n");
  }
}