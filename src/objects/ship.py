"""
Procedurally generated ship model for the river scene.
Features: Textured ship with hull, decks, and cabin. Floats on the river.
"""

import numpy as np
import glm
import ctypes
from OpenGL.GL import *
from PIL import Image


class Ship:
    """A procedural ship model that floats on the river."""
    
    _ship_mesh = None  # Class-level mesh (created once)
    _ship_texture = None  # Class-level texture (created once)
    
    def __init__(self, shader, position=(0.0, 0.1, 0.0)):
        """Initialize the ship.
        
        Args:
            shader: OpenGL shader program (uses application shader)
            position: (x, y, z) position of the ship center
        """
        self.shader = shader
        self.position = np.array(position, dtype=np.float32)
        self.rotation = 180.0  # Rotation around Y axis in degrees
        self.speed = 2.0  # Units per second (movement speed)
        self.scale = 0.4  # Scale down the ship to 40% of original size
        
        # Create mesh and texture once (shared across all ship instances)
        if Ship._ship_mesh is None:
            Ship._ship_mesh = self._create_ship_mesh()
        if Ship._ship_texture is None:
            Ship._ship_texture = self._create_ship_texture()
    
    @staticmethod
    def _create_ship_mesh():
        """Create procedural ship mesh with VAO/VBO."""
        vertices = []
        
        def add_vertex(x, y, z, nx, ny, nz, u, v):
            """Add a vertex to the list."""
            vertices.extend([x, y, z, nx, ny, nz, u, v])
        
        def add_quad(p1, p2, p3, p4, normal, uv_scale=1.0):
            """Add a quad face (2 triangles)."""
            nx, ny, nz = normal
            # Triangle 1
            add_vertex(*p1, nx, ny, nz, 0.0, 0.0)
            add_vertex(*p2, nx, ny, nz, 1.0 * uv_scale, 0.0)
            add_vertex(*p3, nx, ny, nz, 1.0 * uv_scale, 1.0)
            # Triangle 2
            add_vertex(*p1, nx, ny, nz, 0.0, 0.0)
            add_vertex(*p3, nx, ny, nz, 1.0 * uv_scale, 1.0)
            add_vertex(*p4, nx, ny, nz, 0.0, 1.0)
        
        def create_box(pos, size, uv_repeat=1.0):
            """Create a box mesh."""
            x, y, z = pos
            w, h, d = size  # width, height, depth
            
            hw, hh, hd = w/2, h/2, d/2
            
            # Define corners
            p1 = (x-hw, y-hh, z+hd)  # Front Bottom Left
            p2 = (x+hw, y-hh, z+hd)  # Front Bottom Right
            p3 = (x+hw, y+hh, z+hd)  # Front Top Right
            p4 = (x-hw, y+hh, z+hd)  # Front Top Left
            
            p5 = (x-hw, y-hh, z-hd)  # Back Bottom Left
            p6 = (x+hw, y-hh, z-hd)  # Back Bottom Right
            p7 = (x+hw, y+hh, z-hd)  # Back Top Right
            p8 = (x-hw, y+hh, z-hd)  # Back Top Left
            
            # Add 6 faces
            add_quad(p1, p2, p3, p4, (0, 0, 1), uv_repeat)  # Front
            add_quad(p6, p5, p8, p7, (0, 0, -1), uv_repeat)  # Back
            add_quad(p5, p1, p4, p8, (-1, 0, 0), uv_repeat)  # Left
            add_quad(p2, p6, p7, p3, (1, 0, 0), uv_repeat)  # Right
            add_quad(p4, p3, p7, p8, (0, 1, 0), 1.0)  # Top
            add_quad(p5, p6, p2, p1, (0, -1, 0), 1.0)  # Bottom
        
        def create_wedge(pos, size):
            """Create the pointy bow of the ship."""
            x, y, z = pos
            w, h, d = size
            hw, hh, hd = w/2, h/2, d/2
            
            # Base vertices
            p1 = (x-hw, y-hh, z+hd)
            p2 = (x+hw, y-hh, z+hd)
            p3 = (x+hw, y+hh, z+hd)
            p4 = (x-hw, y+hh, z+hd)
            
            # Front tip
            tip_top = (x, y+hh, z-hd)
            
            # Right side face
            add_quad(p2, (x, y-hh, z-hd), tip_top, p3, (1, 0, 1), 2.0)
            
            # Left side face
            add_quad((x, y-hh, z-hd), p1, p4, tip_top, (-1, 0, 1), 2.0)
            
            # Top face
            add_quad(p4, p3, tip_top, tip_top, (0, 1, 0), 1.0)
        
        # Build the ship geometry
        # 1. Main Hull (the body)
        create_box((0, 0, 2), (3.0, 2.0, 8.0), uv_repeat=4.0)
        
        # 2. Pointy Bow (front)
        create_wedge((0, 0, -4.0), (3.0, 2.0, 4.0))
        
        # 3. First Deck (cabin)
        create_box((0, 1.5, 3), (2.5, 1.0, 5.0), uv_repeat=3.0)
        
        # 4. Second Deck (upper cabin)
        create_box((0, 2.2, 3.5), (2.2, 0.8, 3.0), uv_repeat=2.0)
        
        # 5. Bridge (cockpit)
        create_box((0, 2.5, 1.5), (2.0, 0.6, 1.5), uv_repeat=1.0)
        
        # Convert to numpy array
        ship_vertices = np.array(vertices, dtype=np.float32)
        print(f"✅ Ship mesh created with {len(vertices)//8} vertices")
        
        # Create VAO/VBO
        vao = glGenVertexArrays(1)
        vbo = glGenBuffers(1)
        
        glBindVertexArray(vao)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, ship_vertices.nbytes, ship_vertices, GL_STATIC_DRAW)
        
        # Vertex attributes (8 floats per vertex: 3 pos, 3 normal, 2 uv)
        stride = 8 * 4
        
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(3 * 4))
        glEnableVertexAttribArray(1)
        
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(6 * 4))
        glEnableVertexAttribArray(2)
        
        glBindVertexArray(0)
        
        return {"vao": vao, "vbo": vbo, "vertex_count": len(vertices) // 8}
    
    @staticmethod
    def _create_ship_texture():
        """Create procedural ship hull texture."""
        width, height = 256, 256
        img = Image.new('RGB', (width, height), (240, 240, 240))  # White hull
        pixels = img.load()
        
        # Draw windows (dark blue glass)
        for y in range(80, 140):
            for x in range(width):
                if (x // 30) % 2 == 0:  # Spaced windows
                    pixels[x, y] = (20, 20, 40)  # Dark blue
        
        # Add wood trim at bottom
        for y in range(230, 240):
            for x in range(width):
                pixels[x, y] = (139, 69, 19)  # Wood brown
        
        # Convert to OpenGL texture
        img_data = img.tobytes()
        
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        
        print("✅ Ship texture created")
        return texture_id
    
    def update(self, delta_time):
        """Update ship position (animate along river)."""
        # Move ship along Z axis (along the river)
        self.position[2] += self.speed * delta_time
        
        # Wrap around when off-screen
        if self.position[2] > 20.0:
            self.position[2] = -20.0
    
    def draw(self, view, projection, light_pos, view_pos):
        """Draw the ship using the application shader."""
        if Ship._ship_mesh is None:
            return
        
        self.shader.use()
        self.shader.set_mat4("view", view)
        self.shader.set_mat4("projection", projection)
        self.shader.set_vec3("lightPos", light_pos)
        self.shader.set_vec3("viewPos", view_pos)
        
        # Create model matrix with translation, rotation, and scale
        model = glm.translate(glm.mat4(1.0), glm.vec3(
            self.position[0],
            self.position[1],
            self.position[2]
        ))
        model = glm.rotate(model, glm.radians(self.rotation), glm.vec3(0, 1, 0))
        model = glm.scale(model, glm.vec3(self.scale, self.scale, self.scale))
        
        self.shader.set_mat4("model", model)
        self.shader.set_vec3("objectColor", (1.0, 1.0, 1.0))  # White
        self.shader.set_bool("useTexture", True)
        
        # Bind texture
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, Ship._ship_texture)
        self.shader.set_sampler("texture1", 0)
        
        # Draw
        glBindVertexArray(Ship._ship_mesh["vao"])
        glDrawArrays(GL_TRIANGLES, 0, Ship._ship_mesh["vertex_count"])
        glBindVertexArray(0)
        
        self.shader.set_bool("useTexture", False)