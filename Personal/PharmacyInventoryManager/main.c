#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MIN_CAPACITY 10

typedef struct {
  int month;
  int year;
} ExpiryDate;

typedef struct {
  char name[31];
  char expiryDate[8];
  long long id;
  double price;
  int quantity;
} Medicine;

void appendMedicine(Medicine *medicines, int *len, int *capacity,
                    Medicine newMed) {
  if (*len >= *capacity) {
    medicines = realloc(medicines, (*capacity) * 2);
    medicines[*len] = newMed;

    *capacity *= 2;
    *len += 1;
  } else {
    medicines[*len] = newMed;
    *len += 1;
  }
}

void checkToken(char *token) {
  if (token == NULL) {
    printf("invalid token\n");
    exit(2);
  }
}

void printMedicine(Medicine med) {
  printf("Name: %s\n", med.name);
  printf("Expiry Date: %s\n", med.expiryDate);
  printf("ID: %lld\n", med.id);
  printf("Price: %.2f\n", med.price);
  printf("Quantity: %d\n", med.quantity);
  printf("\n");
}

Medicine parseLine(char *line, size_t len) {
  Medicine med;
  char *token;

  token = strtok(line, ";");
  checkToken(token);
  strcpy(med.name, token);

  token = strtok(NULL, ";");
  checkToken(token);
  strcpy(med.expiryDate, token);

  token = strtok(NULL, ";");
  checkToken(token);
  med.id = atoll(token);

  token = strtok(NULL, ";");
  checkToken(token);
  med.price = atof(token);

  token = strtok(NULL, ";");
  checkToken(token);
  med.quantity = atoi(token);

  return med;
}

ExpiryDate dateStringToExpiryDate(char expiryDate[8]) {
  char *token;
  token = strtok(expiryDate, ".");
  checkToken(token);
  int month = atoi(token);

  token = strtok(NULL, "\0");
  checkToken(token);
  int year = atoi(token);

  ExpiryDate exp;
  exp.month = month;
  exp.year = year;

  return exp;
}

int isAfter(ExpiryDate exp1, ExpiryDate exp2) {
  if (exp1.year > exp2.year) {
    return 1;
  } else if (exp1.year < exp2.year) {
    return -1;
  } else if (exp1.month > exp2.month) {
    return 1;
  } else if (exp1.month < exp2.month) {
    return -1;
  } else {
    return 0;
  }
}

void discountExpiry(Medicine *medicines, int len, char expiryDate[8]) {
  ExpiryDate exp = dateStringToExpiryDate(expiryDate);

  for (int i = 0; i < len; i++) {
    ExpiryDate currExp = dateStringToExpiryDate(medicines[i].expiryDate);
    if (isAfter(exp, currExp) == 1) {
      double oldPrice = medicines[i].price;
      medicines[i].price *= 0.8;
      printf("%s - %s - %.2fлв - %.2fлв\n", medicines[i].name,
             medicines[i].expiryDate, oldPrice, medicines[i].price);
    }
  }
}

int main() {
  int medLen = 0;
  int medCapacity = MIN_CAPACITY;
  Medicine *medicines = malloc(sizeof(Medicine) * MIN_CAPACITY);

  FILE *file = fopen("medicines.txt", "r");

  if (file == NULL) {
    printf("Cannot open file\n");
    exit(1);
  }

  char *line = NULL;
  size_t len = 0;
  ssize_t read;

  while ((read = getline(&line, &len, file)) != -1) {
    Medicine newMed = parseLine(line, len);
    appendMedicine(medicines, &medLen, &medCapacity, newMed);
  }

  for (int i = 0; i < medLen; i++) {
    printMedicine(medicines[i]);
  }

  char expireDate[8] = "5.2025";
  discountExpiry(medicines, medLen, expireDate);

  if (line) {
    free(line);
  }

  free(medicines);
}