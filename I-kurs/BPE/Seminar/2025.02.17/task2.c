#include <stdio.h>

int main() {
  for (int i = 0; i < 10; i++) {
    for (int j = 0; j < i + 1; j++) {
      printf("%s", "*");
    }
    printf("\n");
  }

  return 0;
}