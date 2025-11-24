"""
Simple Christmas tree with layered cones.
"""

import numpy as np
import glm
from rendering.mesh import Mesh
from core.texture import Texture
from utils.transformations import create_model_matrix


class ChristmasTree:
    # Class-level texture shared by all instances
    _shared_texture = None
    _texture_loaded = False
    
    def __init__(self, shader):
        """Initialize Christmas tree."""
        self.shader = shader
        self.tree_parts = []
        # Load texture once for all instances
        if not ChristmasTree._texture_loaded:
            self._load_texture_once()
        self._create_tree()
    
    @classmethod
    def _load_texture_once(cls):
        """Load the Christmas tree texture once for all instances."""
        try:
            cls._shared_texture = Texture("assets/textures/christmas_tree.png")
            cls._texture_loaded = True
            print("✅ Christmas tree texture loaded once (shared)")
        except Exception as e:
            print(f"Failed to load christmas_tree.png: {e}")
            cls._shared_texture = None
            cls._texture_loaded = True
    
    @property
    def tree_texture(self):
        """Return the shared texture."""
        return ChristmasTree._shared_texture

    def _create_cone_mesh(self, radius, height, segments=16):
        """Create a cone mesh (for tree layers)."""
        vertices = []
        
        # Base circle
        base_y = 0
        for i in range(segments):
            angle1 = 2 * np.pi * i / segments
            angle2 = 2 * np.pi * (i + 1) / segments
            
            x1 = radius * np.cos(angle1)
            z1 = radius * np.sin(angle1)
            x2 = radius * np.cos(angle2)
            z2 = radius * np.sin(angle2)
            
            # Base triangle
            normal = np.array([0, -1, 0])
            vertices.append([0, base_y, 0] + list(normal) + [0.5, 0.5])
            vertices.append([x1, base_y, z1] + list(normal) + [0.5 + 0.5*np.cos(angle1), 0.5 + 0.5*np.sin(angle1)])
            vertices.append([x2, base_y, z2] + list(normal) + [0.5 + 0.5*np.cos(angle2), 0.5 + 0.5*np.sin(angle2)])
        
        # Sides (from base to peak)
        peak_y = height
        for i in range(segments):
            angle1 = 2 * np.pi * i / segments
            angle2 = 2 * np.pi * (i + 1) / segments
            
            x1 = radius * np.cos(angle1)
            z1 = radius * np.sin(angle1)
            x2 = radius * np.cos(angle2)
            z2 = radius * np.sin(angle2)
            
            # Calculate normal for side face
            edge1 = np.array([x1, base_y, z1]) - np.array([0, peak_y, 0])
            edge2 = np.array([x2, base_y, z2]) - np.array([0, peak_y, 0])
            normal = np.cross(edge1, edge2)
            norm_len = np.linalg.norm(normal)
            if norm_len > 0:
                normal = normal / norm_len
            
            # Side triangle
            vertices.append([0, peak_y, 0] + list(normal) + [0.5, 1.0])
            vertices.append([x1, base_y, z1] + list(normal) + [i/segments, 0.0])
            vertices.append([x2, base_y, z2] + list(normal) + [(i+1)/segments, 0.0])
        
        return np.array([item for sublist in vertices for item in sublist], dtype=np.float32)
    
    def _create_sphere_mesh(self, radius, segments=8):
        """Create a simple sphere mesh (for ornaments)."""
        vertices = []
        
        for i in range(segments):
            for j in range(segments):
                lat1 = np.pi * i / segments
                lat2 = np.pi * (i + 1) / segments
                lon1 = 2 * np.pi * j / segments
                lon2 = 2 * np.pi * (j + 1) / segments
                
                # Four corners of quad
                x1 = radius * np.sin(lat1) * np.cos(lon1)
                y1 = radius * np.cos(lat1)
                z1 = radius * np.sin(lat1) * np.sin(lon1)
                
                x2 = radius * np.sin(lat1) * np.cos(lon2)
                y2 = radius * np.cos(lat1)
                z2 = radius * np.sin(lat1) * np.sin(lon2)
                
                x3 = radius * np.sin(lat2) * np.cos(lon1)
                y3 = radius * np.cos(lat2)
                z3 = radius * np.sin(lat2) * np.sin(lon1)
                
                x4 = radius * np.sin(lat2) * np.cos(lon2)
                y4 = radius * np.cos(lat2)
                z4 = radius * np.sin(lat2) * np.sin(lon2)
                
                # Normal is direction from center
                for x, y, z in [(x1, y1, z1), (x2, y2, z2), (x3, y3, z3)]:
                    norm = np.linalg.norm([x, y, z])
                    n_x, n_y, n_z = x/norm, y/norm, z/norm
                    vertices.extend([x, y, z, n_x, n_y, n_z, (lon1 + lon2) / (4 * np.pi), (lat1 + lat2) / (2 * np.pi)])
                
                for x, y, z in [(x2, y2, z2), (x3, y3, z3), (x4, y4, z4)]:
                    norm = np.linalg.norm([x, y, z])
                    n_x, n_y, n_z = x/norm, y/norm, z/norm
                    vertices.extend([x, y, z, n_x, n_y, n_z, (lon1 + lon2) / (4 * np.pi), (lat1 + lat2) / (2 * np.pi)])
        
        return np.array(vertices, dtype=np.float32)
    
    def _create_tree(self):
        """Create tree structure with cones and ornaments."""
        # Layer 1: Large bottom cone
        cone1_mesh = Mesh(self._create_cone_mesh(radius=0.6, height=0.8))
        self.tree_parts.append({
            'mesh': cone1_mesh,
            'position': (0, 0, 0),
            'color': (0.2, 0.7, 0.2)  # Green
        })
        
        # Layer 2: Medium middle cone
        cone2_mesh = Mesh(self._create_cone_mesh(radius=0.4, height=0.6))
        self.tree_parts.append({
            'mesh': cone2_mesh,
            'position': (0, 0.6, 0),
            'color': (0.15, 0.65, 0.15)  # Darker green
        })
        
        # Layer 3: Small top cone
        cone3_mesh = Mesh(self._create_cone_mesh(radius=0.25, height=0.4))
        self.tree_parts.append({
            'mesh': cone3_mesh,
            'position': (0, 1.1, 0),
            'color': (0.1, 0.6, 0.1)  # Even darker green
        })
        
        # Trunk
        trunk_vertices = []
        trunk_radius = 0.08
        trunk_height = 0.3
        segments = 6
        
        for i in range(segments):
            angle1 = 2 * np.pi * i / segments
            angle2 = 2 * np.pi * (i + 1) / segments
            
            x1 = trunk_radius * np.cos(angle1)
            z1 = trunk_radius * np.sin(angle1)
            x2 = trunk_radius * np.cos(angle2)
            z2 = trunk_radius * np.sin(angle2)
            
            # Side face
            normal = np.array([np.cos((angle1 + angle2) / 2), 0, np.sin((angle1 + angle2) / 2)])
            
            # Face 1
            trunk_vertices.extend([x1, 0, z1] + list(normal) + [i/segments, 0.0])
            trunk_vertices.extend([x1, trunk_height, z1] + list(normal) + [i/segments, 1.0])
            trunk_vertices.extend([x2, trunk_height, z2] + list(normal) + [(i+1)/segments, 1.0])
            
            # Face 2
            trunk_vertices.extend([x1, 0, z1] + list(normal) + [i/segments, 0.0])
            trunk_vertices.extend([x2, trunk_height, z2] + list(normal) + [(i+1)/segments, 1.0])
            trunk_vertices.extend([x2, 0, z2] + list(normal) + [(i+1)/segments, 0.0])
        
        trunk_mesh = Mesh(np.array(trunk_vertices, dtype=np.float32))
        self.tree_parts.append({
            'mesh': trunk_mesh,
            'position': (0, -0.3, 0),
            'color': (0.5, 0.3, 0.1)  # Brown
        })
    
    def draw(self, view, projection, light_pos, view_pos, position=(0, 0, 0)):
        """Draw the Christmas tree."""
        self.shader.use()
        self.shader.set_mat4("view", view)
        self.shader.set_mat4("projection", projection)
        self.shader.set_vec3("lightPos", light_pos)
        self.shader.set_vec3("viewPos", view_pos)
        self.shader.set_bool("useTexture", False)
        
        for part in self.tree_parts:
            # Create model matrix for this part
            part_pos = (
                position[0] + part['position'][0],
                position[1] + part['position'][1],
                position[2] + part['position'][2]
            )
            model = glm.translate(glm.mat4(1.0), glm.vec3(part_pos[0], part_pos[1], part_pos[2]))
            
            self.shader.set_mat4("model", model)
            self.shader.set_vec3("objectColor", part['color'])
            
            part['mesh'].draw(self.shader)
