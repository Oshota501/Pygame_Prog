#version 330

in vec2 v_uv;
out vec4 f_color;

uniform sampler2D texture0;
uniform vec4 color_tint; // 色を変えたい時用 (デフォルトは白 1.0, 1.0, 1.0, 1.0)

void main() {
    vec4 texColor = texture(texture0, v_uv);
    
    // UIなどは半透明合成(Blend)を使うことが多いですが、
    // ここでは簡易的に透過ピクセルを破棄する処理を入れています
    if (texColor.a < 0.01) {
        discard;
    }
    
    // テクスチャの色 * 乗算カラー (フェードアウト演出などに使える)
    f_color = texColor * color_tint;
}