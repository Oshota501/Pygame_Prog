#version 330

in vec2 in_vert; // 2Dなので (x, y) だけでOK
in vec2 in_uv;

out vec2 v_uv;

uniform mat4 proj;  // Orthographic (正射影) 行列
uniform mat4 model; // 位置・回転・拡大縮小

void main() {
    // 2D座標を変換。Zは0.0固定、Wは1.0
    gl_Position = proj * model * vec4(in_vert, 0.0, 1.0);
    v_uv = in_uv;
}