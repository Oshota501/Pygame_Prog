#version 330

in vec3 v_color;
out vec4 f_color;

void main() {
    vec3 custom_color = vec3(1.0,1.0,1.0) ;
    f_color = vec4(v_color*custom_color, 1.0);
}