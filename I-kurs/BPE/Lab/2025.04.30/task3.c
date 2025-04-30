#include <stdio.h>

#define MAX_BRAND 50
#define MODEL_LENGTH 5

typedef struct {
  char brand[MAX_BRAND];
  char model[MODEL_LENGTH + 1];
  float engine_volume;
  float price;
  char registration;
} Car;

void add_record(FILE *binary_file, FILE *text_file) {
  Car car;

  printf("Enter car brand: ");
  scanf("%s", car.brand);

  printf("Enter car model (5 characters): ");
  scanf("%s", car.model);

  printf("Enter engine volume: ");
  scanf("%f", &car.engine_volume);

  printf("Enter price: ");
  scanf("%f", &car.price);

  printf("Is the car registered? (Y/N): ");
  scanf(" %c", &car.registration);
  while (getchar() != '\n')
    ;

  fwrite(&car, sizeof(Car), 1, binary_file);
  fprintf(text_file, "%s %s %.2f %.2f %c\n", car.brand, car.model,
          car.engine_volume, car.price, car.registration);
}

void read_and_display_files(const char *binary_filename,
                            const char *text_filename) {
  FILE *binary_file = fopen(binary_filename, "rb");
  FILE *text_file = fopen(text_filename, "r");

  if (!binary_file || !text_file) {
    perror("Error opening files");
    return;
  }

  printf("\nData from binary file:\n");
  Car car;
  while (fread(&car, sizeof(Car), 1, binary_file)) {
    printf("%s %s %.2f %.2f %c\n", car.brand, car.model, car.engine_volume,
           car.price, car.registration);
  }

  printf("\nData from text file:\n");
  char line[256];
  while (fgets(line, sizeof(line), text_file)) {
    printf("%s", line);
  }

  fclose(binary_file);
  fclose(text_file);
}

int main() {
  const char *binary_filename = "cars.bin";
  const char *text_filename = "cars.txt";

  FILE *binary_file = fopen(binary_filename, "ab");
  FILE *text_file = fopen(text_filename, "a");

  if (!binary_file || !text_file) {
    perror("Error opening files");
    return 1;
  }

  int choice;
  do {
    printf("\n1. Add new record\n2. Display records\n3. Exit\nEnter your "
           "choice: ");
    scanf("%d", &choice);

    switch (choice) {
    case 1:
      add_record(binary_file, text_file);
      break;
    case 2:
      fclose(binary_file);
      fclose(text_file);
      read_and_display_files(binary_filename, text_filename);
      binary_file = fopen(binary_filename, "ab");
      text_file = fopen(text_filename, "a");
      break;
    case 3:
      printf("Exiting...\n");
      break;
    default:
      printf("Invalid choice. Try again.\n");
    }
  } while (choice != 3);

  fclose(binary_file);
  fclose(text_file);

  return 0;
}
