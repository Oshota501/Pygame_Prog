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
    array<float,16> data;

    Matrix4() { set_identity(); }

    Matrix4(const array<float,16> &arr) {
        data = arr ;
    }
    Matrix4(const array<array<float,4>,4> &arr) {
        for (int i = 0; i < 4; ++i) {
            for (int j = 0; j < 4; ++j) {
                data[i*4+j] = arr[i][j];
            }
        }
    }

    static Matrix4 from_list(const vector<float> &v) {
        Matrix4 r;
        if ((int)v.size() == 16) {
            for (int i = 0; i < 16; ++i) r.data[i] = v[i];
        } else {
            throw runtime_error("from_list requires 16 elements");
        }
        return r;
    }

    void set_identity() {
        for (int i = 0; i < 4; ++i)
            for (int j = 0; j < 4; ++j)
                data[i*4+j] = (i == j) ? 1.0f : 0.0f;
    }
    static Matrix4 get_identity() {
        Matrix4 i(array<float,16>({
            1.0f,0.0f,0.0f,0.0f,
            0.0f,1.0f,0.0f,0.0f,
            0.0f,0.0f,1.0f,0.0f,
            0.0f,0.0f,0.0f,1.0f
        })) ;
        return i ;
    }

    static Matrix4 identity() { return Matrix4(); }

    Matrix4 operator*(const Matrix4 &o) const {
        Matrix4 r;
        for (int i = 0; i < 4; ++i) {
            for (int j = 0; j < 4; ++j) {
                float s = 0.0f;
                for (int k = 0; k < 4; ++k) s += data[i*4+k] * o.data[k*4+j];
                r.data[i*4+j] = s;
            }
        }
        return r;
    }

    // operator* for 4-element vector (std::array)
    array<float,4> operator*(const array<float,4> &v) const {
        array<float,4> out;
        for (int i = 0; i < 4; ++i) {
            float s = 0.0f;
            for (int j = 0; j < 4; ++j) s += data[i*4+j] * v[j];
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
            for (int j = 0; j < 4; ++j) s += data[i*4+j] * v4[j];
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
            for (int j = 0; j < 4; ++j) s += data[i*4+j] * v[j];
            out[i] = s;
        }
        return out;
    }

    // .Tと同じです。
    Matrix4 transposed() const {
        Matrix4 r ;
        for (int i = 0; i < 4; ++i)
            for (int j = 0; j < 4; ++j)
                r.data[i*4+j] = data[j*4+i];
        return r;
    }
    Matrix4 T() const {
        Matrix4 r ;
        for (int i = 0; i < 4; ++i)
            for (int j = 0; j < 4; ++j)
                r.data[i*4+j] = data[j*4+i];
        return r;
    }

    array<float,16> to_array() const {
        array<float,16> a;
        for (int i = 0; i < 16; ++i) a[i] = data[i];
        return a;
    }

    string toString() const {
        ostringstream ss;
        ss << "Matrix4([\n";
        ss << fixed << setprecision(6);
        for (int i = 0; i < 4; ++i) {
            ss << "  [";
            for (int j = 0; j < 4; ++j) {
                ss << data[i*4+j];
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
                if(abs(data[i*4+j] - other.data[i*4+j]) > EPSILON) return false;
            }
        }
        return true ;
    }

    void set_item (int line_index,int column_index,int value) {
        data[line_index*4+column_index] = value ;
        return ;
    }
    float get_item (int line_index,int column_index) {
        return data[line_index*4+column_index] ;
    }
    py::bytes tobytes() const {
        return py::bytes(
            reinterpret_cast<const char*>(data.data()), 
            sizeof(float) * 16
        );
    }
    array<float, 16> get_elements() const {
        return data;
    }
};

PYBIND11_MODULE(matrix, m) {
    m.doc() = "Matrix4 4x4 matrix";

    py::class_<Matrix4>(m, "Matrix4")
        .def(py::init<>())
        .def(py::init<const array<float,16>&>())
        .def(py::init<const array<array<float,4>,4>&>())
        .def_static("from_list", [](py::iterable seq){
            vector<float> v;
            for (auto item : seq) v.push_back(static_cast<float>(py::cast<double>(item)));
            return Matrix4::from_list(v);
        })
        .def_static("identity", &Matrix4::identity)
        .def_static("get_identity",&Matrix4::get_identity)
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
            array<float,4> row;
            for (int j = 0; j < 4; ++j) row[j] = self.data[i*4+j];
            return row;
        })
        .def("__setitem__", [](Matrix4 &self, int i, const array<float,4> &row) {
            if (i < 0 || i >= 4) throw py::index_error("Matrix4 index out of range");
            for (int j = 0; j < 4; ++j) self.data[i*4+j] = row[j];
        })
        .def("get_item", &Matrix4::get_item)
        .def("set_item", &Matrix4::set_item)
        .def("tobytes", &Matrix4::tobytes)
        .def("elements",&Matrix4::get_elements)
        ;
}