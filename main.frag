#version 330

in vec3 v_color;
out vec4 f_color;

void main() {
    // そのまま色を出力
    f_color = vec4(v_color, 1.0);
}