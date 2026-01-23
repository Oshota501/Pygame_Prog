#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
#include <string>
#include <cmath>

// c++初心者なので書き方については許して
namespace py = pybind11;
using namespace std;

struct Vector3 {
    float x, y, z;

    Vector3(float x, float y, float z) : x(x), y(y), z(z) {}

    // +
    Vector3 operator+(const Vector3 &other) const {
        return Vector3(x + other.x, y + other.y, z + other.z);
    }
    Vector3 operator+(float s) const {
        return Vector3(x + s, y + s, z + s);
    }
    // -
    Vector3 operator-(const Vector3 &other) const {
        return Vector3(x - other.x, y - other.y, z - other.z);
    }
    Vector3 operator-(float s) const {
        return Vector3(x - s, y - s, z - s);
    }
    // *
    Vector3 operator*(const Vector3 &other) const {
        return Vector3(x*other.z,y*other.y,z*other.z) ;
    }
    Vector3 operator*(float s) const {
        return Vector3(x*s,y*s,z*s) ;
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
        
        .def(py::self + py::self)

        .def(py::self - py::self)

        .def(py::self * py::self);
}