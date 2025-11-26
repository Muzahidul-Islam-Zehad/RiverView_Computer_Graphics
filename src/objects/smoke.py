"""
Smoke particle system coming from the house chimney.
Features: Animated particles that rise and fade, procedurally generated smoke texture.
"""

import numpy as np
import glm
from OpenGL.GL import *
from rendering.mesh import Mesh
from core.texture import Texture
from PIL import Image
import math

def generate_smoke_texture():
    """Generate a procedural smoke texture with alpha channel."""
    width, height = 128, 128
    data = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Create smoke-like radial gradient
    center_x, center_y = width / 2, height / 2
    max_dist = math.sqrt((width/2)**2 + (height/2)**2)
    
    for y in range(height):
        for x in range(width):
            # Distance from center
            dx = x - center_x
            dy = y - center_y
            dist = math.sqrt(dx*dx + dy*dy)
            
            # Create radial falloff for smoke puff
            falloff = max(0, 1.0 - (dist / max_dist))
            
            # Add some noise variation
            noise = math.sin(x * 0.1) * math.cos(y * 0.1) * 0.3 + 0.7
            
            # Smoke color (light gray/white)
            intensity = int(200 * falloff * noise)
            alpha = int(255 * falloff * falloff)  # Quadratic falloff for alpha
            
            data[y, x] = [220, 220, 220, alpha]
    
    image = Image.fromarray(data, 'RGBA')
    return image

class SmokeParticle:
    """A single smoke particle."""
    
    def __init__(self, position, velocity, lifetime=3.0):
        """Initialize a smoke particle.
        
        Args:
            position: (x, y, z) starting position
            velocity: (vx, vy, vz) velocity vector
            lifetime: How long the particle lives
        """
        self.position = np.array(position, dtype=np.float32)
        self.velocity = np.array(velocity, dtype=np.float32)
        self.lifetime = lifetime
        self.age = 0.0
        self.scale = 0.15  # Smaller starting size
    
    def update(self, delta_time):
        """Update particle position and age."""
        self.age += delta_time
        
        # Update position
        self.position += self.velocity * delta_time
        
        # Apply gravity (slight upward drift for smoke)
        self.velocity[1] += 0.5 * delta_time  # Upward acceleration
        
        # Air resistance (fade velocity)
        self.velocity *= 0.95
        
        # Grow slightly as it rises
        self.scale += 0.1 * delta_time
        
        return self.age < self.lifetime
    
    def get_alpha(self):
        """Get alpha value based on age (fade out)."""
        progress = self.age / self.lifetime
        # Fade in quickly, then fade out
        if progress < 0.1:
            return progress * 10.0  # Fade in over 10% of lifetime
        else:
            return max(0, 1.0 - (progress - 0.1) / 0.9)  # Fade out over 90%

class SmokeSystem:
    """Manages smoke particles from chimney."""
    
    _smoke_texture = None
    _smoke_mesh = None
    
    def __init__(self, shader, chimney_position=(5.0, 1.8, 0.0)):
        """Initialize smoke system.
        
        Args:
            shader: OpenGL shader program
            chimney_position: Position of the chimney top
        """
        self.shader = shader
        self.chimney_position = np.array(chimney_position, dtype=np.float32)
        self.particles = []
        self.emission_rate = 8  # Fewer particles per second (was 15)
        self.accumulator = 0.0
        
        # Load shared resources
        if SmokeSystem._smoke_mesh is None:
            self._create_smoke_mesh()
        if SmokeSystem._smoke_texture is None:
            self._load_texture_once()
        
        print("✅ SmokeSystem created")
    
    @classmethod
    def _load_texture_once(cls):
        """Load cloud.png texture for smoke."""
        try:
            # Load cloud.png from file for smoke texture
            cls._smoke_texture = Texture("assets/textures/cloud.png")
            print("✅ Smoke texture loaded from cloud.png")
        except Exception as e:
            print(f"Failed to load cloud.png for smoke ({e}), generating procedurally...")
            # Generate procedurally as fallback
            try:
                img = generate_smoke_texture()
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
                
                cls._smoke_texture = TempTexture(texture_id)
                print("✅ Smoke texture generated procedurally")
            except Exception as e:
                print(f"Failed to create smoke texture: {e}")
    
    @classmethod
    def _create_smoke_mesh(cls):
        """Create a small cube mesh for smoke particles."""
        # Small cube with 6 faces
        vertices = [
            # Front face
            -0.5, -0.5,  0.5,  0, 0, 1,  0, 0,
             0.5, -0.5,  0.5,  0, 0, 1,  1, 0,
             0.5,  0.5,  0.5,  0, 0, 1,  1, 1,
            -0.5, -0.5,  0.5,  0, 0, 1,  0, 0,
             0.5,  0.5,  0.5,  0, 0, 1,  1, 1,
            -0.5,  0.5,  0.5,  0, 0, 1,  0, 1,
            
            # Back face
            -0.5, -0.5, -0.5,  0, 0, -1,  0, 0,
            -0.5,  0.5, -0.5,  0, 0, -1,  1, 1,
             0.5, -0.5, -0.5,  0, 0, -1,  0, 0,
             0.5, -0.5, -0.5,  0, 0, -1,  0, 0,
            -0.5,  0.5, -0.5,  0, 0, -1,  1, 1,
             0.5,  0.5, -0.5,  0, 0, -1,  1, 1,
            
            # Top face
            -0.5,  0.5,  0.5,  0, 1, 0,  0, 1,
             0.5,  0.5,  0.5,  0, 1, 0,  1, 1,
             0.5,  0.5, -0.5,  0, 1, 0,  1, 0,
            -0.5,  0.5,  0.5,  0, 1, 0,  0, 1,
             0.5,  0.5, -0.5,  0, 1, 0,  1, 0,
            -0.5,  0.5, -0.5,  0, 1, 0,  0, 0,
            
            # Bottom face
            -0.5, -0.5,  0.5,  0, -1, 0,  0, 0,
             0.5, -0.5, -0.5,  0, -1, 0,  1, 1,
             0.5, -0.5,  0.5,  0, -1, 0,  1, 0,
            -0.5, -0.5,  0.5,  0, -1, 0,  0, 0,
            -0.5, -0.5, -0.5,  0, -1, 0,  0, 1,
             0.5, -0.5, -0.5,  0, -1, 0,  1, 1,
            
            # Right face
             0.5, -0.5,  0.5,  1, 0, 0,  0, 0,
             0.5, -0.5, -0.5,  1, 0, 0,  1, 0,
             0.5,  0.5,  0.5,  1, 0, 0,  0, 1,
             0.5,  0.5,  0.5,  1, 0, 0,  0, 1,
             0.5, -0.5, -0.5,  1, 0, 0,  1, 0,
             0.5,  0.5, -0.5,  1, 0, 0,  1, 1,
            
            # Left face
            -0.5, -0.5,  0.5,  -1, 0, 0,  1, 0,
            -0.5,  0.5,  0.5,  -1, 0, 0,  1, 1,
            -0.5, -0.5, -0.5,  -1, 0, 0,  0, 0,
            -0.5,  0.5,  0.5,  -1, 0, 0,  1, 1,
            -0.5,  0.5, -0.5,  -1, 0, 0,  0, 1,
            -0.5, -0.5, -0.5,  -1, 0, 0,  0, 0,
        ]
        
        smoke_vertices = np.array(vertices, dtype=np.float32)
        cls._smoke_mesh = Mesh(smoke_vertices)
        print("✅ Smoke cube mesh created")
    
    def emit_particles(self, delta_time):
        """Emit new particles from chimney."""
        self.accumulator += delta_time
        
        num_to_emit = int(self.accumulator * self.emission_rate)
        self.accumulator -= num_to_emit / self.emission_rate
        
        for _ in range(num_to_emit):
            # Random spread around chimney
            spread = 0.15  # Smaller spread
            x_offset = np.random.uniform(-spread, spread)
            z_offset = np.random.uniform(-spread, spread)
            
            position = self.chimney_position + np.array([x_offset, 0.0, z_offset])
            
            # Random upward velocity with slight horizontal drift
            velocity = np.array([
                np.random.uniform(-0.3, 0.3),
                np.random.uniform(1.2, 1.8),  # Upward
                np.random.uniform(-0.3, 0.3)
            ], dtype=np.float32)
            
            particle = SmokeParticle(position, velocity, lifetime=2.5)
            self.particles.append(particle)
            
            # Particle cap: prevent excessive particle count (performance safeguard)
            if len(self.particles) > 100:
                self.particles.pop(0)  # Remove oldest particle
    
    def update(self, delta_time):
        """Update all smoke particles."""
        self.emit_particles(delta_time)
        
        # Update and remove dead particles
        self.particles = [p for p in self.particles if p.update(delta_time)]
    
    def draw(self, view, projection, light_pos, view_pos):
        """Render all smoke particles with optimized batching."""
        if not self.particles or SmokeSystem._smoke_mesh is None or SmokeSystem._smoke_texture is None:
            return
        
        self.shader.use()
        self.shader.set_mat4("view", view)
        self.shader.set_mat4("projection", projection)
        self.shader.set_vec3("lightPos", light_pos)
        self.shader.set_vec3("viewPos", view_pos)
        self.shader.set_vec3("lightColor", (1.0, 1.0, 1.0))
        
        # Enable blending with additive mode to hide black background from cloud.png
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_COLOR, GL_ONE)  # Additive blend: ignore black, show white/colors
        
        # Bind texture ONCE for all particles (major optimization)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, SmokeSystem._smoke_texture.texture_id)
        self.shader.set_sampler("texture1", 0)
        self.shader.set_bool("useTexture", True)
        self.shader.set_vec3("objectColor", (1.0, 1.0, 1.0))  # White to blend with cloud texture
        
        # Draw each particle
        for particle in self.particles:
            # Get alpha for fade out effect
            alpha = particle.get_alpha()
            
            # Create model matrix for cube particle
            model = glm.translate(glm.mat4(1.0), glm.vec3(
                particle.position[0],
                particle.position[1],
                particle.position[2]
            ))
            model = glm.scale(model, glm.vec3(
                particle.scale,
                particle.scale,
                particle.scale
            ))
            
            self.shader.set_mat4("model", model)
            self.shader.set_float("alpha_override", alpha)  # Pass alpha to shader
            
            SmokeSystem._smoke_mesh.draw(self.shader)
        
        # Reset blend function to standard alpha blending
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.shader.set_float("alpha_override", 1.0)
