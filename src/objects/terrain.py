"""
Terrain class with proper river positioning.
"""

import numpy as np
from rendering.mesh import Mesh
from objects.primitives import create_plane_with_uv
from utils.transformations import create_model_matrix

class Terrain:
    def __init__(self, shader):
        self.shader = shader
        self.ground_mesh = None
        self.river_bed_mesh = None  # Renamed from river_mesh for clarity
        
        self._setup_terrain()
    
    def _setup_terrain(self):
        """Setup ground and river bed meshes."""
        ground_vertices = create_plane_with_uv(20.0)
        river_vertices = create_plane_with_uv(8.0)
        
        self.ground_mesh = Mesh(ground_vertices)
        self.river_bed_mesh = Mesh(river_vertices)
    
    def draw(self, view, projection, light_pos, view_pos):
        """Draw the terrain."""
        self.shader.use()
        self.shader.set_mat4("view", view)
        self.shader.set_mat4("projection", projection)
        self.shader.set_vec3("lightPos", light_pos)
        self.shader.set_vec3("viewPos", view_pos)
        self.shader.set_vec3("lightColor", (1.0, 1.0, 1.0))
        
        # Draw ground (green)
        ground_model = create_model_matrix(
            position=(0.0, -0.1, 0.0),  # Ground below water level
            scale=(1.0, 1.0, 1.0)
        )
        
        self.shader.set_mat4("model", ground_model)
        self.shader.set_vec3("objectColor", (0.2, 0.8, 0.2))
        self.ground_mesh.draw(self.shader)
        
        # Draw river bed (darker color, below water)
        river_bed_model = create_model_matrix(
            position=(-3.0, -0.05, 0.0),  # River bed slightly above ground
            scale=(1.0, 1.0, 2.0)
        )
        
        self.shader.set_mat4("model", river_bed_model)
        self.shader.set_vec3("objectColor", (0.1, 0.3, 0.6))  # Dark blue river bed
        self.river_bed_mesh.draw(self.shader)