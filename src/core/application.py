"""
Main application class with proper camera.
"""

import glfw
import OpenGL.GL as gl
import numpy as np
from config import *
from core.shader import Shader
from core.camera import Camera
from objects.terrain import Terrain
from objects.house import House
from utils.transformations import create_projection_matrix, create_projection_matrix_from_camera

class Application:
    def __init__(self):
        self.window = None
        self.running = True
        self.shader = None
        self.terrain = None
        self.house = None
        self.camera = None
        
        # Mouse handling
        self.first_mouse = True
        self.last_x = WINDOW_WIDTH / 2
        self.last_y = WINDOW_HEIGHT / 2
        self.last_frame = 0.0
        
        # Track pressed keys
        self.keys_pressed = set()
        
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
        
        # Set callbacks
        glfw.set_key_callback(self.window, self._key_callback)
        glfw.set_framebuffer_size_callback(self.window, self._framebuffer_size_callback)
        glfw.set_cursor_pos_callback(self.window, self._mouse_callback)
        glfw.set_scroll_callback(self.window, self._scroll_callback)
        
        # Capture mouse
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)
        
        # OpenGL configuration
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glClearColor(*BACKGROUND_COLOR)
        
        # Load shader and objects - USE TEXTURED SHADER
        try:
            self.shader = Shader("assets/shaders/textured.vert", "assets/shaders/textured.frag")
            self.camera = Camera()
            self.terrain = Terrain(self.shader)
            self.house = House(self.shader)
        except Exception as e:
            print(f"Initialization error: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        print("Application initialized successfully!")
        print("Controls:")
        print("  WASD - Move camera")
        print("  Mouse - Look around")
        print("  Scroll - Zoom in/out")
        print("  Space - Move up")
        print("  Shift - Move down")
        print("  ESC - Exit")
        return True
    
    def _main_loop(self):
        """Main rendering loop."""
        while not glfw.window_should_close(self.window) and self.running:
            # Time calculation
            current_frame = glfw.get_time()
            delta_time = current_frame - self.last_frame
            self.last_frame = current_frame
            
            # Process continuous keyboard input
            self._process_continuous_input(delta_time)
            
            # Clear and render
            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
            self._render(delta_time)
            
            # Swap buffers and poll events
            glfw.swap_buffers(self.window)
            glfw.poll_events()
    
    def _process_continuous_input(self, delta_time):
        """Process continuous keyboard input for smooth movement."""
        # WASD movement
        if glfw.KEY_W in self.keys_pressed:
            self.camera.process_keyboard("FORWARD", delta_time)
        if glfw.KEY_S in self.keys_pressed:
            self.camera.process_keyboard("BACKWARD", delta_time)
        if glfw.KEY_A in self.keys_pressed:
            self.camera.process_keyboard("LEFT", delta_time)
        if glfw.KEY_D in self.keys_pressed:
            self.camera.process_keyboard("RIGHT", delta_time)
        
        # Up/Down movement
        if glfw.KEY_SPACE in self.keys_pressed:
            self.camera.process_keyboard("UP", delta_time)
        if glfw.KEY_LEFT_SHIFT in self.keys_pressed:
            self.camera.process_keyboard("DOWN", delta_time)
    
    def _render(self, delta_time):
        """Render the scene."""
        if not self.shader:
            return
            
        # Create matrices using camera
        view = self.camera.get_view_matrix_array()
        projection = create_projection_matrix_from_camera(
            self.camera, WINDOW_WIDTH/WINDOW_HEIGHT, NEAR_PLANE, FAR_PLANE
        )
        
        # Lighting setup
        light_pos = (10.0, 10.0, 10.0)  # Light position in world space
        view_pos = (self.camera.position.x, self.camera.position.y, self.camera.position.z)
        
        # Draw objects with lighting
        self.terrain.draw(view, projection, light_pos, view_pos)
        self.house.draw(view, projection, light_pos, view_pos, position=(5.0, 0.5, 0.0))
        
        # Draw ship
        self._draw_ship(view, projection, light_pos, view_pos)
    
    def _draw_ship(self, view, projection, light_pos, view_pos):
        """Draw a simple ship."""
        from rendering.mesh import Mesh
        from objects.primitives import create_cube_with_uv
        from utils.transformations import create_model_matrix
        
        ship_mesh = Mesh(create_cube_with_uv())
        model = create_model_matrix(position=(-3.0, 0.5, 0.0), scale=(1.5, 0.5, 0.8))
        
        self.shader.use()
        self.shader.set_mat4("model", model)
        self.shader.set_mat4("view", view)
        self.shader.set_mat4("projection", projection)
        self.shader.set_vec3("lightPos", light_pos)
        self.shader.set_vec3("viewPos", view_pos)
        self.shader.set_vec3("lightColor", (1.0, 1.0, 1.0))
        self.shader.set_vec3("objectColor", (0.3, 0.3, 0.3))
        ship_mesh.draw(self.shader)
    
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
        
        # Track key presses for continuous movement
        if action == glfw.PRESS:
            self.keys_pressed.add(key)
        elif action == glfw.RELEASE:
            self.keys_pressed.discard(key)
    
    def _mouse_callback(self, window, xpos, ypos):
        """Handle mouse movement."""
        if self.first_mouse:
            self.last_x = xpos
            self.last_y = ypos
            self.first_mouse = False
        
        xoffset = xpos - self.last_x
        yoffset = self.last_y - ypos  # Reversed since y-coordinates go from bottom to top
        
        self.last_x = xpos
        self.last_y = ypos
        
        self.camera.process_mouse_movement(xoffset, yoffset)
    
    def _scroll_callback(self, window, xoffset, yoffset):
        """Handle mouse scroll."""
        self.camera.process_mouse_scroll(yoffset)
    
    def _framebuffer_size_callback(self, window, width, height):
        """Handle window resize."""
        gl.glViewport(0, 0, width, height)