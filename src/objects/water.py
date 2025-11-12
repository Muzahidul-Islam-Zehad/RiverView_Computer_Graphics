"""
Water class with proper blue color.
"""

import numpy as np
from rendering.mesh import Mesh
from utils.transformations import create_model_matrix

class Water:
    def __init__(self, shader):
        self.shader = shader
        self.water_mesh = None
        self.time = 0.0
        
        # Check shader
        if not self.shader.program_id:
            print("ERROR: Water shader failed to compile!")
        else:
            print(f"Water shader loaded: program {self.shader.program_id}")
        
        self._setup_water()
    
    def _create_water_vertices(self):
        """Create water mesh with proper normals."""
        vertices = []
        
        # Water dimensions
        width = 7.8
        length = 19.8
        base_height = 0.01  # Just above ground level so it's visible on top
        
        segments_x = 20
        segments_z = 40
        
        for i in range(segments_z):
            for j in range(segments_x):
                # Calculate vertex positions
                x = -width/2 + (width / segments_x) * j
                z = -length/2 + (length / segments_z) * i
                y = base_height
                
                # Calculate next vertices
                x1 = -width/2 + (width / segments_x) * (j + 1)
                z1 = -length/2 + (length / segments_z) * (i + 1)
                y1 = base_height
                
                # Water normals - pointing UP
                normal_x, normal_y, normal_z = 0.0, 1.0, 0.0
                
                # Create two triangles for each quad
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
        """Setup water mesh."""
        water_vertices = self._create_water_vertices()
        self.water_mesh = Mesh(water_vertices)
    
    def update(self, delta_time):
        """Update water animation."""
        self.time += delta_time
    
    def draw(self, view, projection, light_pos, view_pos):
        """Draw the blue water."""
        self.shader.use()
        self.shader.set_mat4("view", view)
        self.shader.set_mat4("projection", projection)
        self.shader.set_vec3("lightPos", light_pos)
        self.shader.set_vec3("viewPos", view_pos)
        self.shader.set_vec3("lightColor", (1.0, 1.0, 1.0))
        self.shader.set_float("time", self.time)
        
        # Water model matrix
        water_model = create_model_matrix(
            position=(-3.0, 0.0, 0.0),
            scale=(1.0, 1.0, 1.0)
        )
        
        self.shader.set_mat4("model", water_model)
        # NO objectColor set - water shader uses hardcoded blue
        self.water_mesh.draw(self.shader)