#include "sieve/sieve.hpp"
#include "base/time.hpp"
#include <iostream>

int main(int argc, char *argv[]) {
  int ith = 100000;
  int64_t t1 = base::GetMicroSeconds();
  PrimeGenerator<long long> p;
  for (int i = 0; i < ith-1; ++i) {
    p.Next();
    // std::cout << p.Next() << " ";
  }
  std::cout << p.Next() << std::endl;
  std::cout << base::GetMicroSeconds() - t1 << std::endl;

  t1 = base::GetMicroSeconds();
  PrimeGenerator2<long long> p2;
  for (int i = 0; i < ith-1; ++i) {
    p2.Next();
    // std::cout << p2.Next() << " ";
  }
  std::cout << p2.Next() << std::endl;
  std::cout << base::GetMicroSeconds() - t1 << std::endl;
  return 0;
}
