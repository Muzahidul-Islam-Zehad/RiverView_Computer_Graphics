"""
Fallen log/wood piece for ground decoration.
"""

import numpy as np
import math
from rendering.mesh import Mesh
from utils.transformations import create_model_matrix


class Log:
    """A simple cylindrical fallen log."""
    
    def __init__(self, shader):
        self.shader = shader
        self.wood_texture = None
        
        # Load wood texture (optional)
        try:
            from core.texture import Texture
            self.wood_texture = Texture("assets/textures/log.png")
            print("✅ Wood texture loaded")
        except:
            self.wood_texture = None
        
        self._create_log_mesh()
    
    def _create_log_mesh(self):
        """Create a cylindrical log mesh."""
        vertices = []
        segments = 16  # Increased for smoother cylinder
        height = 1.2
        radius = 0.08  # Reduced from 0.15
        
        # Create cylinder standing vertically (along Y axis)
        for seg in range(segments):
            angle = (seg / segments) * 2 * math.pi
            x = radius * math.cos(angle)
            z = radius * math.sin(angle)
            
            # Normal pointing outward
            nx = math.cos(angle)
            nz = math.sin(angle)
            
            # Get next segment (wraps around to 0)
            angle_next = ((seg + 1) % segments / segments) * 2 * math.pi
            x_next = radius * math.cos(angle_next)
            z_next = radius * math.sin(angle_next)
            nx_next = math.cos(angle_next)
            nz_next = math.sin(angle_next)
            
            y_pos_bottom = -height / 2
            y_pos_top = height / 2
            
            # Triangle 1
            vertices.extend([x, y_pos_bottom, z, nx, 0.0, nz, seg/segments, 0.0])
            vertices.extend([x_next, y_pos_bottom, z_next, nx_next, 0.0, nz_next, (seg+1)/segments, 0.0])
            vertices.extend([x, y_pos_top, z, nx, 0.0, nz, seg/segments, 1.0])
            
            # Triangle 2
            vertices.extend([x_next, y_pos_bottom, z_next, nx_next, 0.0, nz_next, (seg+1)/segments, 0.0])
            vertices.extend([x_next, y_pos_top, z_next, nx_next, 0.0, nz_next, (seg+1)/segments, 1.0])
            vertices.extend([x, y_pos_top, z, nx, 0.0, nz, seg/segments, 1.0])
        
        self.log_mesh = Mesh(np.array(vertices, dtype=np.float32), texture=self.wood_texture)
    
    def draw(self, view, projection, light_pos, view_pos, position, rotation_y=0.0):
        """Draw the log at specified position."""
        self.shader.use()
        self.shader.set_mat4("view", view)
        self.shader.set_mat4("projection", projection)
        self.shader.set_vec3("lightPos", light_pos)
        self.shader.set_vec3("viewPos", view_pos)
        self.shader.set_vec3("lightColor", (1.0, 1.0, 1.0))
        
        # Logs are vertical pillars - no rotation needed
        model = create_model_matrix(position=position)
        self.shader.set_mat4("model", model)
        self.shader.set_vec3("objectColor", (0.5, 0.35, 0.15))  # Dark brown wood
        self.shader.set_bool("useTexture", self.wood_texture is not None)
        
        self.log_mesh.draw(self.shader)
