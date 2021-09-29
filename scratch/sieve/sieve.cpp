#include "sieve/sieve.hpp"
#include <iostream>
#include "absl/flags/flag.h"
#include "absl/flags/parse.h"

ABSL_FLAG(int, number, 1, "the number-th prime");

int main(int argc, char *argv[]) {
  absl::ParseCommandLine(argc, argv);
  int ith = absl::GetFlag(FLAGS_number);

  // int64_t t1 = base::GetMicroSeconds();
  // PrimeGenerator<long long> p;
  // for (int i = 0; i < ith-1; ++i) {
  //   p.Next();
  //   // std::cout << p.Next() << " ";
  // }
  // std::cout << p.Next() << std::endl;
  // std::cout << base::GetMicroSeconds() - t1 << std::endl;

  // t1 = base::GetMicroSeconds();
  PrimeGenerator2<long long> p2;
  for (int i = 0; i < ith-1; ++i) {
    p2.Next();
    // std::cout << p2.Next() << " ";
  }
  std::cout << p2.Next() << std::endl;
  // std::cout << base::GetMicroSeconds() - t1 << std::endl;
  return 0;
}
