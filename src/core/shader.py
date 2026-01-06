from __future__ import annotations

import glm
import OpenGL.GL as gl

class Shader():
    def __init__(self: Shader, vertex_shader_path: str, fragment_shader_path: str) -> None:
        vertex_shader = self._load_shader(vertex_shader_path, gl.GL_VERTEX_SHADER)
        fragment_shader = self._load_shader(fragment_shader_path, gl.GL_FRAGMENT_SHADER)

        program_id = gl.glCreateProgram()
        gl.glAttachShader(program_id, vertex_shader)
        gl.glAttachShader(program_id, fragment_shader)

        gl.glLinkProgram(program_id)
        if gl.glGetProgramiv(program_id, gl.GL_LINK_STATUS) != gl.GL_TRUE:
            raise RuntimeError("Failed to link shader program!")
        gl.glUseProgram(program_id)

        gl.glDeleteShader(vertex_shader)
        gl.glDeleteShader(fragment_shader)

        self._id = program_id

    def _load_shader(self: Shader, source_path: str, shader_type: int) -> int:
        with open(source_path, 'r') as source_file:
            shader_source = source_file.read()

        shader_id = gl.glCreateShader(shader_type)
        gl.glShaderSource(shader_id, shader_source)
        gl.glCompileShader(shader_id)

        if gl.glGetShaderiv(shader_id, gl.GL_COMPILE_STATUS) != gl.GL_TRUE:
            raise RuntimeError(f"Failed to compile shader of type {shader_type.name} from '{source_path}'!\n{gl.glGetShaderInfoLog(shader_id)}")

        return shader_id

    def use(self: Shader) -> None:
        gl.glUseProgram(self._id)

    def destroy(self: Shader) -> None:
        gl.glDeleteProgram(self._id)

    def set_vec4(self: Shader, name: str, vec4: glm.vec4) -> None:
        gl.glUniform4fv(gl.glGetUniformLocation(self._id, name), 1, glm.value_ptr(vec4))

    def set_vec3(self: Shader, name: str, vec3: glm.vec3) -> None:
        gl.glUniform3fv(gl.glGetUniformLocation(self._id, name), 1, glm.value_ptr(vec3))

    def set_vec2(self: Shader, name: str, vec2: glm.vec2) -> None:
        gl.glUniform2fv(gl.glGetUniformLocation(self._id, name), 1, glm.value_ptr(vec2))

    def set_int(self: Shader, name: str, value: int) -> None:
        gl.glUniform1i(gl.glGetUniformLocation(self._id, name), value)

    def set_float(self: Shader, name: str, value: float) -> None:
        gl.glUniform1f(gl.glGetUniformLocation(self._id, name), value)

    def set_mat4(self: Shader, name: str, matrix: glm.mat4) -> None:
        gl.glUniformMatrix4fv(gl.glGetUniformLocation(self._id, name), 1, gl.GL_FALSE, glm.value_ptr(matrix))