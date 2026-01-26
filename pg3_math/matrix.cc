#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
#include <pybind11/stl.h>
#include <string>
#include <array>
#include <vector>
#include <sstream>
#include <iomanip>
#include <cmath>

namespace py = pybind11;
using namespace std;

inline float radians(float degrees) {
    return degrees * 3.14159265359f / 180.0f;
}

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
    // 3dでよくある行列
    static Matrix4 get_identity() {
        Matrix4 i(array<float,16>({
            1.0f,0.0f,0.0f,0.0f,
            0.0f,1.0f,0.0f,0.0f,
            0.0f,0.0f,1.0f,0.0f,
            0.0f,0.0f,0.0f,1.0f
        })) ;
        return i ;
    }
    static Matrix4 get_translation (float x,float y,float z) {
        Matrix4 t(array<float,16>({
            1.0f,0.0f,0.0f,0.0f,
            0.0f,1.0f,0.0f,0.0f,
            0.0f,0.0f,1.0f,0.0f,
               x,   y,   z,1.0f
        })) ;
        return t ;
    }
    static Matrix4 get_perspective(float fov_degrees,float aspect_ratio,float near,float far) {
        float fov_rad = radians(fov_degrees);
        float f = 1.0 / tan(fov_rad / 2.0);
        Matrix4 t(array<float,16>({
            f/aspect_ratio,0.0f,0.0f,0.0f,
            0.0f,f,0.0f,0.0f,
            0.0f,0.0f,(far + near) / (near - far),-1.0f,
            0.0f,0.0f,(2.0f * far * near) / (near - far),1.0f
        })) ;
        return t ;
    }
    static Matrix4 get_scale(float x ,float y , float z) {
        Matrix4 s(array<float ,16>({
            x,0.0f, 0.0f, 0.0f,
            0.0f,y, 0.0f, 0.0f,
            0.0f,0.0f, z, 0.0f,
            0.0f,0.0f, 0.0f, 1.0f
        }));
        return s ;
    }
    static Matrix4 get_lookat (
        float eye_x ,float eye_y ,float eye_z ,
        float target_x ,float target_y ,float target_z ,
        float up_x=0.0f ,float up_y=1.0f ,float up_z=0.0f
    ) {
        // forward = normalize(target - eye)
        float forward_x = target_x - eye_x;
        float forward_y = target_y - eye_y;
        float forward_z = target_z - eye_z;
        float forward_len = sqrt(forward_x*forward_x + forward_y*forward_y + forward_z*forward_z);
        forward_x /= forward_len; forward_y /= forward_len; forward_z /= forward_len;
        
        // right = normalize(cross(forward, up))
        float right_x = forward_y * up_z - forward_z * up_y;
        float right_y = forward_z * up_x - forward_x * up_z;
        float right_z = forward_x * up_y - forward_y * up_x;
        float right_len = sqrt(right_x*right_x + right_y*right_y + right_z*right_z);
        right_x /= right_len; right_y /= right_len; right_z /= right_len;
        
        // up = normalize(cross(right, forward))
        float new_up_x = right_y * forward_z - right_z * forward_y;
        float new_up_y = right_z * forward_x - right_x * forward_z;
        float new_up_z = right_x * forward_y - right_y * forward_x;
        float new_up_len = sqrt(new_up_x*new_up_x + new_up_y*new_up_y + new_up_z*new_up_z);
        new_up_x /= new_up_len; new_up_y /= new_up_len; new_up_z /= new_up_len;
        
        // ビュー行列（転置された形で直接構成）
        // 行優先で格納して、列ベクトルの順序で転置
        Matrix4 rm(array<float,16>({
            right_x,   new_up_x,   -forward_x,   0.0f,
            right_y,   new_up_y,   -forward_y,   0.0f,
            right_z,   new_up_z,   -forward_z,   0.0f,
            -(right_x*eye_x + right_y*eye_y + right_z*eye_z),
            -(new_up_x*eye_x + new_up_y*eye_y + new_up_z*eye_z),
            (forward_x*eye_x + forward_y*eye_y + forward_z*eye_z),
            1.0f
        }));
        return rm;
    }
    static Matrix4 euler_angle (float x,float y,float z) {
        float Sx = sinf(x), Cx = cosf(x);
        float Sy = sinf(y), Cy = cosf(y);
        float Sz = sinf(z), Cz = cosf(z);
        return Matrix4(array<float,16>({
            Cz*Cy,                 -Sz*Cx + Cz*Sy*Sx,   Sz*Sx + Cz*Sy*Cx,   0.0f,
            Sz*Cy,                  Cz*Cx + Sz*Sy*Sx,  -Cz*Sx + Sz*Sy*Cx,   0.0f,
           -Sy,                     Cy*Sx,              Cy*Cx,               0.0f,
            0.0f,                    0.0f,               0.0f,               1.0f
        }));
    }
    static Matrix4 identity() { return Matrix4(); }
    // オーバーロード
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

    py::class_<Matrix4>(m, "Matrix4",py::buffer_protocol())
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

        .def_static("get_translation", &Matrix4::get_translation)
        .def_static("get_perspective", &Matrix4::get_perspective)
        .def_static("get_scale",&Matrix4::get_scale)
        .def_static("get_lookat",&Matrix4::get_lookat)
        .def_static("euler_angle",&Matrix4::euler_angle)
        // by gemini バッファプロトコルの作り方。
        .def_buffer([](Matrix4 &m) -> py::buffer_info {
            return py::buffer_info(
                m.data.data(),      // 1. データの先頭アドレス（ここを見ろ！）
                sizeof(float),          // 2. 要素1個のバイト数 (4byte)
                py::format_descriptor<float>::format(), // 3. 型はfloatだよ
                2,                      // 4. 次元の数 (4x4 なので 2次元)
                { 4, 4 },               // 5. 各次元のサイズ (縦4, 横4)
                
                // 6. ストライド（メモリ上で次の要素に行くために何バイト進むか）
                //    行を進むには float4個分(16byte)、列を進むには float1個分(4byte)
                { sizeof(float) * 4, sizeof(float) }
            );
        });
}