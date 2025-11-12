"""
Mesh class for handling vertex data, buffers, and rendering.
"""

import OpenGL.GL as gl
import numpy as np

class Mesh:
    def __init__(self, vertices, indices=None):
        """
        Initialize mesh with vertex data.
        
        Args:
            vertices: numpy array of vertices
            indices: optional numpy array of indices for indexed drawing
        """
        self.vertices = np.array(vertices, dtype=np.float32)
        self.indices = np.array(indices, dtype=np.uint32) if indices is not None else None
        self.vao = None
        self.vbo = None
        self.ebo = None
        
        self._setup_mesh()
    
    def _setup_mesh(self):
        """Setup VAO, VBO, and optionally EBO."""
        # Generate buffers
        self.vao = gl.glGenVertexArrays(1)
        self.vbo = gl.glGenBuffers(1)
        
        # Bind VAO first
        gl.glBindVertexArray(self.vao)
        
        # Bind and set vertex buffer
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, gl.GL_STATIC_DRAW)
        
        # Set up EBO if indices are provided
        if self.indices is not None:
            self.ebo = gl.glGenBuffers(1)
            gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
            gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, gl.GL_STATIC_DRAW)
        
        # Configure vertex attributes (position only)
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 3 * 4, None)
        gl.glEnableVertexAttribArray(0)
        
        # Unbind VAO
        gl.glBindVertexArray(0)
    
    def draw(self):
        """Render the mesh."""
        gl.glBindVertexArray(self.vao)
        
        if self.indices is not None:
            gl.glDrawElements(gl.GL_TRIANGLES, len(self.indices), gl.GL_UNSIGNED_INT, None)
        else:
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, len(self.vertices) // 3)
        
        gl.glBindVertexArray(0)