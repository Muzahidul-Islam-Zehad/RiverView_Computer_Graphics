"""
Advanced house class with walls, door, and windows (roof is separate).
"""

import numpy as np
from rendering.mesh import Mesh
from objects.primitives import create_cube_with_uv
from utils.transformations import create_model_matrix
from core.texture import Texture

class AdvancedHouse:
    def __init__(self, shader):
        self.shader = shader
        self.cube_mesh = Mesh(create_cube_with_uv())
        self.house_texture = None
        self.door_texture = None
        self.window_texture = None
        self.chimney_texture = None
        
        self._load_textures()
    
    def _load_textures(self):
        """Load house textures."""
        try:
            self.house_texture = Texture("assets/textures/houseWall.png")
            print(f"✅ House texture loaded: {self.house_texture.texture_id}")
        except Exception as e:
            print(f"House texture not found: {e}")
        
        try:
            self.door_texture = Texture("assets/textures/houseDoor.png")
            print(f"✅ Door texture loaded: {self.door_texture.texture_id}")
        except Exception as e:
            print(f"Door texture not found: {e}")
        
        try:
            self.window_texture = Texture("assets/textures/houseWindow.png")
            print(f"✅ Window texture loaded: {self.window_texture.texture_id}")
        except Exception as e:
            print(f"Window texture not found: {e}")
        
        try:
            self.chimney_texture = Texture("assets/textures/column.png")
            print(f"✅ Chimney texture loaded: {self.chimney_texture.texture_id}")
        except Exception as e:
            print(f"Chimney texture not found: {e}")
    
    
    def _draw_cube(self, position, scale, color, texture=None):
        """Helper to draw a textured cube."""
        model = create_model_matrix(position=position, scale=scale)
        self.shader.set_mat4("model", model)
        self.shader.set_vec3("objectColor", color)
        
        if texture:
            texture.bind(0)
            self.shader.set_sampler("texture_diffuse1", 0)
            self.shader.set_bool("useTexture", True)
        else:
            self.shader.set_bool("useTexture", False)
        
        self.cube_mesh.draw(self.shader)
        self.shader.set_bool("useTexture", False)
    
    def _draw_cube_rotated(self, position, scale, color, texture, rotation_angle, center):
        """Helper to draw a rotated textured cube around a center point."""
        import glm
        
        # Translate to center, rotate, translate back
        center_pos = glm.vec3(center[0], center[1], center[2])
        local_pos = glm.vec3(position[0] - center[0], position[1] - center[1], position[2] - center[2])
        
        # Create model matrix with rotation
        model = glm.translate(glm.mat4(1.0), glm.vec3(center[0], center[1], center[2]))
        model = glm.rotate(model, rotation_angle, glm.vec3(0, 1, 0))
        model = glm.translate(model, local_pos)
        model = glm.scale(model, glm.vec3(scale[0], scale[1], scale[2]))
        
        self.shader.set_mat4("model", model)
        self.shader.set_vec3("objectColor", color)
        
        if texture:
            texture.bind(0)
            self.shader.set_sampler("texture_diffuse1", 0)
            self.shader.set_bool("useTexture", True)
        else:
            self.shader.set_bool("useTexture", False)
        
        self.cube_mesh.draw(self.shader)
        self.shader.set_bool("useTexture", False)
    
    def draw(self, view, projection, light_pos, view_pos, position=(0, 0, 0)):
        """Draw an advanced house with multiple components."""
        self.shader.use()
        self.shader.set_mat4("view", view)
        self.shader.set_mat4("projection", projection)
        self.shader.set_vec3("lightPos", light_pos)
        self.shader.set_vec3("viewPos", view_pos)
        self.shader.set_vec3("lightColor", (1.0, 1.0, 1.0))
        
        house_x, house_y, house_z = position
        
        # Rotation: 270 degrees around Y axis (180 + 90)
        import math
        rotation_angle = math.pi * 1.5  # 270 degrees
        
        # ===== MAIN WALLS =====
        wall_color = (0.8, 0.7, 0.6)
        wall_height = 0.8
        wall_width = 1.2
        wall_depth = 1.0
        
        # Front wall (now facing road - rotated)
        self._draw_cube_rotated(
            (house_x, house_y + wall_height/2, house_z + wall_depth/2),
            (wall_width, wall_height, 0.08),
            wall_color,
            self.house_texture,
            rotation_angle,
            (house_x, house_y, house_z)
        )
        
        # Back wall (rotated)
        self._draw_cube_rotated(
            (house_x, house_y + wall_height/2, house_z - wall_depth/2),
            (wall_width, wall_height, 0.08),
            wall_color,
            self.house_texture,
            rotation_angle,
            (house_x, house_y, house_z)
        )
        
        # Left wall (rotated)
        self._draw_cube_rotated(
            (house_x - wall_width/2, house_y + wall_height/2, house_z),
            (0.08, wall_height, wall_depth),
            wall_color,
            self.house_texture,
            rotation_angle,
            (house_x, house_y, house_z)
        )
        
        # Right wall (rotated)
        self._draw_cube_rotated(
            (house_x + wall_width/2, house_y + wall_height/2, house_z),
            (0.08, wall_height, wall_depth),
            wall_color,
            self.house_texture,
            rotation_angle,
            (house_x, house_y, house_z)
        )
        
        # ===== DOOR (now facing road) =====
        door_color = (0.3, 0.15, 0.05)
        door_width = 0.25
        door_height = 0.5
        
        self._draw_cube_rotated(
            (house_x, house_y + door_height/2, house_z + wall_depth/2 + 0.04),
            (door_width, door_height, 0.05),
            door_color,
            self.door_texture,
            rotation_angle,
            (house_x, house_y, house_z)
        )
        
        # ===== WINDOWS =====
        window_color = (0.5, 0.8, 1.0)
        window_size = 0.2
        
        # Front left window (rotated)
        self._draw_cube_rotated(
            (house_x - 0.35, house_y + 0.5, house_z + wall_depth/2 + 0.04),
            (window_size, window_size, 0.03),
            window_color,
            self.window_texture,
            rotation_angle,
            (house_x, house_y, house_z)
        )
        
        # Front right window (rotated)
        self._draw_cube_rotated(
            (house_x + 0.35, house_y + 0.5, house_z + wall_depth/2 + 0.04),
            (window_size, window_size, 0.03),
            window_color,
            self.window_texture,
            rotation_angle,
            (house_x, house_y, house_z)
        )
        
        # Back left window (rotated)
        self._draw_cube_rotated(
            (house_x - 0.35, house_y + 0.5, house_z - wall_depth/2 - 0.04),
            (window_size, window_size, 0.03),
            window_color,
            self.window_texture,
            rotation_angle,
            (house_x, house_y, house_z)
        )
        
        # Back right window (rotated)
        self._draw_cube_rotated(
            (house_x + 0.35, house_y + 0.5, house_z - wall_depth/2 - 0.04),
            (window_size, window_size, 0.03),
            window_color,
            self.window_texture,
            rotation_angle,
            (house_x, house_y, house_z)
        )
        
        # ===== CHIMNEY =====
        chimney_color = (0.8, 0.8, 0.8)
        roof_y = house_y + wall_height
        roof_height = 0.5
        self._draw_cube_rotated(
            (house_x + wall_width/2 - 0.15, roof_y + roof_height/2 + 0.25, house_z - 0.15),
            (0.1, 0.4, 0.1),
            chimney_color,
            self.chimney_texture,
            rotation_angle,
            (house_x, house_y, house_z)
        )