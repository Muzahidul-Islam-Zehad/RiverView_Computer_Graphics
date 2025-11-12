"""
Main application class.
"""

import glfw
import OpenGL.GL as gl
import numpy as np
import glm
from config import *
from core.shader import Shader
from objects.terrain import Terrain
from objects.house import House
from utils.transformations import create_view_matrix, create_projection_matrix

class Application:
    def __init__(self):
        self.window = None
        self.running = True  # Changed to True by default
        self.shader = None
        self.terrain = None
        self.house = None
        
        # Camera
        self.camera_pos = glm.vec3(0.0, 3.0, 10.0)
        self.camera_front = glm.vec3(0.0, -0.3, -1.0)
        self.camera_up = glm.vec3(0.0, 1.0, 0.0)
        
        # Time
        self.delta_time = 0.0
        self.last_frame = 0.0
        
    def run(self):
        """Main application loop."""
        print("Starting application...")
        if not self._initialize():
            print("Initialization failed!")
            return
        
        print("Entering main loop...")
        self._main_loop()
        self._shutdown()
        print("Application closed successfully.")
    
    def _initialize(self):
        """Initialize GLFW and OpenGL."""
        if not glfw.init():
            print("Failed to initialize GLFW")
            return False
        
        # Window hints
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)
        
        # Create window
        self.window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, None, None)
        if not self.window:
            print("Failed to create window")
            glfw.terminate()
            return False
        
        glfw.make_context_current(self.window)
        glfw.set_key_callback(self.window, self._key_callback)
        glfw.set_framebuffer_size_callback(self.window, self._framebuffer_size_callback)
        
        # OpenGL configuration
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glClearColor(*BACKGROUND_COLOR)
        
        # Load shader and objects
        try:
            self.shader = Shader("assets/shaders/default.vert", "assets/shaders/default.frag")
            self.terrain = Terrain(self.shader)
            self.house = House(self.shader)
        except Exception as e:
            print(f"Initialization error: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        print("Application initialized successfully!")
        return True
    
    def _main_loop(self):
        """Main rendering loop."""
        frame_count = 0
        while not glfw.window_should_close(self.window) and self.running:
            # Time calculation
            current_frame = glfw.get_time()
            self.delta_time = current_frame - self.last_frame
            self.last_frame = current_frame
            
            # Print frame info occasionally
            frame_count += 1
            if frame_count % 100 == 0:
                print(f"Frame {frame_count}, FPS: {1.0/self.delta_time if self.delta_time > 0 else 0:.1f}")
            
            # Clear and render
            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
            self._render()
            
            # Swap buffers and poll events
            glfw.swap_buffers(self.window)
            glfw.poll_events()
    
    def _render(self):
        """Render the scene."""
        if not self.shader:
            return
            
        # Create matrices
        view = create_view_matrix(self.camera_pos, self.camera_front, self.camera_up)
        projection = create_projection_matrix(FOV, WINDOW_WIDTH/WINDOW_HEIGHT, NEAR_PLANE, FAR_PLANE)
        
        # Draw objects
        self.terrain.draw(view, projection)
        self.house.draw(view, projection, position=(5.0, 0.5, 0.0))
        
        # Draw ship (simple cube for now)
        self._draw_ship(view, projection)
    
    def _draw_ship(self, view, projection):
        """Draw a simple ship."""
        from rendering.mesh import Mesh
        from objects.primitives import create_cube
        from utils.transformations import create_model_matrix
        
        ship_mesh = Mesh(create_cube())
        model = create_model_matrix(position=(-3.0, 0.5, 0.0), scale=(1.5, 0.5, 0.8))
        
        self.shader.use()
        self.shader.set_mat4("model", model)
        self.shader.set_mat4("view", view)
        self.shader.set_mat4("projection", projection)
        self.shader.set_vec3("objectColor", (0.3, 0.3, 0.3))
        ship_mesh.draw()
    
    def _shutdown(self):
        """Cleanup resources."""
        print("Shutting down...")
        if self.window:
            glfw.destroy_window(self.window)
        glfw.terminate()
    
    def _key_callback(self, window, key, scancode, action, mods):
        """Handle keyboard input."""
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            print("ESC pressed - closing application")
            self.running = False
            glfw.set_window_should_close(window, True)
        
        # Camera movement
        camera_speed = 5.0 * self.delta_time
        if key == glfw.KEY_W and action in [glfw.PRESS, glfw.REPEAT]:
            self.camera_pos += camera_speed * self.camera_front
        if key == glfw.KEY_S and action in [glfw.PRESS, glfw.REPEAT]:
            self.camera_pos -= camera_speed * self.camera_front
        if key == glfw.KEY_A and action in [glfw.PRESS, glfw.REPEAT]:
            self.camera_pos -= glm.normalize(glm.cross(self.camera_front, self.camera_up)) * camera_speed
        if key == glfw.KEY_D and action in [glfw.PRESS, glfw.REPEAT]:
            self.camera_pos += glm.normalize(glm.cross(self.camera_front, self.camera_up)) * camera_speed
    
    def _framebuffer_size_callback(self, window, width, height):
        """Handle window resize."""
        gl.glViewport(0, 0, width, height)
        print(f"Window resized to {width}x{height}")