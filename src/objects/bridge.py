"""
Bridge class for the modern bridge spanning the river.
"""

import numpy as np
from rendering.mesh import Mesh
from objects.primitives import create_cube_with_uv
from utils.transformations import create_model_matrix

class Bridge:
    def __init__(self, shader):
        self.shader = shader
        self.pillar_mesh = None
        self.deck_mesh = None
        self.cable_mesh = None
        
        self._setup_bridge()
    
    def _setup_bridge(self):
        """Setup bridge components."""
        # Use cube for all parts, scaled differently
        cube_vertices = create_cube_with_uv()
        self.pillar_mesh = Mesh(cube_vertices)
        self.deck_mesh = Mesh(cube_vertices)
        self.cable_mesh = Mesh(cube_vertices)
    
    def draw(self, view, projection, light_pos, view_pos):
        """Draw the bridge."""
        self.shader.use()
        self.shader.set_mat4("view", view)
        self.shader.set_mat4("projection", projection)
        self.shader.set_vec3("lightPos", light_pos)
        self.shader.set_vec3("viewPos", view_pos)
        self.shader.set_vec3("lightColor", (1.0, 1.0, 1.0))
        
        # Draw bridge deck (main road)
        deck_model = create_model_matrix(
            position=(-3.0, 1.5, 0.0),
            scale=(8.0, 0.2, 0.8)
        )
        self.shader.set_mat4("model", deck_model)
        self.shader.set_vec3("objectColor", (0.4, 0.4, 0.4))  # Gray concrete
        self.deck_mesh.draw(self.shader)
        
        # Draw left pillar
        left_pillar_model = create_model_matrix(
            position=(-6.5, 0.5, 0.0),
            scale=(0.3, 2.0, 0.3)
        )
        self.shader.set_mat4("model", left_pillar_model)
        self.shader.set_vec3("objectColor", (0.5, 0.5, 0.5))  # Light gray
        self.pillar_mesh.draw(self.shader)
        
        # Draw right pillar
        right_pillar_model = create_model_matrix(
            position=(0.5, 0.5, 0.0),
            scale=(0.3, 2.0, 0.3)
        )
        self.shader.set_mat4("model", right_pillar_model)
        self.shader.set_vec3("objectColor", (0.5, 0.5, 0.5))  # Light gray
        self.pillar_mesh.draw(self.shader)
        
        # Draw cables (simple representation)
        for i in range(3):
            # Left cables
            cable_left_model = create_model_matrix(
                position=(-5.0 + i, 2.5, 0.0),
                scale=(0.1, 1.5, 0.1)
            )
            self.shader.set_mat4("model", cable_left_model)
            self.shader.set_vec3("objectColor", (0.8, 0.8, 0.8))  # White cables
            self.cable_mesh.draw(self.shader)
            
            # Right cables
            cable_right_model = create_model_matrix(
                position=(-1.0 + i, 2.5, 0.0),
                scale=(0.1, 1.5, 0.1)
            )
            self.shader.set_mat4("model", cable_right_model)
            self.shader.set_vec3("objectColor", (0.8, 0.8, 0.8))  # White cables
            self.cable_mesh.draw(self.shader)