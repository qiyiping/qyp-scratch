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

#include "base/time.hpp"

namespace base {

time_t TimeTFromTimeString(const std::string &time_string, const std::string &format) {
  time_t ret = -1;
  struct tm tm = {0};
  if (strptime(time_string.c_str(), format.c_str(), &tm) != NULL) {
    ret = mktime(&tm);
  }
  return ret;
}

std::string TimeStringFromTimeT(time_t t, const std::string &format) {
  char buf[100];
  strftime(buf, 100, format.c_str(), localtime(&t));
  return buf;
}

inline bool is_in_range(int value, int lo, int hi) {
  return lo <= value && value <= hi;
}

bool Time::Exploded::HasValidValues() const {
  return is_in_range(month, 1, 12) &&
      is_in_range(day_of_week, 0, 6) &&
      is_in_range(day_of_month, 1, 31) &&
      is_in_range(hour, 0, 23) &&
      is_in_range(minute, 0, 59) &&
      is_in_range(second, 0, 60) &&
      is_in_range(millisecond, 0, 999);
}

void Time::Exploded::ToTM(struct tm *timestruct) const {
  timestruct->tm_year = year - 1900;
  timestruct->tm_mon = month - 1;
  timestruct->tm_wday = day_of_week;
  timestruct->tm_mday = day_of_month;
  timestruct->tm_hour = hour;
  timestruct->tm_min = minute;
  timestruct->tm_sec = second;
}

Time::Exploded Time::Exploded::FromTM(const struct tm &timestruct) {
  Time::Exploded e;
  e.year = timestruct.tm_year + 1900;
  e.month = timestruct.tm_mon + 1;
  e.day_of_week = timestruct.tm_wday;
  e.day_of_month = timestruct.tm_mday;
  e.hour = timestruct.tm_hour;
  e.minute = timestruct.tm_min;
  e.second = timestruct.tm_sec;
  e.millisecond = 0;
  return e;
}

Time Time::Now() {
  struct timeval tv;
  struct timezone tz = { 0, 0 };
  if (gettimeofday(&tv, &tz) != 0) {
    return Time(0);
  }
  return Time(tv.tv_sec * kMicrosecondsPerSecond + tv.tv_usec);
}

Time Time::FromExploded(const Time::Exploded &e) {
  struct tm timestruct;
  e.ToTM(&timestruct);
  time_t t = mktime(&timestruct);
  return Time(t * kMicrosecondsPerSecond);
}

Time::Exploded Time::ToExploded() const {
  time_t t = us_ / kMicrosecondsPerSecond;
  struct tm timestruct;
  localtime_r(&t, &timestruct);
  return Time::Exploded::FromTM(timestruct);
}

}  // base
