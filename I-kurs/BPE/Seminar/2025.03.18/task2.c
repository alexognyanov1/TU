#include <stdio.h>

int main() {
  int N;
  scanf("%d", &N);
  int arr[N];
  for (int i = 0; i < N; i++) {
    scanf("%d", &arr[i]);
  }

  int valid = 1;
  for (int i = 0; i < N - 1; i++) {
    if (i % 2 == 0) {
      if (arr[i] >= arr[i + 1]) {
        valid = 0;
        break;
      }
    } else {
      if (arr[i] <= arr[i + 1]) {
        valid = 0;
        break;
      }
    }
  }

  if (valid) {
    printf("Yes\n");
  } else {
    printf("No\n");
  }

  return 0;
}