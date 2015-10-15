/*
 * Copyright (c) 2012 Yiping Qi <qiyiping at gmail dot com>
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * 1. Redistributions of source code must retain the above copyright
 * notice, this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright
 * notice, this list of conditions and the following disclaimer in the
 * documentation and/or other materials provided with the distribution.
 *
 * 3. Neither name of copyright holders nor the names of its contributors
 * may be used to endorse or promote products derived from this software
 * without specific prior written permission.
 *
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR
 * CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 * EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 * PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 * PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
 * NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */
#ifndef _BASE_TIME_H_
#define _BASE_TIME_H_
#include <sys/time.h>
#include <time.h>
#include <iostream>
#include <string>
#include "base/config.hpp"

namespace base {
inline int64_t GetMilliSeconds() {
  struct timeval tv;
  gettimeofday(&tv, NULL);
  return (tv.tv_sec*1000+tv.tv_usec/1000);
}

inline int64_t GetMicroSeconds() {
  struct timeval tv;
  gettimeofday(&tv, NULL);
  return (tv.tv_sec*1000000+tv.tv_usec);
}

inline void MilliSecondsToTimespec(int64_t ms, struct timespec *ts) {
  ts->tv_sec = ms/1000;
  ts->tv_nsec = (ms%1000)*1000000;
}

inline void MicroSeccondsToTimespec(int64_t us, struct timespec *ts) {
  ts->tv_sec = us/1000000;
  ts->tv_nsec = (us%1000000)*1000;
}

time_t TimeTFromTimeString(const std::string &time_string,
                           const std::string &format = "%Y-%m-%d %H:%M:%S");
std::string TimeStringFromTimeT(time_t t,
                                const std::string &format = "%Y-%m-%d %H:%M:%S");

class Timer {
 public:
  Timer(const std::string &hint): hint_(hint) { time_ = GetMilliSeconds(); }
  Timer() { time_ = GetMilliSeconds(); }
  int64_t GetElapsedTime() { return GetMilliSeconds() - time_; }
  ~Timer() { std::cout << hint_ << GetElapsedTime() << std::endl; }
 private:
  int64_t time_;
  const std::string hint_;
};

class Time;

class TimeDelta
{
 public:
  TimeDelta(int64_t us): delta_(us) {}

  static TimeDelta FromDays(int64_t days);
  static TimeDelta FromHours(int64_t hours);
  static TimeDelta FromMinutes(int64_t minutes);
  static TimeDelta FromSeconds(int64_t secs);
  static TimeDelta FromMilliseconds(int64_t ms);
  static TimeDelta FromMicroseconds(int64_t us);

  TimeDelta operator+(const TimeDelta &other) const { return TimeDelta(delta_ + other.delta_); }
  TimeDelta operator-(const TimeDelta &other) const { return TimeDelta(delta_ - other.delta_); }
  const TimeDelta& operator+=(const TimeDelta &other) { delta_ += other.delta_; return *this; }
  const TimeDelta& operator-=(const TimeDelta &other) { delta_ -= other.delta_; return *this; }
  template <typename T>
  TimeDelta operator*(const T &n) const { return TimeDelta(delta_ * n); }
  template <typename T>
  TimeDelta operator/(const T &n) const { return TimeDelta(delta_ / n); }
  template <typename T>
  const TimeDelta& operator*=(const T &n) { delta_ *= n; return *this; }
  template <typename T>
  const TimeDelta& operator/=(const T &n) { delta_ /= n; return *this; }

 private:
  friend class Time;

  int64_t delta_;
};

class Time
{
 public:
  static const int64_t kMillisecondsPerSecond = 1000;
  static const int64_t kMicrosecondsPerMillisecond = 1000;
  static const int64_t kMicrosecondsPerSecond = kMicrosecondsPerMillisecond *
                                                kMillisecondsPerSecond;
  static const int64_t kMicrosecondsPerMinute = kMicrosecondsPerSecond * 60;
  static const int64_t kMicrosecondsPerHour = kMicrosecondsPerMinute * 60;
  static const int64_t kMicrosecondsPerDay = kMicrosecondsPerHour * 24;
  static const int64_t kMicrosecondsPerWeek = kMicrosecondsPerDay * 7;
  static const int64_t kNanosecondsPerMicrosecond = 1000;
  static const int64_t kNanosecondsPerSecond = kNanosecondsPerMicrosecond *
                                               kMicrosecondsPerSecond;

  struct Exploded {
    int year;          // Four digit year "2007"
    int month;         // 1-based month (values 1 = January, etc.)
    int day_of_week;   // 0-based day of week (0 = Sunday, etc.)
    int day_of_month;  // 1-based day of month (1-31)
    int hour;          // Hour within the current day (0-23)
    int minute;        // Minute within the current hour (0-59)
    int second;        // Second within the current minute (0-59 plus leap
                       // seconds which may take it up to 60).
    int millisecond;   // Milliseconds within the current second (0-999)

    // A cursory test for whether the data members are within their
    // respective ranges. A 'true' return value does not guarantee the
    // Exploded value can be successfully converted to a Time value.
    bool HasValidValues() const;

    // Convert Exploded to struct tm
    void ToTM(struct tm *timestruct) const;
    // Convert struct tm to Exploded
    static Exploded FromTM(const struct tm &timestruct);
  };

  static Time Now();
  static Time FromTimeT(time_t t);
  static Time FromString(const std::string &timestring,
                         const std::string &format);
  static Time FromExploded(const Exploded &e);

  Time(int64_t us): us_(us) {}

  void Add(const TimeDelta &delta) { us_ += delta.delta_; }
  void Subtract(const TimeDelta &delta) { us_ -= delta.delta_; }

  time_t ToTimeT() const { return us_ / kMicrosecondsPerSecond; }

  std::string ToString(const std::string &format) const {
    return TimeStringFromTimeT(ToTimeT(), format);
  }

  Exploded ToExploded() const;

  Time operator+(const TimeDelta &delta) const { return Time(us_ + delta.delta_); }
  Time operator-(const TimeDelta &delta) const { return Time(us_ - delta.delta_); }
  const Time& operator+=(const TimeDelta &delta) { us_ += delta.delta_; return *this; }
  const Time& operator-=(const TimeDelta &delta) { us_ -= delta.delta_; return *this; }

  // Comparison operators
  bool operator==(Time other) const {
    return us_ == other.us_;
  }
  bool operator!=(Time other) const {
    return us_ != other.us_;
  }
  bool operator<(Time other) const {
    return us_ < other.us_;
  }
  bool operator<=(Time other) const {
    return us_ <= other.us_;
  }
  bool operator>(Time other) const {
    return us_ > other.us_;
  }
  bool operator>=(Time other) const {
    return us_ >= other.us_;
  }

 private:
  int64_t us_;
};


// static
inline TimeDelta TimeDelta::FromDays(int64_t days) {
  return TimeDelta(days * Time::kMicrosecondsPerDay);
}

// static
inline TimeDelta TimeDelta::FromHours(int64_t hours) {
  return TimeDelta(hours * Time::kMicrosecondsPerHour);
}

// static
inline TimeDelta TimeDelta::FromMinutes(int64_t minutes) {
  return TimeDelta(minutes * Time::kMicrosecondsPerMinute);
}

// static
inline TimeDelta TimeDelta::FromSeconds(int64_t secs) {
  return TimeDelta(secs * Time::kMicrosecondsPerSecond);
}

// static
inline TimeDelta TimeDelta::FromMilliseconds(int64_t ms) {
  return TimeDelta(ms * Time::kMicrosecondsPerMillisecond);
}

// static
inline TimeDelta TimeDelta::FromMicroseconds(int64_t us) {
  return TimeDelta(us);
}

inline Time Time::FromTimeT(time_t t) {
  return Time(t * kMicrosecondsPerSecond);
}

inline Time Time::FromString(const std::string &timestring,
                             const std::string &format) {
  return FromTimeT(TimeTFromTimeString(timestring, format));
}

}

#endif /* _BASE_TIME_H_ */
