"""
Simple house class.
"""

from rendering.mesh import Mesh
from objects.primitives import create_cube
from utils.transformations import create_model_matrix

class House:
    def __init__(self, shader):
        self.shader = shader
        self.cube_mesh = Mesh(create_cube())
    
    def draw(self, view, projection, position=(0, 0, 0)):
        """Draw the house."""
        self.shader.use()
        self.shader.set_mat4("view", view)
        self.shader.set_mat4("projection", projection)
        
        model = create_model_matrix(position=position)
        self.shader.set_mat4("model", model)
        self.shader.set_vec3("objectColor", (0.8, 0.7, 0.6))  # Light brown
        self.cube_mesh.draw()