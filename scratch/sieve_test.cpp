#include "sieve.hpp"
#include <iostream>

int main(int argc, char *argv[]) {
  PrimeGenerator<long long> p;
  for (int i = 0; i < 20; ++i) {
    std::cout << p.Next() << std::endl;
  }
  return 0;
}
