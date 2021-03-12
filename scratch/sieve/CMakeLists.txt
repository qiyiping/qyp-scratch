add_executable(sieve_test sieve_test.cpp)
target_link_libraries(sieve_test PUBLIC base)
target_link_directories(sieve_test PUBLIC
  "${PROJECT_BINARY_DIR}")
