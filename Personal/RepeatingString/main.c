#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

void setBit(int64_t *num, int bit) {
  *num |= (1LL << bit);
}

int getBit(int64_t num, int bit) {
  return (num & (1LL << bit)) != 0;
}

int checkIfRepeatingCharacter(char string[]){
  int64_t i1 = 0;
  int64_t i2 = 0;

  for (int i = 0; string[i] != '\0'; i++) {
    char c = string[i];

    if (c < 64) {
      if(getBit(i1, c)){
        return 1;
      }
      setBit(&i1, c);
    } else {
      if(getBit(i2, c - 64)){
        return 1;
      }
      setBit(&i1, c - 64);
    }
  }

  return 0; 
}

int main(){
  char string[] = "12344";

  printf("%d", checkIfRepeatingCharacter(string));

  return 0;
}