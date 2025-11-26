"""
Road class with tiled texture.
"""

import numpy as np
from rendering.mesh import Mesh
from core.texture import Texture
from utils.transformations import create_model_matrix

class Road:
    def __init__(self, shader):
        self.shader = shader
        self.road_mesh = None
        self.road_texture = None
        
        self._setup_road()
    
    def _setup_road(self):
        """Setup road mesh with repeated texture tiles."""
        # Create a plane with repeated UVs for tiling
        # Each tile covers one unit, so we can repeat it multiple times
        size = 15.0
        half = size / 2.0
        
        # Repeat texture 4 times along the length (Z axis) and 2 times along width
        repeat_z = 4.0  # Repeat 4 times along length
        repeat_x = 2.0  # Repeat 2 times along width
        
        vertices = [
            # Front face with repeated UVs
            -half, 0.0, -half,  0.0, 1.0, 0.0,  0.0, 0.0,              # bottom-left
             half, 0.0, -half,  0.0, 1.0, 0.0,  repeat_x, 0.0,         # bottom-right
             half, 0.0,  half,  0.0, 1.0, 0.0,  repeat_x, repeat_z,    # top-right
             half, 0.0,  half,  0.0, 1.0, 0.0,  repeat_x, repeat_z,    # top-right
            -half, 0.0,  half,  0.0, 1.0, 0.0,  0.0, repeat_z,         # top-left
            -half, 0.0, -half,  0.0, 1.0, 0.0,  0.0, 0.0,              # bottom-left
        ]
        
        road_vertices = np.array(vertices, dtype=np.float32)
        
        # Load road texture
        try:
            self.road_texture = Texture("assets/textures/road.png")
        except:
            print("Road texture not found, using fallback color")
            self.road_texture = None
        
        self.road_mesh = Mesh(road_vertices, texture=self.road_texture)
    
    def draw(self, view, projection, light_pos, view_pos):
        """Draw the road with tiled texture."""
        self.shader.use()
        self.shader.set_mat4("view", view)
        self.shader.set_mat4("projection", projection)
        self.shader.set_vec3("lightPos", light_pos)
        self.shader.set_vec3("viewPos", view_pos)
        self.shader.set_vec3("lightColor", (1.0, 1.0, 1.0))
        
        road_model = create_model_matrix(
            position=(2.0, -0.1, 0.0),
            scale=(0.25, 1.0, 4.0)  # Extended length, lowered
        )
        self.shader.set_mat4("model", road_model)
        self.shader.set_bool("useTexture", True)
        self.road_mesh.draw(self.shader)