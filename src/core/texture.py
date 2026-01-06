from __future__ import annotations

from PIL import Image
import OpenGL.GL as gl
import numpy as np

class Texture():
    def __init__(self: Texture, image_path: str) -> None:
        texture = gl.glGenTextures(1)
        img = Image.open(image_path).transpose(Image.FLIP_TOP_BOTTOM)
        img_data = np.array(list(img.getdata()), np.uint8)

        gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST_MIPMAP_LINEAR)

        img_format = gl.GL_RGB if img.mode == "RGB" else gl.GL_RGBA
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, img_format, img.size[0], img.size[1], 0, img_format, gl.GL_UNSIGNED_BYTE, img_data)

        gl.glGenerateMipmap(gl.GL_TEXTURE_2D)
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

        self._id = texture

    def use(self: Texture) -> None:
        gl.glBindTexture(gl.GL_TEXTURE_2D, self._id)

    def destroy(self: Texture) -> None:
        gl.glDeleteTextures(1, (self._id,))