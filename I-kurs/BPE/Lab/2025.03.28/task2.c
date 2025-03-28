#include <stdbool.h>
#include <stdio.h>

#define SIZE 3

bool isMagicSquare(int square[SIZE][SIZE]) {
  int sum = 0, tempSum;

  for (int i = 0; i < SIZE; i++) {
    sum += square[0][i];
  }

  for (int i = 1; i < SIZE; i++) {
    tempSum = 0;
    for (int j = 0; j < SIZE; j++) {
      tempSum += square[i][j];
    }
    if (tempSum != sum) {
      return false;
    }
  }

  for (int i = 0; i < SIZE; i++) {
    tempSum = 0;
    for (int j = 0; j < SIZE; j++) {
      tempSum += square[j][i];
    }
    if (tempSum != sum) {
      return false;
    }
  }

  return true;
}

int main() {
  int square[SIZE][SIZE] = {{1, 1, 1}, {1, 1, 1}, {1, 1, 1}};
  int square1[SIZE][SIZE] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};

  if (isMagicSquare(square)) {
    printf("The square is magic.\n");
  } else {
    printf("The square is not magic.\n");
  }

  if (isMagicSquare(square1)) {
    printf("The square is magic.\n");
  } else {
    printf("The square is not magic.\n");
  }

  return 0;
}