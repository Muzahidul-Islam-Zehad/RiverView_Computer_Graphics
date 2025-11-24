"""
Pyramid roof class for the house.
"""

import numpy as np
import glm
from rendering.mesh import Mesh
from core.texture import Texture


class PyramidRoof:
    def __init__(self, shader):
        """Initialize pyramid roof."""
        self.shader = shader
        self.roof_texture = None
        self.mesh = None
        
        self._load_texture()
        self._create_mesh()
    
    def _load_texture(self):
        """Load roof texture."""
        try:
            self.roof_texture = Texture("assets/textures/houseRoof.png")
            print(f"Roof texture loaded: {self.roof_texture.texture_id}")
        except Exception as e:
            print(f"Roof texture not found: {e}")
    
    def _create_mesh(self):
        """Create pyramid mesh with 4 triangular faces."""
        vertices = []
        
        # Pyramid dimensions (fully stretch to cover entire house)
        width = 1.5
        depth = 1.3
        height = 0.8
        
        # Define base corners and peak
        base_fl = [-width/2, 0, depth/2]    # front-left
        base_fr = [width/2, 0, depth/2]     # front-right
        base_br = [width/2, 0, -depth/2]    # back-right
        base_bl = [-width/2, 0, -depth/2]   # back-left
        peak = [0, height, 0]                # peak
        
        # Helper function to compute face normal
        def get_face_normal(v1, v2, v3):
            """Compute normal for three vertices (counter-clockwise from outside)."""
            edge1 = np.array(v2) - np.array(v1)
            edge2 = np.array(v3) - np.array(v1)
            normal = np.cross(edge1, edge2)
            norm_length = np.linalg.norm(normal)
            if norm_length > 0:
                normal = normal / norm_length
            return list(normal)
        
        # Front face (facing +Z direction)
        n_front = get_face_normal(base_fl, base_fr, peak)
        vertices.append(base_fl + n_front + [0.0, 0.0])
        vertices.append(base_fr + n_front + [1.0, 0.0])
        vertices.append(peak + n_front + [0.5, 1.0])
        
        # Right face (facing +X direction)
        n_right = get_face_normal(base_fr, base_br, peak)
        vertices.append(base_fr + n_right + [0.0, 0.0])
        vertices.append(base_br + n_right + [1.0, 0.0])
        vertices.append(peak + n_right + [0.5, 1.0])
        
        # Back face (facing -Z direction)
        n_back = get_face_normal(base_br, base_bl, peak)
        vertices.append(base_br + n_back + [0.0, 0.0])
        vertices.append(base_bl + n_back + [1.0, 0.0])
        vertices.append(peak + n_back + [0.5, 1.0])
        
        # Left face (facing -X direction)
        n_left = get_face_normal(base_bl, base_fl, peak)
        vertices.append(base_bl + n_left + [0.0, 0.0])
        vertices.append(base_fl + n_left + [1.0, 0.0])
        vertices.append(peak + n_left + [0.5, 1.0])
        
        # Flatten the list of lists into a single list
        flat_vertices = []
        for vertex in vertices:
            flat_vertices.extend(vertex)
        
        vertices_array = np.array(flat_vertices, dtype=np.float32)
        self.mesh = Mesh(vertices_array)
    
    def draw(self, view, projection, light_pos, view_pos, position=(0, 0, 0)):
        """Draw the pyramid roof."""
        self.shader.use()
        self.shader.set_mat4("view", view)
        self.shader.set_mat4("projection", projection)
        self.shader.set_vec3("lightPos", light_pos)
        self.shader.set_vec3("viewPos", view_pos)
        self.shader.set_vec3("lightColor", (1.0, 1.0, 1.0))
        
        # Create model matrix
        model = glm.translate(glm.mat4(1.0), glm.vec3(position[0], position[1], position[2]))
        self.shader.set_mat4("model", model)
        
        # Set roof color
        roof_color = (0.6, 0.3, 0.2)
        self.shader.set_vec3("objectColor", roof_color)
        
        # Apply texture
        if self.roof_texture:
            self.roof_texture.bind(0)
            self.shader.set_sampler("texture_diffuse1", 0)
            self.shader.set_bool("useTexture", True)
        else:
            self.shader.set_bool("useTexture", False)
        
        # Draw mesh
        self.mesh.draw(self.shader)
        
        self.shader.set_bool("useTexture", False)
