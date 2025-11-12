"""
Road class with texture.
"""

import numpy as np
from rendering.mesh import Mesh
from objects.primitives import create_plane_with_uv
from core.texture import Texture
from utils.transformations import create_model_matrix

class Road:
    def __init__(self, shader):
        self.shader = shader
        self.road_mesh = None
        self.road_texture = None
        
        self._setup_road()
    
    def _setup_road(self):
        """Setup road mesh with texture."""
        road_vertices = create_plane_with_uv(15.0)
        
        # Load road texture
        try:
            self.road_texture = Texture("assets/textures/road.png")
        except:
            print("Road texture not found, using fallback color")
            self.road_texture = None
        
        self.road_mesh = Mesh(road_vertices, texture=self.road_texture)
    
    def draw(self, view, projection, light_pos, view_pos):
        """Draw the road - FORCE TEXTURE."""
        self.shader.use()
        self.shader.set_mat4("view", view)
        self.shader.set_mat4("projection", projection)
        self.shader.set_vec3("lightPos", light_pos)
        self.shader.set_vec3("viewPos", view_pos)
        self.shader.set_vec3("lightColor", (1.0, 1.0, 1.0))
        
        road_model = create_model_matrix(
            position=(2.0, 0.1, 0.0),
            scale=(0.5, 1.0, 1.5)
        )
        self.shader.set_mat4("model", road_model)
        self.shader.set_bool("useTexture", True)  # FORCE TEXTURE
        self.road_mesh.draw(self.shader)