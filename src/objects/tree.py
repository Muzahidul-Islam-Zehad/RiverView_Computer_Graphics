"""
Tree class for the countryside trees.
"""

import numpy as np
from rendering.mesh import Mesh
from objects.primitives import create_cube_with_uv
from utils.transformations import create_model_matrix

class Tree:
    def __init__(self, shader):
        self.shader = shader
        self.trunk_mesh = None
        self.leaves_mesh = None
        
        self._setup_tree()
    
    def _setup_tree(self):
        """Setup tree components."""
        cube_vertices = create_cube_with_uv()
        self.trunk_mesh = Mesh(cube_vertices)
        self.leaves_mesh = Mesh(cube_vertices)
    
    def draw(self, view, projection, light_pos, view_pos, position=(0, 0, 0)):
        """Draw the tree at specified position."""
        self.shader.use()
        self.shader.set_mat4("view", view)
        self.shader.set_mat4("projection", projection)
        self.shader.set_vec3("lightPos", light_pos)
        self.shader.set_vec3("viewPos", view_pos)
        self.shader.set_vec3("lightColor", (1.0, 1.0, 1.0))
        
        # Tree trunk
        trunk_model = create_model_matrix(
            position=(position[0], 0.5, position[2]),
            scale=(0.1, 1.0, 0.1)
        )
        self.shader.set_mat4("model", trunk_model)
        self.shader.set_vec3("objectColor", (0.4, 0.2, 0.1))  # Brown trunk
        self.trunk_mesh.draw(self.shader)
        
        # Tree leaves (top part)
        leaves_model = create_model_matrix(
            position=(position[0], 1.5, position[2]),
            scale=(0.8, 0.8, 0.8)
        )
        self.shader.set_mat4("model", leaves_model)
        self.shader.set_vec3("objectColor", (0.1, 0.6, 0.1))  # Green leaves
        self.leaves_mesh.draw(self.shader)