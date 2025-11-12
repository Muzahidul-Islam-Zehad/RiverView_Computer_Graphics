"""
House class with textures.
"""

from rendering.mesh import Mesh
from objects.primitives import create_cube_with_uv
from utils.transformations import create_model_matrix

class House:
    def __init__(self, shader):
        self.shader = shader
        self.cube_mesh = Mesh(create_cube_with_uv())
    
    def draw(self, view, projection, light_pos, view_pos, position=(0, 0, 0)):
        """Draw the house."""
        self.shader.use()
        self.shader.set_mat4("view", view)
        self.shader.set_mat4("projection", projection)
        self.shader.set_vec3("lightPos", light_pos)
        self.shader.set_vec3("viewPos", view_pos)
        self.shader.set_vec3("lightColor", (1.0, 1.0, 1.0))
        
        model = create_model_matrix(position=position)
        self.shader.set_mat4("model", model)
        self.shader.set_vec3("objectColor", (0.8, 0.7, 0.6))  # Light brown fallback
        self.cube_mesh.draw(self.shader)