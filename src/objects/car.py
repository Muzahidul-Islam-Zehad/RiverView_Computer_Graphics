"""
Simple car class for vehicles on the road.
"""

import numpy as np
from rendering.mesh import Mesh
from objects.primitives import create_cube_with_uv
from utils.transformations import create_model_matrix

class Car:
    def __init__(self, shader):
        self.shader = shader
        self.body_mesh = None
        self.wheel_mesh = None
        
        self._setup_car()
        self.position = [0.0, 0.0, 0.0]  # Starting position
        self.speed = 2.0  # Movement speed
    
    def _setup_car(self):
        """Setup car components."""
        cube_vertices = create_cube_with_uv()
        self.body_mesh = Mesh(cube_vertices)
        self.wheel_mesh = Mesh(cube_vertices)
    
    def update(self, delta_time):
        """Update car position (simple animation)."""
        # Move car along road
        self.position[2] += self.speed * delta_time
        
        # Reset position when car goes too far
        if self.position[2] > 12.0:
            self.position[2] = -12.0
    
    def draw(self, view, projection, light_pos, view_pos):
        """Draw the car."""
        self.shader.use()
        self.shader.set_mat4("view", view)
        self.shader.set_mat4("projection", projection)
        self.shader.set_vec3("lightPos", light_pos)
        self.shader.set_vec3("viewPos", view_pos)
        self.shader.set_vec3("lightColor", (1.0, 1.0, 1.0))
        
        # Car body
        body_model = create_model_matrix(
            position=(2.0, 0.3, self.position[2]),
            scale=(0.4, 0.2, 0.8)
        )
        self.shader.set_mat4("model", body_model)
        self.shader.set_vec3("objectColor", (0.9, 0.1, 0.1))  # Red car
        self.body_mesh.draw(self.shader)
        
        # Wheels
        wheel_positions = [
            (1.8, 0.15, self.position[2] - 0.3),  # Front left
            (2.2, 0.15, self.position[2] - 0.3),  # Front right
            (1.8, 0.15, self.position[2] + 0.3),  # Back left
            (2.2, 0.15, self.position[2] + 0.3),  # Back right
        ]
        
        for wheel_pos in wheel_positions:
            wheel_model = create_model_matrix(
                position=wheel_pos,
                scale=(0.1, 0.08, 0.1)
            )
            self.shader.set_mat4("model", wheel_model)
            self.shader.set_vec3("objectColor", (0.1, 0.1, 0.1))  # Black wheels
            self.wheel_mesh.draw(self.shader)