/**
 * Incremental prime sieve described in:
 * "The Genuine Sieve of Eratosthenes"
 */

#ifndef _SIEVE_H_
#define _SIEVE_H_
#include <map>
#include <vector>

template <typename T>
class Iteratable {
  virtual T Next() = 0;
};

template <typename T>
class NumGenerator: public Iteratable<T> {
 public:
  NumGenerator(T seed): state_(seed) {}
  virtual T Next() { return state_++; }
 private:
  T state_;
};

template <typename T>
class PrimeGenerator: public Iteratable<T> {
 public:
  PrimeGenerator(): num_generator_(2) {}
  virtual T Next() {
    while (true) {
      T num = num_generator_.Next();
      if (composite_.find(num) == composite_.end()) {
        composite_[num*num] = std::vector<T>(1, num);
        return num;
      } else {
        for (size_t i = 0; i < composite_[num].size(); ++i) {
          if (composite_.find(num+composite_[num][i]) == composite_.end()) {
            composite_[num+composite_[num][i]] = std::vector<T>(1, composite_[num][i]);
          } else {
            composite_[num+composite_[num][i]].push_back(composite_[num][i]);
          }
        }
        composite_.erase(num);
      }
    }
  }
 private:
  std::map<T, std::vector<T> > composite_;
  NumGenerator<T> num_generator_;
};

#endif /* _SIEVE_H_ */
