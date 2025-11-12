"""
Road class positioned above water level.
"""

import numpy as np
from rendering.mesh import Mesh
from objects.primitives import create_plane_with_uv
from utils.transformations import create_model_matrix

class Road:
    def __init__(self, shader):
        self.shader = shader
        self.road_mesh = None
        
        self._setup_road()
    
    def _setup_road(self):
        """Setup road mesh."""
        road_vertices = create_plane_with_uv(15.0)
        self.road_mesh = Mesh(road_vertices)
    
    def draw(self, view, projection, light_pos, view_pos):
        """Draw the road above water level."""
        self.shader.use()
        self.shader.set_mat4("view", view)
        self.shader.set_mat4("projection", projection)
        self.shader.set_vec3("lightPos", light_pos)
        self.shader.set_vec3("viewPos", view_pos)
        self.shader.set_vec3("lightColor", (1.0, 1.0, 1.0))
        
        # Draw road ABOVE water level
        road_model = create_model_matrix(
            position=(2.0, 0.1, 0.0),  # Higher than water (0.1 vs -0.25)
            rotation=(0, 0, 0),
            scale=(0.5, 1.0, 1.5)
        )
        self.shader.set_mat4("model", road_model)
        self.shader.set_vec3("objectColor", (0.3, 0.3, 0.3))
        self.road_mesh.draw(self.shader)