add_executable(sieve sieve.cpp)
target_link_libraries(sieve
  absl::flags
  absl::flags_parse)
