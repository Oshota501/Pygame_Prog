#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
#include <pybind11/stl.h>
#include <string>
#include <array>
#include <vector>
#include <sstream>
#include <iomanip>

namespace py = pybind11;
using namespace std;

float EPSILON = 1.19209290E-07f; 

struct Matrix4 {
    array<array<float,4>,4> m;

    Matrix4() { set_identity(); }

    Matrix4(const array<float,16> &arr) {
        for (int i = 0; i < 16; ++i) m[i/4][i%4] = arr[i];
    }

    static Matrix4 from_list(const vector<float> &v) {
        Matrix4 r;
        if ((int)v.size() == 16) {
            for (int i = 0; i < 16; ++i) r.m[i/4][i%4] = v[i];
        } else {
            throw runtime_error("from_list requires 16 elements");
        }
        return r;
    }

    void set_identity() {
        for (int i = 0; i < 4; ++i)
            for (int j = 0; j < 4; ++j)
                m[i][j] = (i == j) ? 1.0f : 0.0f;
    }

    static Matrix4 identity() { return Matrix4(); }

    Matrix4 operator*(const Matrix4 &o) const {
        Matrix4 r;
        for (int i = 0; i < 4; ++i) {
            for (int j = 0; j < 4; ++j) {
                float s = 0.0f;
                for (int k = 0; k < 4; ++k) s += m[i][k] * o.m[k][j];
                r.m[i][j] = s;
            }
        }
        return r;
    }

    // operator* for 4-element vector (std::array)
    array<float,4> operator*(const array<float,4> &v) const {
        array<float,4> out;
        for (int i = 0; i < 4; ++i) {
            float s = 0.0f;
            for (int j = 0; j < 4; ++j) s += m[i][j] * v[j];
            out[i] = s;
        }
        return out;
    }

    // Vector3互換: 3要素を受け取り、w=1.0で補完
    vector<float> mul_vec3(py::iterable seq) const {
        vector<float> v;
        for (auto item : seq) {
            v.push_back(static_cast<float>(py::cast<double>(item)));
            if (v.size() == 3) break;
        }
        if (v.size() != 3) throw runtime_error("Expected iterable of length 3");
        
        // w=1.0 で補完して4要素にする
        vector<float> v4 = {v[0], v[1], v[2], 1.0f};
        vector<float> out(4, 0.0f);
        for (int i = 0; i < 4; ++i) {
            float s = 0.0f;
            for (int j = 0; j < 4; ++j) s += m[i][j] * v4[j];
            out[i] = s;
        }
        // 結果を3要素に戻す（斉次座標を正規化）
        if (out[3] != 0.0f) {
            out[0] /= out[3];
            out[1] /= out[3];
            out[2] /= out[3];
        }
        return {out[0], out[1], out[2]};
    }

    // 互換性のためのヘルパー（py::iterable を安全に float に変換）
    vector<float> mul_vec4(py::iterable seq) const {
        vector<float> v;
        for (auto item : seq) {
            v.push_back(static_cast<float>(py::cast<double>(item)));
            if (v.size() == 4) break;
        }
        if (v.size() != 4) throw runtime_error("Expected iterable of length 4");
        vector<float> out(4, 0.0f);
        for (int i = 0; i < 4; ++i) {
            float s = 0.0f;
            for (int j = 0; j < 4; ++j) s += m[i][j] * v[j];
            out[i] = s;
        }
        return out;
    }

    // .Tと同じです。
    Matrix4 transposed() const {
        Matrix4 r ;
        for (int i = 0; i < 4; ++i)
            for (int j = 0; j < 4; ++j)
                r.m[i][j] = m[j][i];
        return r;
    }
    Matrix4 T() const {
        Matrix4 r ;
        for (int i = 0; i < 4; ++i)
            for (int j = 0; j < 4; ++j)
                r.m[i][j] = m[j][i];
        return r;
    }

    array<float,16> to_array() const {
        array<float,16> a;
        for (int i = 0; i < 16; ++i) a[i] = m[i/4][i%4];
        return a;
    }

    string toString() const {
        ostringstream ss;
        ss << "Matrix4([\n";
        ss << fixed << setprecision(6);
        for (int i = 0; i < 4; ++i) {
            ss << "  [";
            for (int j = 0; j < 4; ++j) {
                ss << m[i][j];
                if (j < 3) ss << ", ";
            }
            ss << "]";
            if (i < 3) ss << ",\n";
        }
        ss << "\n])";
        return ss.str();
    }
    bool operator==(const Matrix4 &other) const {
        for(int i = 0 ; i < 4 ; i ++) {
            for(int j = 0 ; j < 4 ; j++) {
                if(abs(m[i][j] - other.m[i][j]) > EPSILON) return false;
            }
        }
        return true ;
    }
};

PYBIND11_MODULE(matrix, m) {
    m.doc() = "Matrix4 4x4 matrix";

    py::class_<Matrix4>(m, "Matrix4")
        .def(py::init<>())
        .def(py::init<const array<float,16>&>())
        .def_readwrite("m",&Matrix4::m)
        .def_static("from_list", [](py::iterable seq){
            vector<float> v;
            for (auto item : seq) v.push_back(static_cast<float>(py::cast<double>(item)));
            return Matrix4::from_list(v);
        })
        .def_static("identity", &Matrix4::identity)
        .def("__repr__", &Matrix4::toString)
        .def("to_list", [](const Matrix4 &self){
            auto a = self.to_array();
            py::list out;
            for (float f : a) out.append((double)f);
            return out;
        })
        .def("transposed", &Matrix4::transposed)
        .def("T",&Matrix4::T)

        // Matrix * Matrix
        .def("__mul__", [](const Matrix4 &A, const Matrix4 &B){ return A * B; })
        // Matrix * Vector3（3要素Iterable）← Vector3互換
        .def("__mul__", [](const Matrix4 &A, py::iterable v){
            auto res = A.mul_vec3(v);
            py::list out;
            for (float f : res) out.append((double)f);
            return out;
        })
        // Vector3 * Matrix
        .def("__rmul__", [](py::iterable v, const Matrix4 &A){
            auto res = A.mul_vec3(v);
            py::list out;
            for (float f : res) out.append((double)f);
            return out;
        })
        .def(py::self == py::self)
        .def("__getitem__", [](const Matrix4 &self, int i) -> array<float,4> {
            if (i < 0 || i >= 4) throw py::index_error("Matrix4 index out of range");
            return self.m[i];
        })
        .def("__setitem__", [](Matrix4 &self, int i, const array<float,4> &row) {
            if (i < 0 || i >= 4) throw py::index_error("Matrix4 index out of range");
            self.m[i] = row;
        })
        ;
}