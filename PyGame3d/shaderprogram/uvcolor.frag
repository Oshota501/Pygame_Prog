#version 330

uniform sampler2D u_texture;
uniform vec3 light_pos;
uniform vec3 view_pos;
uniform vec3 light_color;

in vec2 v_uv;
in vec3 v_norm;
in vec3 v_frag_pos;

out vec4 f_color;

void main() {
    vec3 norm = normalize(v_norm);
    vec3 lightDir = normalize(light_pos - v_frag_pos);

    // 1. Ambient (環境光)
    float ambientStrength = 0.45;
    vec3 ambient = ambientStrength * light_color;

    // 2. Diffuse (拡散光)
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * light_color;

    // 3. Specular (鏡面反射)
    float specularStrength = 0.5;
    vec3 viewDir = normalize(view_pos - v_frag_pos);
    vec3 reflectDir = reflect(-lightDir, norm);  
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32); // 32は輝き度（大きいほど鋭いハイライト）
    vec3 specular = specularStrength * spec * light_color;

    //4 
    vec4 texColor = texture(u_texture, v_uv);
    vec3 result = (ambient + diffuse + specular) * texColor.rgb;
    f_color = vec4(result, texColor.a);
}