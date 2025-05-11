#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
  int id;
  char author[31];
  char name[31];
  float price;
} Picture;

Picture scanPicture() {
  Picture pic;

  scanf("%d", &pic.id);
  scanf("%s", pic.author);
  scanf("%s", pic.name);
  scanf("%f", &pic.price);

  return pic;
}

float averageWithThreshhold(Picture *pic, int n, float price) {
  float sum = 0;
  int count = 0;

  for (int i = 0; i < n; i++) {
    if (pic[i].price > price) {
      sum += pic[i].price;
      count++;
    }
  }

  return count == 0 ? 0 : sum / count;
}

int writeToFile(Picture *pic, int n, char c) {
  FILE *f = fopen("info.txt", "w+");

  if (f == NULL) {
    printf("Error opening file\n");
    exit(1);
  }

  int count = 0;

  for (int i = 0; i < n; i++) {
    if (tolower(pic[i].author[0]) == tolower(c)) {
      fprintf(f, "%d;%s;%.2fleva\n", pic[i].id, pic[i].name, pic[i].price);
      count++;
    }
  }

  fclose(f);

  return count;
}

void readFromFile(char author[31]) {
  FILE *f = fopen("info.bin", "r");

  if (f == NULL) {
    printf("Error opening file\n");
    exit(1);
  }

  int count = 0;
  int bufferLen = 255;
  char buffer[bufferLen];

  while (fgets(buffer, bufferLen, f)) {
    char *id = strtok(buffer, ";");
    char *authorLen = strtok(NULL, ";");
    char *fileAuthor = strtok(NULL, ";");
    if (strcmp(fileAuthor, author) != 0) {
      continue;
    }
    char *pictureNameLen = strtok(NULL, ";");
    char *pictureName = strtok(NULL, ";");
    char *price = strtok(NULL, ";");

    float picturePrice = strtof(price, NULL);

    count++;

    printf("Picture title: %s\nPrice: %.2f BGN\n", pictureName, picturePrice);
    printf("==============================\n");
  }

  if (count == 0) {
    printf("No matching pictures found!\n");
  }

  fclose(f);
}

int main() {
  int n;
  scanf("%d", &n);

  if (n < 4 || n > 29) {
    printf("Invalid n");
    exit(1);
  }

  Picture *pictures = calloc(n, sizeof(Picture));

  for (int i = 0; i < n; i++) {
    pictures[i] = scanPicture();
  }

  printf("AVERAGE: %.2f\n", averageWithThreshhold(pictures, n, 20.30));
  writeToFile(pictures, n, 'a');
  readFromFile("asdf");
}