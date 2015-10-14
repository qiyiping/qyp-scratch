/**
 * Incremental prime sieve described in:
 * "The Genuine Sieve of Eratosthenes"
 */

#ifndef _SIEVE_H_
#define _SIEVE_H_
#include <map>
#include <vector>
#include <queue>

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
        for (std::size_t i = 0; i < composite_[num].size(); ++i) {
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

// the improved version
// using priority queque
// please refer to:
// 3.1 Using a Better Data Structure
template <typename T>
class PrimeGenerator2: public Iteratable<T> {
 public:
  PrimeGenerator2(): num_generator_(2) {}
  virtual T Next() {
    while (true) {
      T num = num_generator_.Next();
      if (pq_.empty() || pq_.top().cutoff > num) {
        Cutoff c;
        c.prime = num;
        c.cutoff = num*num;
        pq_.push(c);
        return num;
      } else {
        while (pq_.top().cutoff == num) {
          Cutoff c = pq_.top();
          c.cutoff += c.prime;
          pq_.pop();
          pq_.push(c);
        }
      }
    }
  }
 private:
  struct Cutoff {
    T prime;
    T cutoff;
    bool operator > (const Cutoff &rhs) const { return cutoff > rhs.cutoff; }
  };
  std::priority_queue<Cutoff, std::vector<Cutoff>, std::greater<Cutoff> > pq_;
  NumGenerator<T> num_generator_;
};

#endif /* _SIEVE_H_ */
