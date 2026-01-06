#version 330 core
layout (location = 0) in vec3 position;
layout (location = 1) in vec2 a_texture_coordinates;

uniform mat4 MVP;

out vec2 texture_coordinates;

void main()
{
    texture_coordinates = a_texture_coordinates;
    gl_Position = MVP * vec4(position, 1.0);
}