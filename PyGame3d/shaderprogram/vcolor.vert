#version 330

uniform mat4 model_opt; // オブジェクトごとの回転・移動 (Mesh.renderで渡す)
uniform mat4 position;
uniform mat4 rotation;
uniform mat4 scale;
uniform mat4 view;  // カメラの位置 (メインループで渡す)
uniform mat4 proj;  // 遠近感 (メインループで渡す)

in vec3 in_vert;
in vec3 in_color;  

out vec3 v_color;      // フラグメントシェーダーに渡す色

void main() {
    mat4 model = model_opt * position * rotation * scale ;
    gl_Position =  proj * view * model * vec4(in_vert, 1.0);
    v_color = in_color;
}