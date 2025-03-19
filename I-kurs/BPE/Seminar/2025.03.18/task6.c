#include <stdio.h>

void findLongestSubsequence(int arr[], int n) {
  int maxLength = 1, length = 1, start = 0, end = 0;
  int i;

  for (i = 1; i < n; i++) {
    if (arr[i] > arr[i - 1]) {
      length++;
    } else {
      if (length > maxLength) {
        maxLength = length;
        end = i - 1;
        start = end - maxLength + 1;
      }
      length = 1;
    }
  }

  if (length > maxLength) {
    maxLength = length;
    end = i - 1;
    start = end - maxLength + 1;
  }

  length = 1;
  for (i = 1; i < n; i++) {
    if (arr[i] < arr[i - 1]) {
      length++;
    } else {
      if (length > maxLength) {
        maxLength = length;
        end = i - 1;
        start = end - maxLength + 1;
      }
      length = 1;
    }
  }

  if (length > maxLength) {
    maxLength = length;
    end = i - 1;
    start = end - maxLength + 1;
  }

  printf("Longest subsequence: ");
  for (i = start; i <= end; i++) {
    printf("%d ", arr[i]);
  }
  printf("\n");
}

int main() {
  int arr[] = {1, 2, 2, 1, 4, 5, 3, 2, 1, 0};
  int n = sizeof(arr) / sizeof(arr[0]);

  findLongestSubsequence(arr, n);

  return 0;
}