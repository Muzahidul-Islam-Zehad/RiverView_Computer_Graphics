"""
Procedural moving clouds for the sky.
Features: Billboarded clouds that move across the sky, procedurally generated textures.
"""

import numpy as np
import glm
from OpenGL.GL import *
from rendering.mesh import Mesh
from core.texture import Texture
from PIL import Image
import math

def generate_cloud_texture():
    """Generate a procedural cloud texture using Perlin-like noise."""
    width, height = 256, 256
    data = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Create cloud-like noise pattern
    for y in range(height):
        for x in range(width):
            # Multiple layers of noise for natural cloud look
            noise = 0.0
            frequency = 1.0
            amplitude = 1.0
            max_amplitude = 0.0
            
            for i in range(4):
                # Sine-based pseudo-random noise
                nx = (x / width) * frequency
                ny = (y / height) * frequency
                
                noise_val = math.sin(nx * 12.9898 + ny * 78.233) * 43758.5453
                noise_val = noise_val - math.floor(noise_val)
                
                # Smooth interpolation
                noise_val = noise_val * noise_val * (3.0 - 2.0 * noise_val)
                
                noise += noise_val * amplitude
                max_amplitude += amplitude
                
                frequency *= 2.0
                amplitude *= 0.5
            
            noise = noise / max_amplitude
            
            # Convert to cloud color (white/light gray)
            intensity = int(255 * max(0, noise - 0.3))
            
            data[y, x] = [255, 255, 255, intensity]
    
    image = Image.fromarray(data, 'RGBA')
    return image

class Cloud:
    """A single cloud billboard."""
    
    _cloud_texture = None
    _cloud_mesh = None
    
    def __init__(self, position, scale=1.0, speed=0.5):
        """Initialize a cloud.
        
        Args:
            position: (x, y, z) initial position
            scale: Size of the cloud
            speed: Movement speed along X-axis
        """
        self.position = list(position)
        self.scale = scale
        self.speed = speed
        self.initial_x = position[0]
        
        # Load shared resources
        if Cloud._cloud_mesh is None:
            self._create_cloud_mesh()
    
    @classmethod
    def _load_texture_once(cls):
        """Load or generate cloud texture."""
        if cls._cloud_texture is not None:
            return
        
        try:
            # Load cloud.png from file
            cls._cloud_texture = Texture("assets/textures/cloud.png")
            print("✅ Cloud texture loaded from file")
        except Exception as e:
            print(f"Cloud file not found ({e}), generating procedurally...")
            # Generate procedurally as fallback
            try:
                img = generate_cloud_texture()
                img_data = img.tobytes()
                
                texture_id = glGenTextures(1)
                glBindTexture(GL_TEXTURE_2D, texture_id)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
                glGenerateMipmap(GL_TEXTURE_2D)
                
                # Create a temporary texture object
                class TempTexture:
                    def __init__(self, tid):
                        self.texture_id = tid
                
                cls._cloud_texture = TempTexture(texture_id)
                print("✅ Procedural cloud texture generated")
            except Exception as e:
                print(f"Failed to create cloud texture: {e}")
    
    @classmethod
    def _create_cloud_mesh(cls):
        """Create a 3D cloud mesh made of multiple cubes for volumetric appearance."""
        vertices = []
        
        # Create a cloud shape using multiple small cube positions
        # Arrange cubes in a cloud-like formation
        cloud_positions = [
            # Center cluster
            (0, 0, 0),
            (1, 0, 0), (-1, 0, 0),
            (0, 1, 0), (0, -1, 0),
            (0, 0, 1), (0, 0, -1),
            # Secondary positions for fuller look
            (1, 1, 0), (-1, 1, 0),
            (1, -1, 0), (-1, -1, 0),
            (1, 0, 1), (-1, 0, 1),
            (1, 0, -1), (-1, 0, -1),
        ]
        
        # Create vertices for each small cube in the formation
        for pos in cloud_positions:
            cx, cy, cz = pos[0] * 0.3, pos[1] * 0.3, pos[2] * 0.3
            
            # Cube vertices (scaled)
            cube_verts = [
                # Front face
                cx - 0.3, cy - 0.25, cz + 0.3,  0, 0, 1,  0, 0,
                cx + 0.3, cy - 0.25, cz + 0.3,  0, 0, 1,  1, 0,
                cx + 0.3, cy + 0.25, cz + 0.3,  0, 0, 1,  1, 1,
                cx - 0.3, cy - 0.25, cz + 0.3,  0, 0, 1,  0, 0,
                cx + 0.3, cy + 0.25, cz + 0.3,  0, 0, 1,  1, 1,
                cx - 0.3, cy + 0.25, cz + 0.3,  0, 0, 1,  0, 1,
                
                # Back face
                cx - 0.3, cy - 0.25, cz - 0.3,  0, 0, -1,  0, 0,
                cx - 0.3, cy + 0.25, cz - 0.3,  0, 0, -1,  1, 1,
                cx + 0.3, cy - 0.25, cz - 0.3,  0, 0, -1,  0, 0,
                cx + 0.3, cy - 0.25, cz - 0.3,  0, 0, -1,  0, 0,
                cx - 0.3, cy + 0.25, cz - 0.3,  0, 0, -1,  1, 1,
                cx + 0.3, cy + 0.25, cz - 0.3,  0, 0, -1,  1, 1,
                
                # Top face
                cx - 0.3, cy + 0.25, cz + 0.3,  0, 1, 0,  0, 1,
                cx + 0.3, cy + 0.25, cz + 0.3,  0, 1, 0,  1, 1,
                cx + 0.3, cy + 0.25, cz - 0.3,  0, 1, 0,  1, 0,
                cx - 0.3, cy + 0.25, cz + 0.3,  0, 1, 0,  0, 1,
                cx + 0.3, cy + 0.25, cz - 0.3,  0, 1, 0,  1, 0,
                cx - 0.3, cy + 0.25, cz - 0.3,  0, 1, 0,  0, 0,
                
                # Bottom face
                cx - 0.3, cy - 0.25, cz + 0.3,  0, -1, 0,  0, 0,
                cx + 0.3, cy - 0.25, cz - 0.3,  0, -1, 0,  1, 1,
                cx + 0.3, cy - 0.25, cz + 0.3,  0, -1, 0,  1, 0,
                cx - 0.3, cy - 0.25, cz + 0.3,  0, -1, 0,  0, 0,
                cx - 0.3, cy - 0.25, cz - 0.3,  0, -1, 0,  0, 1,
                cx + 0.3, cy - 0.25, cz - 0.3,  0, -1, 0,  1, 1,
                
                # Right face
                cx + 0.3, cy - 0.25, cz + 0.3,  1, 0, 0,  0, 0,
                cx + 0.3, cy - 0.25, cz - 0.3,  1, 0, 0,  1, 0,
                cx + 0.3, cy + 0.25, cz + 0.3,  1, 0, 0,  0, 1,
                cx + 0.3, cy + 0.25, cz + 0.3,  1, 0, 0,  0, 1,
                cx + 0.3, cy - 0.25, cz - 0.3,  1, 0, 0,  1, 0,
                cx + 0.3, cy + 0.25, cz - 0.3,  1, 0, 0,  1, 1,
                
                # Left face
                cx - 0.3, cy - 0.25, cz + 0.3,  -1, 0, 0,  1, 0,
                cx - 0.3, cy + 0.25, cz + 0.3,  -1, 0, 0,  1, 1,
                cx - 0.3, cy - 0.25, cz - 0.3,  -1, 0, 0,  0, 0,
                cx - 0.3, cy + 0.25, cz + 0.3,  -1, 0, 0,  1, 1,
                cx - 0.3, cy + 0.25, cz - 0.3,  -1, 0, 0,  0, 1,
                cx - 0.3, cy - 0.25, cz - 0.3,  -1, 0, 0,  0, 0,
            ]
            
            vertices.extend(cube_verts)
        
        cloud_vertices = np.array(vertices, dtype=np.float32)
        cls._cloud_mesh = Mesh(cloud_vertices)
        print("✅ 3D volumetric cloud mesh created")
    
    def update(self, delta_time):
        """Update cloud position."""
        self.position[0] += self.speed * delta_time
        
        # Wrap around - if goes off screen, reset to other side
        if self.position[0] > 30.0:
            self.position[0] = -30.0
        elif self.position[0] < -30.0:
            self.position[0] = 30.0
    
    def draw(self, shader, view, projection, light_pos, view_pos):
        """Render the 3D cloud."""
        if Cloud._cloud_mesh is None:
            return
        
        # Load texture if not done
        if Cloud._cloud_texture is None:
            self._load_texture_once()
        
        shader.use()
        shader.set_mat4("view", view)
        shader.set_mat4("projection", projection)
        shader.set_vec3("lightPos", light_pos)
        shader.set_vec3("viewPos", view_pos)
        shader.set_vec3("lightColor", (1.0, 1.0, 1.0))
        
        # Create model matrix - just position and scale (no billboard rotation)
        model = glm.translate(glm.mat4(1.0), glm.vec3(self.position[0], self.position[1], self.position[2]))
        model = glm.scale(model, glm.vec3(self.scale, self.scale * 0.7, self.scale * 0.8))  # Varied dimensions
        
        shader.set_mat4("model", model)
        shader.set_vec3("objectColor", (1.0, 1.0, 1.0))  # White
        shader.set_bool("useTexture", True)
        
        if Cloud._cloud_texture:
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, Cloud._cloud_texture.texture_id)
            shader.set_sampler("texture1", 0)
            
            # Enable additive blending to ignore black background
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_COLOR, GL_ONE)  # Additive blend: ignore black, show white/colors
        
        Cloud._cloud_mesh.draw(shader)
        
        shader.set_bool("useTexture", False)
        # Reset blend function
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


class CloudSystem:
    """Manages multiple clouds for the sky."""
    
    def __init__(self, shader, num_clouds=8):
        """Initialize cloud system.
        
        Args:
            shader: OpenGL shader program
            num_clouds: Number of clouds to generate
        """
        self.shader = shader
        self.clouds = []
        
        # Create clouds at random positions in the sky
        np.random.seed(42)  # For reproducibility
        
        for i in range(num_clouds):
            # Random position in sky
            x = np.random.uniform(-25.0, 25.0)
            y = np.random.uniform(12.0, 18.0)  # High in the sky
            z = np.random.uniform(-15.0, 10.0)  # Various depths
            
            # Random size - smaller clouds
            scale = np.random.uniform(1.0, 2.5)
            
            # Random speed - slower movement
            speed = np.random.uniform(0.5, 1.5)
            
            cloud = Cloud(
                position=(x, y, z),
                scale=scale,
                speed=speed
            )
            self.clouds.append(cloud)
        
        print(f"✅ CloudSystem created with {num_clouds} clouds")
    
    def update(self, delta_time):
        """Update all clouds."""
        for cloud in self.clouds:
            cloud.update(delta_time)
    
    def draw(self, view, projection, light_pos, view_pos):
        """Render all clouds."""
        for cloud in self.clouds:
            cloud.draw(self.shader, view, projection, light_pos, view_pos)
