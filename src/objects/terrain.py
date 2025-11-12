"""
Terrain class for ground and river.
"""

import numpy as np
from rendering.mesh import Mesh
from objects.primitives import create_plane
from utils.transformations import create_model_matrix

class Terrain:
    def __init__(self, shader):
        self.shader = shader
        self.ground_mesh = None
        self.river_mesh = None
        self._setup_terrain()
    
    def _setup_terrain(self):
        """Setup ground and river meshes."""
        self.ground_mesh = Mesh(create_plane(20.0))
        self.river_mesh = Mesh(create_plane(8.0))
    
    def draw(self, view, projection):
        """Draw the terrain."""
        self.shader.use()
        self.shader.set_mat4("view", view)
        self.shader.set_mat4("projection", projection)
        
        # Draw ground
        ground_model = create_model_matrix(position=(0.0, -0.1, 0.0))
        self.shader.set_mat4("model", ground_model)
        self.shader.set_vec3("objectColor", (0.2, 0.8, 0.2))  # Green
        self.ground_mesh.draw()
        
        # Draw river
        river_model = create_model_matrix(position=(-3.0, 0.0, 0.0), scale=(1.0, 1.0, 2.0))
        self.shader.set_mat4("model", river_model)
        self.shader.set_vec3("objectColor", (0.0, 0.5, 1.0))  # Blue
        self.river_mesh.draw()