#include <pybind11/pybind11.h>
#include <pybind11/operators.h> // これが必要です
#include <string>

namespace py = pybind11;

struct Vector3 {
    float x, y, z;

    Vector3(float x, float y, float z) : x(x), y(y), z(z) {}

    // 【修正箇所】名前を 'add' から 'operator+' に変更します
    // これにより、C++の中でも "v1 + v2" と書けるようになり、py::self + py::self が動くようになります
    Vector3 operator+(const Vector3 &other) const {
        return Vector3(x + other.x, y + other.y, z + other.z);
    }

    // 引き算もあると便利なので追加しておきます
    Vector3 operator-(const Vector3 &other) const {
        return Vector3(x - other.x, y - other.y, z - other.z);
    }
    
    std::string toString() const {
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