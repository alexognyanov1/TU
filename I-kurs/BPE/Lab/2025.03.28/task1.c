#include <stdio.h>

#define N 4

int main() {
  int matrix[N][N];
  int i, j;

  printf("Enter elements for a %dx%d matrix:\n", N, N);
  for (i = 0; i < N; i++) {
    for (j = 0; j < N; j++) {
      printf("Element [%d][%d]: ", i, j);
      scanf("%d", &matrix[i][j]);
    }
  }

  printf("\nMain diagonal elements:\n");
  for (i = 0; i < N; i++) {
    printf("%d ", matrix[i][i]);
  }
  printf("\n");

  printf("\nSecondary diagonal elements:\n");
  for (i = 0; i < N; i++) {
    printf("%d ", matrix[i][N - i - 1]);
  }
  printf("\n");

  printf("\nElements above the main diagonal:\n");
  for (i = 0; i < N; i++) {
    for (j = i + 1; j < N; j++) {
      printf("%d ", matrix[i][j]);
    }
  }
  printf("\n");

  printf("\nElements below the main diagonal:\n");
  for (i = 1; i < N; i++) {
    for (j = 0; j < i; j++) {
      printf("%d ", matrix[i][j]);
    }
  }
  printf("\n");

  return 0;
}