#include <stdio.h>

int main() {
  int N;
  scanf("%d", &N);
  int arr[N];
  for (int i = 0; i < N; i++) {
    scanf("%d", &arr[i]);
  }

  int max_length = 1, current_length = 1, start_index = 0, max_start_index = 0;

  for (int i = 1; i < N; i++) {
    if (arr[i] == arr[i - 1]) {
      current_length++;
    } else {
      if (current_length > max_length) {
        max_length = current_length;
        max_start_index = start_index;
      }
      current_length = 1;
      start_index = i;
    }
  }

  if (current_length > max_length) {
    max_length = current_length;
    max_start_index = start_index;
  }

  printf("Index: %d\nLength:%d\n", max_start_index, max_length);
  return 0;
}