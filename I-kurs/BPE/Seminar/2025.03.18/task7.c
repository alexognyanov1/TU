#include <stdio.h>

int main() {
  int arr[] = {4, 3, 1, 4, 2, 5, 8};
  int n = sizeof(arr) / sizeof(arr[0]);
  int target, sum, start;

  printf("Enter target sum: ");
  scanf("%d", &target);

  for (int i = 0; i < n; i++) {
    sum = 0;
    for (int j = i; j < n; j++) {
      sum += arr[j];
      if (sum == target) {
        for (int k = i; k <= j; k++) {
          printf("%d ", arr[k]);
        }
        printf("\n");
        return 0;
      }
    }
  }

  printf("No sequence found\n");
  return 0;
}