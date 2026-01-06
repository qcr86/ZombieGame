import glm
import glfw
import OpenGL.GL as gl

class Window():
    def __init__(self: Window, resolution: glm.ivec2, title: str) -> None:
        if not glfw.init():
            raise Exception("Failed to initialize GLFW!")

        window = glfw.create_window(resolution.x, resolution.y, title, None, None)
        if not window:
            glfw.terminate()
            raise Exception("Failed to create GLFW window!")

        glfw.make_context_current(window)
        glfw.set_framebuffer_size_callback(window, self._resize_callback)
        glfw.swap_interval(0)

        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_CULL_FACE)

        self._window = window
        self.resolution = resolution

        self._last_time = glfw.get_time()
        self.delta_time = 0.0

    def _resize_callback(self: Window, window: glfw._GLFWwindow, width: int, height: int) -> None:
        gl.glViewport(0, 0, width, height)
        self.resolution = glm.ivec2(width, height)

    def tick(self: Window) -> bool:
        glfw.make_context_current(self._window)

        if glfw.window_should_close(self._window):
            return False

        glfw.swap_buffers(self._window)
        glfw.poll_events()

        current_time = glfw.get_time()
        self.delta_time = current_time - self._last_time
        self._last_time = current_time

        return True

    def destroy(self: Window) -> None:
        glfw.destroy_window(self._window)