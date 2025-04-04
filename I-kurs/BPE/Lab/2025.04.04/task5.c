#include <stdio.h>
#include <stdlib.h>

int main() {
  int n;

  scanf("%d", &n);

  int **matrix = (int **)malloc(sizeof(int *) * n);
  for (int i = 0; i < n; i++) {
    matrix[i] = (int *)malloc(sizeof(int) * i);
  }

  matrix[0][0] = 1;
  matrix[0][1] = 1;

  for (int i = 0; i < n; i++) {
    for (int j = 0; j < i; j++) {
      if (j == 0 || j == i - 1) {
        matrix[i][j] = 1;
        continue;
      }

      matrix[i][j] = matrix[i - 1][j - 1] + matrix[i - 1][j];
    }
  }

  for (int i = 0; i < n; i++) {
    for (int j = 0; j < i; j++) {
      printf("%d ", matrix[i][j]);
    }
    printf("\n");
  }

  for (int i = 0; i < n; i++) {
    free(matrix[i]);
  }
  free(matrix);
}