#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MIN_CAPACITY 10

typedef struct {
  char type[20];
  char model[30];
  int topSpeed;
  double l100km;
} Vehicle;

Vehicle scanVehicle() {
  char type[20];
  char model[30];
  int topSpeed;
  double l100km;

  printf("Type: ");
  fgets(type, 29, stdin);
  size_t len = strlen(type);
  if (len > 0 && type[len - 1] == '\n') {
    type[len - 1] = '\0';
  }

  printf("Model: ");
  fgets(model, 29, stdin);
  len = strlen(model);
  if (len > 0 && model[len - 1] == '\n') {
    model[len - 1] = '\0';
  }

  printf("Top Speed: ");
  scanf("%d%*c", &topSpeed);

  printf("L/100km: ");
  scanf("%lf%*c", &l100km);

  Vehicle v;
  strcpy(v.type, type);
  strcpy(v.model, model);
  v.topSpeed = topSpeed;
  v.l100km = l100km;

  return v;
}

void appendVehicle(Vehicle *vehicles, int *len, int *capacity, Vehicle v) {
  if (*len >= *capacity) {
    *capacity *= 2;
    vehicles = realloc(vehicles, sizeof(Vehicle) * (*capacity));
  }
  vehicles[*len] = v;
  (*len)++;
}

void printVehicles(Vehicle *vehicles, int len) {
  for (int i = 0; i < len; i++) {
    printf("Type: %s \n", vehicles[i].type);
    printf("Model: %s \n", vehicles[i].model);
    printf("Top Speed: %d \n", vehicles[i].topSpeed);
    printf("L/100km: %lf \n", vehicles[i].l100km);
    printf("\n");
  }
}

void sortByTopSpeed(Vehicle *vehicles, int len) {
  for (int i = 0; i < len - 1; i++) {
    for (int j = i + 1; j < len; j++) {
      if (vehicles[i].topSpeed > vehicles[j].topSpeed) {
        Vehicle temp = vehicles[i];
        vehicles[i] = vehicles[j];
        vehicles[j] = temp;
      }
    }
  }
}

int main() {
  Vehicle *vehicles = malloc(sizeof(Vehicle) * MIN_CAPACITY);
  int capacity = MIN_CAPACITY;
  int len = 0;

  for (int i = 0; i < 3; i++) {
    Vehicle v = scanVehicle();
    appendVehicle(vehicles, &len, &capacity, v);
  }

  printVehicles(vehicles, len);

  sortByTopSpeed(vehicles, len);

  printVehicles(vehicles, len);

  free(vehicles);
}
