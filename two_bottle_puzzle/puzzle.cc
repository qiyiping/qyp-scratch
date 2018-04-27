#include "two_bottle_puzzle.h"
#include <pybind11/pybind11.h>

namespace py = pybind11;

PYBIND11_MODULE(puzzle, m) {
  m.doc() = "two bottle puzzle: given two bottle with volumn `v1` and `v2`, how to get some water of volumn `t`";
  m.def("solve", &solve, "solve the two bottle puzzle",
        py::arg("v1"), py::arg("v2"), py::arg("t"), py::arg("print_actions")=false);
}
