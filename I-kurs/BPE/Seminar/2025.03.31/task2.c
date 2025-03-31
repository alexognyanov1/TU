#include <stdio.h>

int main() {
  int n, m;

  scanf("%d %d", &n, &m);

  int arr[n][m];

  for (int i = 0; i < n; i++) {
    for (int j = 0; j < m; j++) {
      scanf("%d", &arr[i][j]);
    }
  }

  long long maxSum = 0;
  int minVal;

  for (int i = 0; i < n; i++) {
    for (int j = 0; j < m; j++) {
      int sum = 0;
      for (int di = -1; di <= 1; di++) {
        for (int dj = -1; dj <= 1; dj++) {
          if (di == 0 && dj == 0) {
            continue;
          }
          int ni = i + di;
          int nj = j + dj;
          if (ni >= 0 && ni < n && nj >= 0 && nj < m) {
            sum += arr[ni][nj];
          }
        }
      }

      if (sum > maxSum) {
        maxSum = sum;
        minVal = arr[i][j];
      }
    }
  }

  printf("Max sum: %lld of element: %d\n", maxSum, minVal);
}