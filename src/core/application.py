"""
Main application class with proper camera.
"""

import glfw
import OpenGL.GL as gl
import numpy as np
import random
import math
from config import *
from core.shader import Shader
from core.camera import Camera
from objects.terrain import Terrain
from objects.house import House
from objects.bridge import Bridge
from objects.road import Road
from objects.car import Car
from objects.advanced_tree import AdvancedTree
from objects.log import Log
from objects.water import Water
from objects.mountain import Mountain
from objects.advanced_mountain import AdvancedMountain
from utils.transformations import create_projection_matrix, create_projection_matrix_from_camera

class Application:
    def __init__(self):
        self.window = None
        self.running = True
        self.shader = None
        self.terrain = None
        self.house = None
        self.camera = None
        self.bridge = None
        self.road = None
        self.car1 = None
        self.car2 = None
        self.trees = []
        self.logs = []
        self.water = None
        self.mountains = []
        
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
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glClearColor(*BACKGROUND_COLOR)
        
        # Load shaders and objects
        try:
            # Load main shader for most objects
            self.shader = Shader("assets/shaders/textured.vert", "assets/shaders/textured.frag")
            print(f"Main shader loaded: program {self.shader.program_id}")
            
            # Load WATER SHADER - separate from main shader
            self.water_shader = Shader("assets/shaders/water.vert", "assets/shaders/water.frag")
            print(f"Water shader loaded: program {self.water_shader.program_id}")
            
            # Create objects
            self.camera = Camera()
            self.terrain = Terrain(self.shader)  # Uses main shader
            self.house = House(self.shader)
            self.bridge = Bridge(self.shader)
            self.road = Road(self.shader)
            self.car1 = Car(self.shader)
            self.car2 = Car(self.shader)
            self.water = Water(self.water_shader)  # Uses WATER shader
            
            # Create advanced mountains
            self.mountains = [
                AdvancedMountain(self.shader, position=(7.0, -1.0, -12.0), size=12.0, max_height=8.0, seed=1),  # Right back (further back)
                AdvancedMountain(self.shader, position=(10.0, -1.0, -3.0), size=12.0, max_height=8.0, seed=2),    # Right front
            ]
            
            # Create advanced trees
            self.trees = []
            for i in range(5):
                tree = AdvancedTree(self.shader, height=1.2 + random.random() * 0.6, seed=i*10 + random.randint(0, 100))
                self.trees.append(tree)
            
            # Create logs around trees
            self.logs = []
            tree_positions = [
                (6.0, 0.0, 2.0),
                (7.0, 0.0, -1.0),
                (4.0, 0.0, 3.0),
                (5.5, 0.0, -2.5),
                (3.5, 0.0, -1.5)
            ]
            for tree_pos in tree_positions:
                # One log per tree at the center
                log = Log(self.shader)
                # Position log at tree center
                log_y = 0.5  # At middle of tree
                log_pos = (tree_pos[0], log_y, tree_pos[2])
                self.logs.append((log, log_pos, 0.0))
                
        except Exception as e:
            print(f"Initialization error: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        print("Application initialized successfully!")
        print("Controls: WASD, Mouse, Scroll, Space/Shift, ESC")
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
        """Render the scene with proper depth ordering."""
        if not self.shader:
            return
            
        # Create matrices using camera
        view = self.camera.get_view_matrix_array()
        projection = create_projection_matrix_from_camera(
            self.camera, WINDOW_WIDTH/WINDOW_HEIGHT, NEAR_PLANE, FAR_PLANE
        )
        
        # Lighting setup
        current_time = glfw.get_time()
        light_x = 5.0 * np.cos(current_time * 0.1)
        light_y = 8.0
        light_z = 5.0 * np.sin(current_time * 0.1)
        light_pos = (light_x, light_y, light_z)
        
        view_pos = (self.camera.position.x, self.camera.position.y, self.camera.position.z)
        
        # Update animated objects
        self.car1.update(delta_time)
        self.car2.update(delta_time)
        self.water.update(delta_time)
        
        # Set time uniform for main shader
        self.shader.use()
        self.shader.set_float("time", current_time)
        
        # CORRECT RENDER ORDER:
        
        # 0. Draw advanced mountains (terrain generation with noise)
        for mountain in self.mountains:
            mountain.draw(view, projection, light_pos, view_pos)
        
        # 1. Draw terrain (ground and river channel) - uses main shader
        self.terrain.draw(view, projection, light_pos, view_pos)
        
        # 2. Draw water - uses WATER SHADER (different from terrain!)
        self.water.draw(view, projection, light_pos, view_pos)
        
        # 3. Draw other objects - use main shader
        self.road.draw(view, projection, light_pos, view_pos)
        self.bridge.draw(view, projection, light_pos, view_pos)
        self.house.draw(view, projection, light_pos, view_pos, position=(5.0, 0.5, 0.0))
        
        # 4. Draw moving objects
        self.car1.draw(view, projection, light_pos, view_pos)
        self.car2.position[2] = self.car1.position[2] - 4.0
        self.car2.draw(view, projection, light_pos, view_pos)
        
        # DEBUG: Check which shader water is using
        # print(f"Water shader program: {self.water.shader.program_id}")
        # print(f"Main shader program: {self.shader.program_id}")
        
        # 5. Draw trees
        tree_positions = [
            (6.0, 0.0, 2.0),
            (7.0, 0.0, -1.0),
            (4.0, 0.0, 3.0),
            (5.5, 0.0, -2.5),
            (3.5, 0.0, -1.5)
        ]
        
        for i, tree in enumerate(self.trees):
            if i < len(tree_positions):
                tree.position = tree_positions[i]
                tree.draw(view, projection, light_pos, view_pos)
        
        # 5.5 Draw logs around trees
        for log, log_pos, log_rot in self.logs:
            log.draw(view, projection, light_pos, view_pos, log_pos, log_rot)
    
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