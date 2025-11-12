"""
Terrain class with proper river channel.
"""

import numpy as np
from rendering.mesh import Mesh
from utils.transformations import create_model_matrix

class Terrain:
    def __init__(self, shader):
        self.shader = shader
        self.ground_mesh = None
        self.river_channel_mesh = None
        
        self._setup_terrain()
    
    
    def _create_river_channel_vertices(self):
        """Create vertices for a river channel with proper normals."""
        vertices = []
        
        # River channel dimensions
        width = 8.0
        length = 20.0
        depth = 0.3
        
        segments_x = 10
        segments_z = 20
        
        for i in range(segments_z):
            for j in range(segments_x):
                # Calculate vertex positions
                x = -width/2 + (width / segments_x) * j
                z = -length/2 + (length / segments_z) * i
                
                # Calculate next vertices
                x1 = -width/2 + (width / segments_x) * (j + 1)
                z1 = -length/2 + (length / segments_z) * (i + 1)
                
                # RIVER CHANNEL NORMALS - pointing UP (0,1,0)
                normal_x, normal_y, normal_z = 0.0, 1.0, 0.0
                
                # Create two triangles for each quad
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
        """Create vertices for the ground plane with proper normals."""
        size = 30.0
        half = size / 2.0
        
        # GROUND NORMALS - pointing UP (0,1,0)
        normal_x, normal_y, normal_z = 0.0, 1.0, 0.0
        
        vertices = [
            # Ground plane - lowered so water sits above it
            -half, -0.2, -half,  normal_x, normal_y, normal_z,  0.0, 0.0,
            half, -0.2, -half,  normal_x, normal_y, normal_z,  1.0, 0.0,
            half, -0.2,  half,  normal_x, normal_y, normal_z,  1.0, 1.0,
            half, -0.2,  half,  normal_x, normal_y, normal_z,  1.0, 1.0,
            -half, -0.2,  half,  normal_x, normal_y, normal_z,  0.0, 1.0,
            -half, -0.2, -half,  normal_x, normal_y, normal_z,  0.0, 0.0,
        ]
        
        return np.array(vertices, dtype=np.float32)
    
    def _setup_terrain(self):
        """Setup ground and river channel meshes."""
        ground_vertices = self._create_ground_vertices()
        river_vertices = self._create_river_channel_vertices()
        
        self.ground_mesh = Mesh(ground_vertices)
        self.river_channel_mesh = Mesh(river_vertices)
    
    def draw(self, view, projection, light_pos, view_pos):
        """Draw the terrain."""
        self.shader.use()
        self.shader.set_mat4("view", view)
        self.shader.set_mat4("projection", projection)
        self.shader.set_vec3("lightPos", light_pos)
        self.shader.set_vec3("viewPos", view_pos)
        self.shader.set_vec3("lightColor", (1.0, 1.0, 1.0))
        
        # Draw ground
        ground_model = create_model_matrix(position=(0.0, 0.0, 0.0))
        self.shader.set_mat4("model", ground_model)
        self.shader.set_vec3("objectColor", (0.2, 0.8, 0.2))  # Green ground
        self.ground_mesh.draw(self.shader)
        
        # NOTE: River channel is now rendered by the Water object with proper shader
        # Don't render it here with the default shader