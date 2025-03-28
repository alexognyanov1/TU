#include <stdio.h>

int main() {
  int A[3][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};

  int B[2][2] = {{5, 6}, {8, 9}};

  printf("Matrix A:\n");
  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
      printf("%d ", A[i][j]);
    }
    printf("\n");
  }

  printf("\nMatrix B:\n");
  for (int i = 0; i < 2; i++) {
    for (int j = 0; j < 2; j++) {
      printf("%d ", B[i][j]);
    }
    printf("\n");
  }

  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
      if (A[i][j] == B[0][0]) {
        int isSame = 1;
        for (int x = 0; x < 2; x++) {
          for (int y = 0; y < 2; y++) {
            if (A[i + x][j + y] != B[x][y]) {
              isSame = 0;
              break;
            }
          }
          if (isSame == 0) {
            break;
          }
        }

        if (isSame == 1) {
          printf("A contains B\n");
        } else {
          printf("A does not contain B\n");
        }
      }
    }
  }
}