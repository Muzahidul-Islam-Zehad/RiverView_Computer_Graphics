"""
Advanced procedural car model with metallic texture and smooth curves.
Integrates into the RiverView graphics simulation.

Key Features:
- Procedural sedan mesh with 8 cross-sections creating smooth curves
- 32-segment wheels with realistic tread pattern
- Procedurally generated metallic red texture using Pillow
- Phong lighting model with specular highlights
- Smooth lofting between cross-sections for aerodynamic appearance
"""

from OpenGL.GL import *
import numpy as np
import glm
import math
import ctypes
from rendering.mesh import Mesh
from core.texture import Texture

# ==========================================
# GEOMETRY GENERATION
# ==========================================

def create_wheel_mesh(radius=0.0875, width=0.0625, segments=24):
    """Generates vertices for a cylinder wheel with proper triangle connectivity."""
    vertices = []
    
    # Create a cylinder oriented along the X-axis (width direction)
    # Left cap (x = -width/2)
    for i in range(segments):
        angle1 = 2.0 * math.pi * i / segments
        angle2 = 2.0 * math.pi * (i + 1) / segments
        
        y1, z1 = radius * math.cos(angle1), radius * math.sin(angle1)
        y2, z2 = radius * math.cos(angle2), radius * math.sin(angle2)
        
        # Center, point1, point2
        vertices.extend([-width/2, 0.0, 0.0, -1, 0, 0, 0.5, 0.5])
        vertices.extend([-width/2, y1, z1, -1, 0, 0, 0.5 + 0.5*math.cos(angle1), 0.5 + 0.5*math.sin(angle1)])
        vertices.extend([-width/2, y2, z2, -1, 0, 0, 0.5 + 0.5*math.cos(angle2), 0.5 + 0.5*math.sin(angle2)])
    
    # Right cap (x = +width/2)
    for i in range(segments):
        angle1 = 2.0 * math.pi * i / segments
        angle2 = 2.0 * math.pi * (i + 1) / segments
        
        y1, z1 = radius * math.cos(angle1), radius * math.sin(angle1)
        y2, z2 = radius * math.cos(angle2), radius * math.sin(angle2)
        
        # Center, point2, point1 (reversed for outward normal)
        vertices.extend([width/2, 0.0, 0.0, 1, 0, 0, 0.5, 0.5])
        vertices.extend([width/2, y2, z2, 1, 0, 0, 0.5 + 0.5*math.cos(angle2), 0.5 + 0.5*math.sin(angle2)])
        vertices.extend([width/2, y1, z1, 1, 0, 0, 0.5 + 0.5*math.cos(angle1), 0.5 + 0.5*math.sin(angle1)])
    
    # Tread (cylindrical surface)
    for i in range(segments):
        angle1 = 2.0 * math.pi * i / segments
        angle2 = 2.0 * math.pi * (i + 1) / segments
        
        y1, z1 = radius * math.cos(angle1), radius * math.sin(angle1)
        y2, z2 = radius * math.cos(angle2), radius * math.sin(angle2)
        
        # Normal pointing outward
        norm_y1 = math.cos(angle1)
        norm_z1 = math.sin(angle1)
        norm_y2 = math.cos(angle2)
        norm_z2 = math.sin(angle2)
        
        # First triangle
        vertices.extend([-width/2, y1, z1, 0, norm_y1, norm_z1, float(i)/segments, 0.0])
        vertices.extend([width/2, y1, z1, 0, norm_y1, norm_z1, float(i)/segments, 1.0])
        vertices.extend([-width/2, y2, z2, 0, norm_y2, norm_z2, float(i+1)/segments, 0.0])
        
        # Second triangle
        vertices.extend([width/2, y1, z1, 0, norm_y1, norm_z1, float(i)/segments, 1.0])
        vertices.extend([width/2, y2, z2, 0, norm_y2, norm_z2, float(i+1)/segments, 1.0])
        vertices.extend([-width/2, y2, z2, 0, norm_y2, norm_z2, float(i+1)/segments, 0.0])
    
    return np.array(vertices, dtype=np.float32)

def create_sedan_mesh():
    """
    Procedurally creates a sedan shape by connecting cross-sections along the Z-axis.
    This creates a smooth, continuous mesh rather than disjointed cubes.
    """
    vertices = []

    # Define the cross-sections of the car from Front to Back (Z-axis)
    # Each section is defined by 4 points (Clockwise from top-left looking front)
    # Format: [Width_Top, Height_Top, Width_Bottom, Height_Bottom, Z_Pos]
    
    sections = [
        # Front Bumper
        [0.2, 0.1, 0.2, 0.05,  0.6], 
        # Hood Start
        [0.35, 0.175, 0.4, 0.05,  0.45],
        # Windshield Base
        [0.375, 0.2, 0.425, 0.05,  0.2],
        # Roof Start (Cabin Front)
        [0.3, 0.325, 0.425, 0.05,  0.075],
        # Roof End (Cabin Rear)
        [0.3, 0.325, 0.425, 0.05, -0.15],
        # Rear Window Base / Trunk Start
        [0.35, 0.225, 0.425, 0.05, -0.3],
        # Trunk End
        [0.325, 0.2, 0.4, 0.075, -0.525],
        # Rear Bumper
        [0.25, 0.125, 0.25, 0.075, -0.575]
    ]

    def add_quad(p1, p2, p3, p4, normal):
        # 1-2-3
        vertices.extend([*p1, *normal, 0, 1])
        vertices.extend([*p2, *normal, 1, 1])
        vertices.extend([*p3, *normal, 1, 0])
        # 1-3-4
        vertices.extend([*p1, *normal, 0, 1])
        vertices.extend([*p3, *normal, 1, 0])
        vertices.extend([*p4, *normal, 0, 0])

    # Generate mesh between sections
    for i in range(len(sections) - 1):
        curr = sections[i]
        next_s = sections[i+1]
        
        # Calculate 8 corners for the segment (4 current, 4 next)
        # We assume symmetry over X axis
        
        # Current Slice Points
        c_wt, c_ht, c_wb, c_hb, c_z = curr
        c_tl = [-c_wt/2, c_ht, c_z] # Top Left
        c_tr = [ c_wt/2, c_ht, c_z] # Top Right
        c_br = [ c_wb/2, c_hb, c_z] # Bottom Right
        c_bl = [-c_wb/2, c_hb, c_z] # Bottom Left
        
        # Next Slice Points
        n_wt, n_ht, n_wb, n_hb, n_z = next_s
        n_tl = [-n_wt/2, n_ht, n_z]
        n_tr = [ n_wt/2, n_ht, n_z]
        n_br = [ n_wb/2, n_hb, n_z]
        n_bl = [-n_wb/2, n_hb, n_z]
        
        # --- Top Face (Hood/Roof/Trunk) ---
        # Normal points UP
        add_quad(c_tl, c_tr, n_tr, n_tl, [0, 1, 0])
        
        # --- Right Face ---
        # Approximate normal to right
        add_quad(c_tr, c_br, n_br, n_tr, [1, 0, 0])
        
        # --- Left Face ---
        # Approximate normal to left
        add_quad(c_bl, c_tl, n_tl, n_bl, [-1, 0, 0])
        
        # --- Bottom Face ---
        add_quad(c_br, c_bl, n_bl, n_br, [0, -1, 0])

    # Cap the ends
    # Front Cap
    f = sections[0]
    add_quad([-f[0]/2, f[1], f[4]], [f[0]/2, f[1], f[4]], [f[2]/2, f[3], f[4]], [-f[2]/2, f[3], f[4]], [0, 0, 1])
    
    # Rear Cap
    r = sections[-1]
    add_quad([r[0]/2, r[1], r[4]], [-r[0]/2, r[1], r[4]], [-r[2]/2, r[3], r[4]], [r[2]/2, r[3], r[4]], [0, 0, -1])

    return np.array(vertices, dtype=np.float32)

# ==========================================
# PROCEDURAL CAR CLASS
# ==========================================

class ProceduralCar:
    """Advanced procedural Tesla-style car with smooth curves and metallic texture."""
    
    _shared_texture = None
    _texture_loaded = False
    _body_mesh = None
    _wheel_mesh = None
    
    def __init__(self, shader, lane=0, direction=1, car_index=0, is_bridge=False):
        """Initialize the procedural car.
        
        Args:
            shader: OpenGL shader program
            lane: 0 for left, 1 for right
            direction: 1 forward, -1 backward
            car_index: 0-11 for identification
            is_bridge: True if car is on bridge (moves on X-axis), False if on road (moves on Z-axis)
        """
        self.shader = shader
        self.lane = lane
        self.direction = 1 if direction >= 0 else -1
        self.car_index = car_index
        self.is_bridge = is_bridge
        
        if is_bridge:
            # Bridge cars - positioned by X coordinate, fixed Z
            self.position = [0.0, -0.1, 0.0]  # Will be set by application
            self.speed = 4.0 * self.direction  # Slightly faster on bridge
        else:
            # Road cars - positioned by Z coordinate, fixed X
            x_pos = 1.5 if lane == 0 else 2.5
            self.position = [x_pos, -0.1, 0.0]  # Will be set by application
            self.speed = 3.0 * self.direction
        
        self._wheel_spin = 0.0
        
        # Load shared resources
        if not ProceduralCar._texture_loaded:
            self._load_texture_once()
        
        if ProceduralCar._body_mesh is None:
            self._create_meshes()
        
        # Wheel positions
        self.wheel_positions = [
            glm.vec3(-0.225, 0.0875,  0.35),
            glm.vec3( 0.225, 0.0875,  0.35),
            glm.vec3(-0.225, 0.0875, -0.35),
            glm.vec3( 0.225, 0.0875, -0.35)
        ]
    
    @classmethod
    def _load_texture_once(cls):
        """Load PNG texture from file for all instances."""
        try:
            # Load car.png as car texture
            cls._shared_texture = Texture("assets/textures/car.png")
            cls._texture_loaded = True
            print("✅ Car texture loaded from PNG (car.png)")
        except Exception as e:
            print(f"Failed to load car texture: {e}")
            cls._texture_loaded = False
    
    @classmethod
    def _create_meshes(cls):
        """Create body and wheel meshes once for all instances."""
        try:
            # Create body mesh
            body_vertices = create_sedan_mesh()
            cls._body_mesh = Mesh(body_vertices)
            
            # Create wheel mesh
            wheel_vertices = create_wheel_mesh(radius=0.0875, width=0.0625, segments=32)
            cls._wheel_mesh = Mesh(wheel_vertices)
            
            print("✅ Procedural car meshes created")
        except Exception as e:
            print(f"Failed to create car meshes: {e}")
    
    def update(self, delta_time):
        """Update car position and wheel rotation."""
        if self.is_bridge:
            # Bridge cars move along X-axis
            self.position[0] += self.speed * delta_time
            
            # Wrap around on bridge (X range approximately -28 to 22)
            if self.direction > 0:
                if self.position[0] > 25.0:
                    self.position[0] = -30.0
            else:
                if self.position[0] < -30.0:
                    self.position[0] = 25.0
        else:
            # Road cars move along Z-axis
            self.position[2] += self.speed * delta_time
            
            # Wrap around on road
            if self.direction > 0:
                if self.position[2] > 15.0:
                    self.position[2] = -15.0
            else:
                if self.position[2] < -15.0:
                    self.position[2] = 15.0
        
        # Animate wheels
        wheel_radius = 0.35
        angular_speed = abs(self.speed) / wheel_radius
        self._wheel_spin += angular_speed * delta_time * (1 if self.direction > 0 else -1)
    
    def _get_car_color(self):
        """Get metallic car color."""
        # Adjust metallic red for lighting
        return (200/255, 20/255, 20/255)  # Metallic red
    
    def draw(self, view, projection, light_pos, view_pos):
        """Render the procedural car."""
        if not ProceduralCar._body_mesh or not ProceduralCar._wheel_mesh:
            return
        
        self.shader.use()
        self.shader.set_mat4("view", view)
        self.shader.set_mat4("projection", projection)
        self.shader.set_vec3("lightPos", light_pos)
        self.shader.set_vec3("viewPos", view_pos)
        self.shader.set_vec3("lightColor", (1.0, 1.0, 1.0))
        
        # Draw body
        model = glm.translate(glm.mat4(1.0), glm.vec3(self.position[0], self.position[1], self.position[2]))
        model = glm.translate(model, glm.vec3(0.0, 0.1, 0.0))  # Shift up for wheels
        
        if self.is_bridge:
            # Bridge cars: rotate 90 degrees to face along X-axis
            model = glm.rotate(model, glm.radians(90.0), glm.vec3(0, 1, 0))
            if self.direction == -1:
                model = glm.rotate(model, glm.radians(180.0), glm.vec3(0, 1, 0))
        else:
            # Road cars: standard orientation
            if self.direction == -1:
                model = glm.rotate(model, glm.radians(180.0), glm.vec3(0, 1, 0))
        
        self.shader.set_mat4("model", model)
        self.shader.set_vec3("objectColor", self._get_car_color())
        self.shader.set_bool("useTexture", True)
        
        if ProceduralCar._shared_texture:
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, ProceduralCar._shared_texture.texture_id)
            self.shader.set_sampler("texture1", 0)
        
        ProceduralCar._body_mesh.draw(self.shader)
        
        # Draw wheels
        self.shader.set_bool("useTexture", False)
        self.shader.set_vec3("objectColor", (0.2, 0.2, 0.2))
        
        for wheel_pos in self.wheel_positions:
            model = glm.translate(glm.mat4(1.0), glm.vec3(self.position[0], self.position[1], self.position[2]))
            model = glm.translate(model, glm.vec3(0.0, 0.1, 0.0))
            
            if self.is_bridge:
                # Bridge cars: rotate 90 degrees to face along X-axis
                model = glm.rotate(model, glm.radians(90.0), glm.vec3(0, 1, 0))
                if self.direction == -1:
                    model = glm.rotate(model, glm.radians(180.0), glm.vec3(0, 1, 0))
            else:
                # Road cars: standard orientation
                if self.direction == -1:
                    model = glm.rotate(model, glm.radians(180.0), glm.vec3(0, 1, 0))
            
            model = glm.translate(model, wheel_pos)
            # Rotate wheels around X-axis (the wheel is oriented along X-axis)
            model = glm.rotate(model, glm.radians(glm.degrees(self._wheel_spin)), glm.vec3(1, 0, 0))
            
            self.shader.set_mat4("model", model)
            ProceduralCar._wheel_mesh.draw(self.shader)
