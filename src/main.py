import glfw
from OpenGL.GL import *
import glm
import numpy as np
import ctypes
import math
import time
import pathlib

from core import Shader, Texture, Window

class Camera: # thank you random github dude
    def __init__(self):
        self.position = glm.vec3(0, 0, 3)
        self.front = glm.vec3(0, 0, -1)
        self.up = glm.vec3(0, 1, 0)
        self.yaw = -90.0
        self.pitch = 0.0
        self.speed = 5.0
        self.sensitivity = 0.1

    def view_matrix(self):
        return glm.lookAt(self.position, self.position + self.front, self.up)

    def process_mouse(self, dx, dy):
        dx *= self.sensitivity
        dy *= self.sensitivity

        self.yaw += dx
        self.pitch += dy
        self.pitch = max(-89.0, min(89.0, self.pitch))

        direction = glm.vec3(
            math.cos(math.radians(self.yaw)) * math.cos(math.radians(self.pitch)),
            math.sin(math.radians(self.pitch)),
            math.sin(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        )
        self.front = glm.normalize(direction)

    def process_keyboard(self, window, dt):
        velocity = self.speed * dt
        right = glm.normalize(glm.cross(self.front, self.up))

        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
            self.position += self.front * velocity
        if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
            self.position -= self.front * velocity
        if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
            self.position -= right * velocity
        if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
            self.position += right * velocity

base_path = pathlib.Path(__file__).parent.absolute()

window = Window(glm.ivec2(1280, 720), "Zombie Game")

shader = Shader(
    base_path / 'shaders' / 'default.vert',
    base_path / 'shaders' / 'default.frag'
)

# just front for now
vertices = np.array([
    -0.5, -0.5,  0.5, 0, 0,
     0.5, -0.5,  0.5, 1, 0,
     0.5,  0.5,  0.5, 1, 1,
     0.5,  0.5,  0.5, 1, 1,
    -0.5,  0.5,  0.5, 0, 1,
    -0.5, -0.5,  0.5, 0, 0,
], dtype=np.float32)

VAO = glGenVertexArrays(1)
VBO = glGenBuffers(1)

glBindVertexArray(VAO)

glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(0))
glEnableVertexAttribArray(0)

glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(12))
glEnableVertexAttribArray(1)

texture = Texture(base_path / 'debug.png')

camera = Camera()
last_x, last_y = 640, 360
first_mouse = True
last_time = time.time()

def mouse_callback(window, x, y):
    global last_x, last_y, first_mouse
    if first_mouse:
        last_x, last_y = x, y
        first_mouse = False
    dx = x - last_x
    dy = last_y - y
    last_x, last_y = x, y
    camera.process_mouse(dx, dy)

glfw.set_cursor_pos_callback(window._window, mouse_callback)
glfw.set_input_mode(window._window, glfw.CURSOR, glfw.CURSOR_DISABLED)
glfw.swap_interval(0)

while window.tick():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    print("FPS:", 1 / window.delta_time)

    if glfw.get_key(window._window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window._window, True)

    camera.process_keyboard(window._window, window.delta_time)

    projection = glm.perspective(glm.radians(90), window.resolution.x / window.resolution.y, 0.01, 1024.0)
    view = camera.view_matrix()
    model = glm.mat4(1.0)
    mvp = projection * view * model

    shader.use()
    shader.set_mat4('MVP', mvp)

    texture.use()

    glBindVertexArray(VAO)
    glDrawArrays(GL_TRIANGLES, 0, len(vertices) // 5)

window.destroy()
glfw.terminate()