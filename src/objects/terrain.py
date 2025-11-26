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
        length = 50.0
        depth = 0.6  # Increased depth - river channel goes deeper
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
        """Create vertices for ground with cutouts for river and road."""
        size = 30.0
        half = size / 2.0
        normal_x, normal_y, normal_z = 0.0, 1.0, 0.0
        
        # Repeat texture 5 times across the ground
        tex_repeat = 5.0
        
        vertices = []
        
        # River position (X: -3.0 +/- 4.0 = -7.0 to 1.0, Z: full length)
        # Road position (X: 2.0 +/- 0.3 = 1.7 to 2.3, Z: full length)
        river_x_min = -6.7
        river_x_max = 1.0
        road_x_min = 1.7
        road_x_max = 2.3
        z_min = -half
        z_max = half
        
        def add_quad(x1, x2, z1, z2, y_height=-0.25):
            """Add a quad using two triangles."""
            tex_x1 = (x1 + half) / size * tex_repeat
            tex_x2 = (x2 + half) / size * tex_repeat
            tex_z1 = (z1 + half) / size * tex_repeat
            tex_z2 = (z2 + half) / size * tex_repeat
            
            # Triangle 1
            vertices.extend([x1, y_height, z1,  normal_x, normal_y, normal_z,  tex_x1, tex_z1])
            vertices.extend([x2, y_height, z1,  normal_x, normal_y, normal_z,  tex_x2, tex_z1])
            vertices.extend([x2, y_height, z2,  normal_x, normal_y, normal_z,  tex_x2, tex_z2])
            
            # Triangle 2
            vertices.extend([x2, y_height, z2,  normal_x, normal_y, normal_z,  tex_x2, tex_z2])
            vertices.extend([x1, y_height, z2,  normal_x, normal_y, normal_z,  tex_x1, tex_z2])
            vertices.extend([x1, y_height, z1,  normal_x, normal_y, normal_z,  tex_x1, tex_z1])
        
        # Left ground (X: -30 to river_x_min) - lowered
        add_quad(-half, river_x_min, z_min, z_max, y_height=-0.35)
        
        # Right ground (X: road_x_max to 30)
        add_quad(road_x_max, half, z_min, z_max)
        
        # Middle ground between river and road (X: river_x_max to road_x_min)
        add_quad(river_x_max, road_x_min, z_min, z_max)
        
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