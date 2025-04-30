#include <stdio.h>
#include <string.h>

int areAnagrams(char *str1, char *str2) {
  if (strlen(str1) != strlen(str2)) {
    return 0;
  }

  int count[256] = {0};

  for (int i = 0; str1[i] != '\0'; i++) {
    count[(char)str1[i]]++;
    count[(char)str2[i]]--;
  }

  for (int i = 0; i < 256; i++) {
    if (count[i] != 0) {
      return 0;
    }
  }

  return 1;
}

int main() {
  char str1[] = "asdf";
  char str2[] = "123a";

  if (areAnagrams(str1, str2)) {
    printf("The strings are anagrams.\n");
  } else {
    printf("The strings are not anagrams.\n");
  }

  return 0;
}