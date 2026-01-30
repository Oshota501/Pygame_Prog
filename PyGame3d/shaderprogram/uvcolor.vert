#version 330

uniform mat4 model;
uniform mat4 view;
uniform mat4 proj;

in vec3 in_vert;
in vec2 in_uv;
in vec3 in_norm;

out vec2 v_uv;
out vec3 v_norm; 
out vec3 v_frag_pos;  

void main() {
    gl_Position = proj * view * model * vec4(in_vert, 1.0);
    mat3 N = transpose(inverse(mat3(model)));
    v_norm = N * in_norm;
    v_frag_pos = vec3(model * vec4(in_vert, 1.0));
    v_uv = in_uv;
}