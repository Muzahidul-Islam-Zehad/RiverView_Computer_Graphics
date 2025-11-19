"""
Mountain class - Simple hill.
"""

import numpy as np
from rendering.mesh import Mesh
from objects.primitives import create_cube_with_uv
from utils.transformations import create_model_matrix

class Mountain:
    def __init__(self, shader):
        self.shader = shader
    
    def _draw_block(self, position, scale, color, use_texture=False):
        """Helper to draw a block."""
        cube_vertices = create_cube_with_uv()
        mesh = Mesh(cube_vertices, texture=None)
        
        model = create_model_matrix(position=position, scale=scale)
        self.shader.set_mat4("model", model)
        self.shader.set_vec3("objectColor", color)
        self.shader.set_bool("useTexture", False)
        
        mesh.draw(self.shader)
    
    def draw(self, view, projection, light_pos, view_pos):
        """Draw a simple 3-layer green hill at right back of bridge."""
        self.shader.use()
        self.shader.set_mat4("view", view)
        self.shader.set_mat4("projection", projection)
        self.shader.set_vec3("lightPos", light_pos)
        self.shader.set_vec3("viewPos", view_pos)
        self.shader.set_vec3("lightColor", (1.0, 1.0, 1.0))
        
        # Hill positioned at right back of bridge
        hill_x = 10.0
        hill_z = -8.0
        
        # Green colors
        light_green = (0.3, 0.8, 0.3)
        medium_green = (0.2, 0.7, 0.2)
        dark_green = (0.15, 0.6, 0.15)
        
        # Base layer - wide
        self._draw_block((hill_x, -0.5, hill_z), (8.0, 2.0, 5.0), dark_green)
        
        # Middle layer - medium
        self._draw_block((hill_x, 1.5, hill_z), (5.0, 2.0, 3.5), medium_green)
        
        # Top layer - narrow peak
        self._draw_block((hill_x, 3.5, hill_z), (2.0, 2.0, 1.5), light_green)

