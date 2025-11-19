"""
Terrain class with textures.
"""

import numpy as np
from rendering.mesh import Mesh
from core.texture import Texture
from utils.transformations import create_model_matrix

class Terrain:
    def __init__(self, shader):
        self.shader = shader
        self.ground_mesh = None
        self.river_channel_mesh = None
        self.grass_texture = None
        
        self._setup_terrain()
    
    def _create_river_channel_vertices(self):
        """Create vertices for river channel."""
        vertices = []
        width = 8.0
        length = 20.0
        depth = 0.3
        segments_x = 10
        segments_z = 20
        
        for i in range(segments_z):
            for j in range(segments_x):
                x = -width/2 + (width / segments_x) * j
                z = -length/2 + (length / segments_z) * i
                x1 = -width/2 + (width / segments_x) * (j + 1)
                z1 = -length/2 + (length / segments_z) * (i + 1)
                
                normal_x, normal_y, normal_z = 0.0, 1.0, 0.0
                
                # Triangle 1
                vertices.extend([x, -depth, z,  normal_x, normal_y, normal_z,  j/segments_x, i/segments_z])
                vertices.extend([x1, -depth, z,  normal_x, normal_y, normal_z,  (j+1)/segments_x, i/segments_z])
                vertices.extend([x, -depth, z1,  normal_x, normal_y, normal_z,  j/segments_x, (i+1)/segments_z])
                
                # Triangle 2
                vertices.extend([x1, -depth, z,  normal_x, normal_y, normal_z,  (j+1)/segments_x, i/segments_z])
                vertices.extend([x1, -depth, z1, normal_x, normal_y, normal_z,  (j+1)/segments_x, (i+1)/segments_z])
                vertices.extend([x, -depth, z1,  normal_x, normal_y, normal_z,  j/segments_x, (i+1)/segments_z])
        
        return np.array(vertices, dtype=np.float32)

    def _create_ground_vertices(self):
        """Create vertices for ground with proper texture coordinates."""
        size = 30.0
        half = size / 2.0
        normal_x, normal_y, normal_z = 0.0, 1.0, 0.0
        
        # Repeat texture 5 times across the ground for better visualization
        tex_repeat = 5.0
        
        vertices = [
            # Position (3), Normal (3), Texture Coords (2)
            # Triangle 1
            -half, -0.25, -half,  normal_x, normal_y, normal_z,  0.0, 0.0,
            half, -0.25, -half,  normal_x, normal_y, normal_z,  tex_repeat, 0.0,
            half, -0.25,  half,  normal_x, normal_y, normal_z,  tex_repeat, tex_repeat,
            
            # Triangle 2  
            half, -0.25,  half,  normal_x, normal_y, normal_z,  tex_repeat, tex_repeat,
            -half, -0.25,  half,  normal_x, normal_y, normal_z,  0.0, tex_repeat,
            -half, -0.25, -half,  normal_x, normal_y, normal_z,  0.0, 0.0,
        ]
        
        return np.array(vertices, dtype=np.float32)
    
    def _setup_terrain(self):
        """Setup ground and river channel with textures."""
        ground_vertices = self._create_ground_vertices()
        river_vertices = self._create_river_channel_vertices()
        
        # Load texture with debug info
        try:
            self.grass_texture = Texture("assets/textures/grass.png")
            print(f"✅ Grass texture loaded: {self.grass_texture.texture_id}")
        except Exception as e:
            print(f"❌ Grass texture failed: {e}")
            self.grass_texture = None
        
        self.ground_mesh = Mesh(ground_vertices, texture=self.grass_texture)
        self.river_channel_mesh = Mesh(river_vertices)
    
    def draw(self, view, projection, light_pos, view_pos):
        """Draw the terrain - FORCE TEXTURE."""
        self.shader.use()
        self.shader.set_mat4("view", view)
        self.shader.set_mat4("projection", projection)
        self.shader.set_vec3("lightPos", light_pos)
        self.shader.set_vec3("viewPos", view_pos)
        self.shader.set_vec3("lightColor", (1.0, 1.0, 1.0))
        
        # Draw ground WITH TEXTURE FORCED
        ground_model = create_model_matrix(position=(0.0, 0.0, 0.0))
        self.shader.set_mat4("model", ground_model)
        self.shader.set_bool("useTexture", True)  # FORCE TEXTURE
        self.ground_mesh.draw(self.shader)
        
        # Draw river channel WITHOUT TEXTURE
        river_channel_model = create_model_matrix(position=(-3.0, 0.0, 0.0))
        self.shader.set_mat4("model", river_channel_model)
        self.shader.set_bool("useTexture", False)  # No texture
        self.shader.set_vec3("objectColor", (0.6, 0.5, 0.3))
        self.river_channel_mesh.draw(self.shader)