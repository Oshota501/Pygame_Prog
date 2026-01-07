#version 330

uniform mat4 rotation; // Pythonから受け取る回転行列
in vec3 in_vert;       // 頂点データ
in vec3 in_color;      // 色データ

out vec3 v_color;      // フラグメントシェーダーに渡す色

void main() {
    // 【重要】 ここで行列と頂点を掛け算して回転させている
    gl_Position = rotation * vec4(in_vert, 1.0);
    v_color = in_color;
}