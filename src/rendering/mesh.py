"""
Mesh class with texture support.
"""

import OpenGL.GL as gl
import numpy as np

class Mesh:
    def __init__(self, vertices, indices=None, texture=None):
        """
        Initialize mesh with vertex data and optional texture.
        """
        self.vertices = np.array(vertices, dtype=np.float32)
        self.indices = np.array(indices, dtype=np.uint32) if indices is not None else None
        self.texture = texture
        self.vao = None
        self.vbo = None
        self.ebo = None
        
        self._setup_mesh()
    
    def _setup_mesh(self):
        """Setup VAO, VBO for vertex data."""
        self.vao = gl.glGenVertexArrays(1)
        self.vbo = gl.glGenBuffers(1)
        
        gl.glBindVertexArray(self.vao)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, gl.GL_STATIC_DRAW)
        
        if self.indices is not None:
            self.ebo = gl.glGenBuffers(1)
            gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
            gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, gl.GL_STATIC_DRAW)
        
        # Vertex attributes: position(3), normal(3), texcoords(2) = 8 floats
        stride = 8 * 4
        
        # Position
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, stride, None)
        gl.glEnableVertexAttribArray(0)
        
        # Normal
        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, stride, gl.ctypes.c_void_p(3 * 4))
        gl.glEnableVertexAttribArray(1)
        
        # Texture coordinates
        gl.glVertexAttribPointer(2, 2, gl.GL_FLOAT, gl.GL_FALSE, stride, gl.ctypes.c_void_p(6 * 4))
        gl.glEnableVertexAttribArray(2)
        
        gl.glBindVertexArray(0)
    def draw(self, shader):
        """Render the mesh with texture."""
        # Bind texture if available
        if self.texture:
            self.texture.bind(0)
            shader.set_bool("useTexture", True)
            shader.set_int("texture0", 0)
        else:
            shader.set_bool("useTexture", False)
        
        gl.glBindVertexArray(self.vao)
        
        if self.indices is not None:
            gl.glDrawElements(gl.GL_TRIANGLES, len(self.indices), gl.GL_UNSIGNED_INT, None)
        else:
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, len(self.vertices) // 8)
        
        gl.glBindVertexArray(0)
    
    def __del__(self):
        """Clean up buffers."""
        try:
            if self.vao:
                gl.glDeleteVertexArrays(1, [self.vao])
            if self.vbo:
                gl.glDeleteBuffers(1, [self.vbo])
            if self.ebo:
                gl.glDeleteBuffers(1, [self.ebo])
        except:
            pass