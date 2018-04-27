#include "two_bottle_puzzle.h"

int main(int argc, char **argv) {
  int a, b, c;
  char line[100];

  while(fgets(line, sizeof(line), stdin)) {
    sscanf(line, "%d %d %d", &a, &b, &c);

    printf("=================\n");
    if (!solve(a, b, c, true)) {
      printf("No solution...\n");
    }
    printf("=================\n");
  }
  return 0;
}
