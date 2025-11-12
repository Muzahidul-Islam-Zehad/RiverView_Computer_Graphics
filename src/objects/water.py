"""
Water class with proper positioning and realistic waves.
"""

import numpy as np
from rendering.mesh import Mesh
from objects.primitives import create_plane_with_uv
from utils.transformations import create_model_matrix

class Water:
    def __init__(self, shader):
        self.shader = shader
        self.water_mesh = None
        self.time = 0.0
        
        self._setup_water()
    
    def _setup_water(self):
        """Setup water mesh."""
        water_vertices = create_plane_with_uv(8.0)
        self.water_mesh = Mesh(water_vertices)
    
    def update(self, delta_time):
        """Update water animation."""
        self.time += delta_time
    
    def draw(self, view, projection, light_pos, view_pos):
        """Draw the water with proper positioning."""
        self.shader.use()
        self.shader.set_mat4("view", view)
        self.shader.set_mat4("projection", projection)
        self.shader.set_vec3("lightPos", light_pos)
        self.shader.set_vec3("viewPos", view_pos)
        self.shader.set_vec3("lightColor", (1.0, 1.0, 1.0))
        self.shader.set_float("time", self.time)
        
        # Water model matrix - positioned at river level (0.0 Y)
        water_model = create_model_matrix(
            position=(-3.0, 0.0, 0.0),  # At ground level, not above
            scale=(1.0, 1.0, 2.0)
        )
        
        self.shader.set_mat4("model", water_model)
        self.shader.set_vec3("objectColor", (0.0, 0.3, 0.8))
        self.water_mesh.draw(self.shader)