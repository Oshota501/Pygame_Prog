#include <pybind11/pybind11.h>
#include <pybind11/operators.h> // これが必要です
#include <string>

namespace py = pybind11;
using namespace std;

struct Vector3 {
    float x, y, z;

    Vector3(float x, float y, float z) : x(x), y(y), z(z) {}

    Vector3 operator+(const Vector3 &other) const {
        return Vector3(x + other.x, y + other.y, z + other.z);
    }

    Vector3 operator-(const Vector3 &other) const {
        return Vector3(x - other.x, y - other.y, z - other.z);
    }
    
    string toString() const {
        return "Vector3(" + std::to_string(x) + ", " + std::to_string(y) + ", " + std::to_string(z) + ")";
    }
};

PYBIND11_MODULE(vector, m) {
    m.doc() = "Fast Vector3 implementation in C++";

    py::class_<Vector3>(m, "Vector3")
        .def(py::init<float, float, float>())
        .def_readwrite("x", &Vector3::x)
        .def_readwrite("y", &Vector3::y)
        .def_readwrite("z", &Vector3::z)
        .def("__repr__", &Vector3::toString)
        
        // これで Python の + が C++ の operator+ に繋がります
        .def(py::self + py::self)
        // 引き算も繋いでおきます
        .def(py::self - py::self);
}