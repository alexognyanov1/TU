#include <stdio.h>

void createBinaryFile(const char *filename) {
  FILE *file = fopen(filename, "wb");
  if (!file) {
    perror("Error opening file");
    return;
  }

  int N;
  printf("Enter the number of integers (N): ");
  scanf("%d", &N);

  fwrite(&N, sizeof(int), 1, file);

  printf("Enter %d integers:\n", N);
  for (int i = 0; i < N; i++) {
    int num;
    scanf("%d", &num);
    fwrite(&num, sizeof(int), 1, file);
  }

  fclose(file);
  printf("Binary file '%s' created successfully.\n", filename);
}

int main() {
  createBinaryFile("numbers.bin");
  return 0;
}