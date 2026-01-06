#version 330 core
in vec2 texture_coordinates;

out vec4 FragColor;

uniform sampler2D test_texture;

void main()
{
    FragColor = texture(test_texture, texture_coordinates);
}