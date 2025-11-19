"""
Advanced tree generation with procedural trunks and branching foliage.
"""

import numpy as np
import math
import random
from rendering.mesh import Mesh
from core.texture import Texture
from utils.transformations import create_model_matrix


class AdvancedTree:
    """Procedurally generated tree with trunk branches and complex foliage."""
    
    def __init__(self, shader, position=(0, 0, 0), height=3.0, seed=42):
        self.shader = shader
        self.position = position
        self.height = height
        self.seed = seed
        self.leaf_texture = None
        
        random.seed(seed)
        np.random.seed(seed)
        
        # Load leaf texture (optional)
        try:
            self.leaf_texture = Texture("assets/textures/leafs.png")
            print("✅ Leaf texture loaded")
        except:
            self.leaf_texture = None
        
        self._generate_tree()
    
    def _generate_trunk(self):
        """Generate trunk with branches."""
        vertices = []
        segments = 12
        trunk_levels = 4
        
        for level in range(trunk_levels):
            t = level / max(1, trunk_levels - 1)
            radius = self.height * 0.15 * (1 - t * 0.7)  # Taper towards top
            z_pos = self.height * t
            
            for seg in range(segments):
                angle = (seg / segments) * 2 * math.pi
                x = radius * math.cos(angle)
                y = radius * math.sin(angle)
                
                # Add slight waviness for organic look
                wave = math.sin(angle * 3) * radius * 0.2
                x_wave = x + wave * math.cos(z_pos)
                
                if level < trunk_levels - 1:
                    next_level = level + 1
                    t_next = next_level / max(1, trunk_levels - 1)
                    radius_next = self.height * 0.15 * (1 - t_next * 0.7)
                    z_pos_next = self.height * t_next
                    
                    angle_next = ((seg + 1) % segments) / segments * 2 * math.pi
                    x_next = radius_next * math.cos(angle_next)
                    y_next = radius_next * math.sin(angle_next)
                    wave_next = math.sin(angle_next * 3) * radius_next * 0.2
                    x_wave_next = x_next + wave_next * math.cos(z_pos_next)
                    
                    # Normal pointing outward
                    normal = [math.cos(angle), math.sin(angle), 0.0]
                    
                    # Triangle 1
                    vertices.extend([x_wave, y, z_pos, normal[0], normal[1], normal[2], (seg/segments), (level/trunk_levels)])
                    vertices.extend([x_wave_next, y_next, z_pos_next, normal[0], normal[1], normal[2], ((seg+1)/segments), ((level+1)/trunk_levels)])
                    vertices.extend([x_next, y_next, z_pos_next, normal[0], normal[1], normal[2], ((seg+1)/segments), ((level+1)/trunk_levels)])
                    
                    # Triangle 2
                    vertices.extend([x_wave, y, z_pos, normal[0], normal[1], normal[2], (seg/segments), (level/trunk_levels)])
                    vertices.extend([x, y, z_pos, normal[0], normal[1], normal[2], (seg/segments), (level/trunk_levels)])
                    vertices.extend([x_next, y_next, z_pos_next, normal[0], normal[1], normal[2], ((seg+1)/segments), ((level+1)/trunk_levels)])
        
        return vertices
    
    def _generate_foliage(self):
        """Generate complex foliage clusters."""
        vertices = []
        foliage_clusters = 5
        
        # Main foliage starts at top 40% of tree
        foliage_start = self.height * 0.6
        
        for cluster_idx in range(foliage_clusters):
            # Position along trunk
            cluster_z = foliage_start + (cluster_idx / foliage_clusters) * (self.height * 0.3)
            
            # Multiple sphere-like clusters
            num_spheres = 3 + cluster_idx
            for sphere_idx in range(num_spheres):
                # Random offset from trunk
                angle = random.random() * 2 * math.pi
                distance = (0.15 + random.random() * 0.25) * self.height
                
                sphere_x = math.cos(angle) * distance
                sphere_z = math.sin(angle) * distance
                sphere_center_y = cluster_z + random.random() * (self.height * 0.15)
                
                # Foliage sphere radius - REDUCED
                sphere_radius = self.height * (0.12 + random.random() * 0.08)
                
                # Generate sphere vertices
                lat_segments = 8
                lon_segments = 8
                
                for lat in range(lat_segments):
                    lat_ratio = lat / lat_segments
                    lat_angle = lat_ratio * math.pi
                    sin_lat = math.sin(lat_angle)
                    cos_lat = math.cos(lat_angle)
                    
                    for lon in range(lon_segments):
                        lon_ratio = lon / lon_segments
                        lon_angle = lon_ratio * 2 * math.pi
                        sin_lon = math.sin(lon_angle)
                        cos_lon = math.cos(lon_angle)
                        
                        # Sphere vertex
                        x = sphere_x + sphere_radius * sin_lat * cos_lon
                        y = sphere_center_y + sphere_radius * cos_lat
                        z = sphere_z + sphere_radius * sin_lat * sin_lon
                        
                        # Normal
                        nx = sin_lat * cos_lon
                        ny = cos_lat
                        nz = sin_lat * sin_lon
                        
                        # Add variation
                        if lat < lat_segments - 1:
                            lon_next = (lon + 1) % lon_segments
                            lon_angle_next = lon_next / lon_segments * 2 * math.pi
                            sin_lon_next = math.sin(lon_angle_next)
                            cos_lon_next = math.cos(lon_angle_next)
                            
                            x_next = sphere_x + sphere_radius * sin_lat * cos_lon_next
                            z_next = sphere_z + sphere_radius * sin_lat * sin_lon_next
                            
                            # Triangle 1
                            vertices.extend([x, y, z, nx, ny, nz, lon_ratio, lat_ratio])
                            vertices.extend([x_next, y, z_next, nx, ny, nz, lon_next/lon_segments, lat_ratio])
                            
                            lat_next = lat + 1
                            lat_angle_next = (lat_next / lat_segments) * math.pi
                            sin_lat_next = math.sin(lat_angle_next)
                            cos_lat_next = math.cos(lat_angle_next)
                            
                            x_next_lat = sphere_x + sphere_radius * sin_lat_next * cos_lon
                            y_next_lat = sphere_center_y + sphere_radius * cos_lat_next
                            z_next_lat = sphere_z + sphere_radius * sin_lat_next * sin_lon
                            
                            nx_next = sin_lat_next * cos_lon
                            ny_next = cos_lat_next
                            nz_next = sin_lat_next * sin_lon
                            
                            vertices.extend([x_next_lat, y_next_lat, z_next_lat, nx_next, ny_next, nz_next, lon_ratio, lat_next/lat_segments])
        
        return vertices
    
    def _generate_tree(self):
        """Generate complete tree geometry."""
        print("Building advanced tree...")
        
        # Generate foliage only (no trunk)
        foliage_vertices = self._generate_foliage()
        
        # Create mesh for foliage only with texture
        if foliage_vertices:
            self.foliage_mesh = Mesh(np.array(foliage_vertices, dtype=np.float32), texture=self.leaf_texture)
        else:
            self.foliage_mesh = None
        
        self.trunk_mesh = None  # No trunk mesh
        
        print("✅ Advanced tree generated!")
    
    def draw(self, view, projection, light_pos, view_pos):
        """Draw the tree."""
        self.shader.use()
        self.shader.set_mat4("view", view)
        self.shader.set_mat4("projection", projection)
        self.shader.set_vec3("lightPos", light_pos)
        self.shader.set_vec3("viewPos", view_pos)
        self.shader.set_vec3("lightColor", (1.0, 1.0, 1.0))
        
        model = create_model_matrix(position=self.position)
        self.shader.set_mat4("model", model)
        
        # Draw foliage only
        if self.foliage_mesh:
            self.shader.set_vec3("objectColor", (0.2, 0.5, 0.1))  # Green leaves
            self.shader.set_bool("useTexture", self.leaf_texture is not None)
            self.foliage_mesh.draw(self.shader)
