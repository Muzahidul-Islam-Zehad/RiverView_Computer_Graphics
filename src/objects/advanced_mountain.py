"""
Advanced mountain generation using pure Python noise functions.
"""

import numpy as np
import math
import random
from rendering.mesh import Mesh
from core.texture import Texture
from utils.transformations import create_model_matrix


class AdvancedMountain:
    def __init__(self, shader, position=(0, 0, 0), size=12.0, max_height=8.0, seed=42):
        self.shader = shader
        self.position = position
        self.size = size
        self.max_height = max_height
        self.seed = seed
        self.texture = None
        
        random.seed(seed)
        np.random.seed(seed)
        
        # Load hill texture
        try:
            self.texture = Texture("assets/textures/hill_texture.png")
            print("✅ Hill texture loaded")
        except:
            print("⚠️  Hill texture not found, using fallback color")
            self.texture = None
        
        self._generate_advanced_mountain()
    
    def _generate_heightmap(self, width, depth):
        """Generate mountain heightmap using simple noise."""
        heightmap = np.zeros((width, depth), dtype=np.float32)
        
        # Multiple peaks
        peaks = [
            (0.0, 0.0, 1.0, 2.5),
            (-0.3, -0.2, 0.8, 2.0),
            (0.25, -0.3, 0.7, 3.0),
        ]
        
        for i in range(width):
            for j in range(depth):
                x = (i / (width - 1) - 0.5) * 2.0
                z = (j / (depth - 1) - 0.5) * 2.0
                
                height = 0.0
                
                # Peak heights
                for peak_x, peak_z, strength, sharpness in peaks:
                    dx = x - peak_x
                    dz = z - peak_z
                    distance = math.sqrt(dx*dx + dz*dz)
                    peak_height = max(0, 1.0 - distance * 1.5) ** sharpness
                    height += peak_height * strength
                
                # Simple noise for texture
                noise = math.sin(x * 5.0) * math.cos(z * 5.0) * 0.1
                height += max(0, noise)
                
                heightmap[i][j] = height * self.max_height
        
        return heightmap
    
    def _generate_advanced_mountain(self):
        """Generate the mountain mesh."""
        print("Building advanced mountain...")
        width, depth = 40, 40
        
        heightmap = self._generate_heightmap(width, depth)
        
        vertices = []
        
        # Generate mesh from heightmap
        for i in range(depth - 1):
            for j in range(width - 1):
                h00 = heightmap[j][i]
                h10 = heightmap[j + 1][i]
                h11 = heightmap[j + 1][i + 1]
                h01 = heightmap[j][i + 1]
                
                x00 = (j / (width - 1) - 0.5) * self.size
                z00 = (i / (depth - 1) - 0.5) * self.size
                x10 = ((j + 1) / (width - 1) - 0.5) * self.size
                z10 = ((i + 1) / (depth - 1) - 0.5) * self.size
                
                # Simple normal
                normal = [0.0, 1.0, 0.0]
                
                # Triangle 1
                vertices.extend([x00, h00, z00, normal[0], normal[1], normal[2], j/width, i/depth])
                vertices.extend([x10, h10, z00, normal[0], normal[1], normal[2], (j+1)/width, i/depth])
                vertices.extend([x10, h11, z10, normal[0], normal[1], normal[2], (j+1)/width, (i+1)/depth])
                
                # Triangle 2
                vertices.extend([x00, h00, z00, normal[0], normal[1], normal[2], j/width, i/depth])
                vertices.extend([x10, h11, z10, normal[0], normal[1], normal[2], (j+1)/width, (i+1)/depth])
                vertices.extend([x00, h01, z10, normal[0], normal[1], normal[2], j/width, (i+1)/depth])
        
        self.mountain_mesh = Mesh(np.array(vertices, dtype=np.float32), texture=self.texture)
        print("✅ Advanced mountain generated!")
    
    def draw(self, view, projection, light_pos, view_pos):
        """Draw the mountain."""
        self.shader.use()
        self.shader.set_mat4("view", view)
        self.shader.set_mat4("projection", projection)
        self.shader.set_vec3("lightPos", light_pos)
        self.shader.set_vec3("viewPos", view_pos)
        self.shader.set_vec3("lightColor", (1.0, 1.0, 1.0))
        
        model = create_model_matrix(position=self.position)
        self.shader.set_mat4("model", model)
        self.shader.set_vec3("objectColor", (0.6, 0.5, 0.3))
        self.shader.set_bool("useTexture", self.texture is not None)
        
        self.mountain_mesh.draw(self.shader)