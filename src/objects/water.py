"""
Water class with texture support.
"""

import numpy as np
from rendering.mesh import Mesh
from core.texture import Texture
from utils.transformations import create_model_matrix

class Water:
    def __init__(self, shader):
        self.shader = shader
        self.water_mesh = None
        self.water_texture = None
        self.time = 0.0
        
        self._setup_water()
    
    def _create_water_vertices(self):
        """Create water mesh with texture coordinates."""
        vertices = []
        width = 7.8
        length = 19.8
        base_height = -0.05  # Water now above ground
        segments_x = 20
        segments_z = 40
        
        for i in range(segments_z):
            for j in range(segments_x):
                x = -width/2 + (width / segments_x) * j
                z = -length/2 + (length / segments_z) * i
                y = base_height
                x1 = -width/2 + (width / segments_x) * (j + 1)
                z1 = -length/2 + (length / segments_z) * (i + 1)
                y1 = base_height
                
                normal_x, normal_y, normal_z = 0.0, 1.0, 0.0
                
                # Triangle 1
                vertices.extend([x, y, z,  normal_x, normal_y, normal_z,  j/segments_x, i/segments_z])
                vertices.extend([x1, y1, z,  normal_x, normal_y, normal_z,  (j+1)/segments_x, i/segments_z])
                vertices.extend([x, y, z1,  normal_x, normal_y, normal_z,  j/segments_x, (i+1)/segments_z])
                
                # Triangle 2
                vertices.extend([x1, y1, z,  normal_x, normal_y, normal_z,  (j+1)/segments_x, i/segments_z])
                vertices.extend([x1, y1, z1, normal_x, normal_y, normal_z,  (j+1)/segments_x, (i+1)/segments_z])
                vertices.extend([x, y, z1,  normal_x, normal_y, normal_z,  j/segments_x, (i+1)/segments_z])
        
        return np.array(vertices, dtype=np.float32)
    
    def _setup_water(self):
        """Setup water mesh with texture."""
        water_vertices = self._create_water_vertices()
        
        # Load water texture
        try:
            print("Loading texture: assets/textures/water.png")
            self.water_texture = Texture("assets/textures/water.png")
            print(f"✅ Water texture loaded: {self.water_texture.texture_id}")
        except Exception as e:
            print(f"Water texture not found: {e}")
            self.water_texture = None
        
        self.water_mesh = Mesh(water_vertices, texture=self.water_texture)
    
    def update(self, delta_time):
        """Update water animation."""
        self.time += delta_time
    
    def draw(self, view, projection, light_pos, view_pos):
        """Draw the water."""
        self.shader.use()
        self.shader.set_mat4("view", view)
        self.shader.set_mat4("projection", projection)
        self.shader.set_vec3("lightPos", light_pos)
        self.shader.set_vec3("viewPos", view_pos)
        self.shader.set_vec3("lightColor", (1.0, 1.0, 1.0))
        self.shader.set_float("time", self.time)
        
        water_model = create_model_matrix(position=(-3.0, 0.0, 0.0))
        self.shader.set_mat4("model", water_model)
        self.shader.set_vec3("objectColor", (0.1, 0.5, 0.9))
        self.water_mesh.draw(self.shader)