#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MIN_CAPACITY 10

typedef struct {
  char name[40];
  int points;
} Student;

typedef struct {
  Student *students;
  int len;
  int capacity;
} Class;

typedef struct {
  Class *classes;
  int len;
  int capacity;
} Graduation;

Student scanStudent() {
  char name[40];
  int points;

  printf("Name: ");
  fgets(name, 39, stdin);
  size_t len = strlen(name);
  if (len > 0 && name[len - 1] == '\n') {
    name[len - 1] = '\0';
  }

  printf("Points: ");
  scanf("%d%*c", &points);

  Student s;
  strcpy(s.name, name);
  s.points = points;

  return s;
}

void appendToClass(Class *class, Student s) {
  if (class->len >= class->capacity) {
    class->capacity *= 2;
    class->students = realloc(class->students, class->capacity);
  }

  class->students[class->len] = s;
  class->len++;
}

void appendToGraduation(Graduation *grad, Class c) {
  if (grad->len >= grad->capacity) {
    grad->capacity *= 2;
    grad->classes = realloc(grad->classes, grad->capacity);
  }

  grad->classes[grad->len] = c;
  grad->len++;
}

Graduation *generateGrad() {
  Graduation *g = malloc(sizeof(Graduation));
  g->classes = malloc(sizeof(Class) * MIN_CAPACITY);
  g->len = 0;
  g->capacity = MIN_CAPACITY;

  return g;
}

Class *generateClass() {
  Class *c = malloc(sizeof(Class));
  c->students = malloc(sizeof(Student) * MIN_CAPACITY);
  c->len = 0;
  c->capacity = MIN_CAPACITY;

  return c;
}

void findAveragePoints(Graduation g) {
  int sumGlobal = 0;
  int lenGlobal = 0;

  for (int i = 0; i < g.len; i++) {
    int sumLocal = 0;
    for (int j = 0; j < g.classes[i].len; j++) {
      sumLocal += g.classes[i].students[j].points;
    }
    printf("Average for class at index %d: %lf\n", i,
           (double)sumLocal / g.classes[i].len);
    sumGlobal += sumLocal;
    lenGlobal += g.classes[i].len;
  }

  printf("Average for grad: %lf\n", (double)sumGlobal / lenGlobal);
}

int main() {
  int numClasses = 2;
  int numStudentsPerClass = 2;
  Graduation *g = generateGrad();

  for (int i = 0; i < numClasses; i++) {
    Class *c = generateClass();
    for (int j = 0; j < numStudentsPerClass; j++) {
      Student s = scanStudent();
      appendToClass(c, s);
    }
    appendToGraduation(g, *c);
  }

  findAveragePoints(*g);

  for (int i = 0; i < g->len; i++) {
    free(g->classes[i].students);
  }
  free(g->classes);
  free(g);
}