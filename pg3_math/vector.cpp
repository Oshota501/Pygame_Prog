#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
#include <string>
#include <cmath>

// c++初心者なので書き方については許して
namespace py = pybind11;
using namespace std;


float EPSILON = 1.19209290E-07f; 

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
        return Vector3(x*other.x, y*other.y, z*other.z) ;
    }
    Vector3 operator*(float s) const {
        return Vector3(x*s,y*s,z*s) ;
    }

    // ｼﾞｮｻﾝ
    Vector3 operator/(const Vector3 &other) const {
        return Vector3(x/other.x,y/other.y,z/other.z) ;
    }
    Vector3 operator/(float s) const {
        float inv = 1/s ;
        return Vector3(x*inv,y*inv,z*inv) ;
    }

    // eq
    bool operator==(const Vector3 &other) const {
        return 
            std::abs(x-other.x) < EPSILON &&
            std::abs(y-other.y) < EPSILON &&
            std::abs(z-other.z) < EPSILON ;
    }

    
    string toString() const {
        return "Vector3(" + std::to_string(x) + ", " + std::to_string(y) + ", " + std::to_string(z) + ")";
    }
    
};

// 非メンバ演算子：数値 op ベクトル（python側の float + vec 等で必要）
inline Vector3 operator+(float s, const Vector3 &v) {
    return Vector3(v.x + s, v.y + s, v.z + s);
}
inline Vector3 operator-(float s, const Vector3 &v) {
    return Vector3(s - v.x, s - v.y, s - v.z);
}
inline Vector3 operator*(float s, const Vector3 &v) {
    return Vector3(v.x * s, v.y * s, v.z * s);
}

PYBIND11_MODULE(vector, m) {
    m.doc() = "Fast Vector3 implementation in C++";

    py::class_<Vector3>(m, "Vector3")
        .def(py::init<float, float, float>())
        .def_readwrite("x", &Vector3::x)
        .def_readwrite("y", &Vector3::y)
        .def_readwrite("z", &Vector3::z)
        .def("__repr__", &Vector3::toString)
        
        // 足し算
        .def(py::self + py::self)    // vec + vec
        .def(py::self + float())     // vec + float
        .def(float() + py::self)     // float + vec 

        // 引き算
        .def(py::self - py::self)    // vec - vec
        .def(py::self - float())     // vec - float
        .def(float() - py::self)     // float - vec

        // 掛け算
        .def(py::self * py::self)    // vec * vec
        .def(py::self * float())     // vec * float
        .def(float() * py::self)     // float * vec

        // 割り算 (Pythonの / 演算子は __truediv__)
        .def(py::self / py::self)    // vec / vec
        .def(py::self / float())     // vec / float
        
        // 比較
        .def(py::self == py::self);  // vec == vec
}