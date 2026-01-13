#version 330
uniform sampler2D u_texture;

uniform mat4 model_opt;
uniform mat4 position;
uniform mat4 rotation;
uniform mat4 scale;
uniform mat4 view;
uniform mat4 proj;

in vec3 in_vert;
in vec2 in_uv;
out vec2 v_uv;

void main() {
    mat4 model = model_opt * position * rotation * scale ;
    gl_Position = proj * view * model * vec4(in_vert, 1.0);
    v_uv = in_uv;
}