"""
Main application class with proper camera.
"""

import glfw
import OpenGL.GL as gl
import numpy as np
import random
import math
import glm
from config import *
from core.shader import Shader
from core.camera import Camera
from objects.terrain import Terrain
from objects.house import AdvancedHouse
from objects.roof import PyramidRoof
from objects.bridge import Bridge
from objects.road import Road
from objects.car import ProceduralCar
from objects.advanced_tree import AdvancedTree
from objects.log import Log
from objects.water import Water
from objects.mountain import Mountain
from objects.advanced_mountain import AdvancedMountain
from objects.christmas_tree import ChristmasTree
from objects.clouds import CloudSystem
from objects.smoke import SmokeSystem
from objects.ship import Ship
from utils.transformations import create_projection_matrix, create_projection_matrix_from_camera

class Application:
    def __init__(self):
        self.window = None
        self.running = True
        self.shader = None
        self.terrain = None
        self.house = None
        self.roof = None
        self.camera = None
        self.bridge = None
        self.road = None
        self.cars = []
        self.trees = []
        self.logs = []
        self.water = None
        self.mountains = []
        self.christmas_trees = []
        self.cloud_system = None
        self.smoke_system = None
        self.ship = None
        
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
            self.terrain = Terrain(self.shader) 
            self.house = AdvancedHouse(self.shader)
            self.roof = PyramidRoof(self.shader)
            self.bridge = Bridge(self.shader)
            self.road = Road(self.shader)
            
            # Create procedural Tesla cars on two lanes of the ROAD
            # Left lane (X=1.5) - cars going forward
            for i in range(3):
                car = ProceduralCar(self.shader, lane=0, direction=1, car_index=i)
                car.position[2] = -10.0 + i * 6.0
                self.cars.append(car)
            
            # Right lane (X=2.5) - cars going backward
            for i in range(3):
                car = ProceduralCar(self.shader, lane=1, direction=-1, car_index=i+3)
                car.position[2] = 10.0 - i * 6.0
                self.cars.append(car)
            
            # Create procedural Tesla cars on the BRIDGE
            # Bridge is at Z=-8.0, spans from X=-28 to X22 (center at -3)
            # Bridge deck is at Y=1.8, width is 3.0, so lanes at roughly Z=-8.5 and Z=-7.5
            
            # Left lane (Z=-8.5) - cars going forward along X-axis
            for i in range(2):
                car = ProceduralCar(self.shader, lane=0, direction=1, car_index=i+6, is_bridge=True)
                car.position[0] = -20.0 + i * 10.0  # Spread along bridge length
                car.position[1] = 1.8  # Bridge deck height
                car.position[2] = -8.5  # Left lane of bridge
                self.cars.append(car)
            
            # Right lane (Z=-7.5) - cars going backward along X-axis
            for i in range(2):
                car = ProceduralCar(self.shader, lane=1, direction=-1, car_index=i+8, is_bridge=True)
                car.position[0] = 15.0 - i * 10.0  # Spread along bridge length
                car.position[1] = 1.8  # Bridge deck height
                car.position[2] = -7.5  # Right lane of bridge
                self.cars.append(car)
            
            self.water = Water(self.water_shader)
            
            # Create advanced mountains
            self.mountains = [
                AdvancedMountain(self.shader, position=(7.0, -1.0, -12.0), size=12.0, max_height=8.0, seed=1),  # Right back
                AdvancedMountain(self.shader, position=(10.0, -1.0, -3.0), size=12.0, max_height=8.0, seed=2),    # Right front
                AdvancedMountain(self.shader, position=(-12.0, -1.0, -12.0), size=12.0, max_height=8.0, seed=3),   # Left back
                AdvancedMountain(self.shader, position=(-14.0, -1.0, -3.0), size=12.0, max_height=8.0, seed=4),    # Left front
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
            
            # Create Christmas tree forest filling empty GROUND on left side of river
            self.christmas_trees = []
            # Fill the flat ground areas between mountains and river on left side
            random.seed(42)  # For consistent placement
            
            # Ground area between left mountains and river (X: -8 to -11, Z: -10 to 8)
            for i in range(100):
                x = -8.5 - random.uniform(0, 3)  # Between mountains and river (X: -8.5 to -11.5)
                z = -10.0 + random.uniform(-5, 15)  # Safe ground area (Z: -15 to 5)
                tree = ChristmasTree(self.shader)
                self.christmas_trees.append({
                    'tree': tree,
                    'position': (x, -0.25, z),
                    'scale': 0.4 + random.uniform(0, 0.9)  # Random height scale 0.4 to 1.3
                })
            
            # Create cloud system for dynamic sky
            self.cloud_system = CloudSystem(self.shader, num_clouds=8)
            
            # Create smoke system from chimney (house chimney is at X=5.0, positioned above roof)
            self.smoke_system = SmokeSystem(self.shader, chimney_position=(5.0, 1.5, 0.0))
            
            # Create ship on the river (river center is at X=-3.0, Y slightly above water)
            self.ship = Ship(self.shader, position=(-3.0, 0.1, 0.0))
                
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
        for car in self.cars:
            car.update(delta_time)
        self.water.update(delta_time)
        if self.cloud_system:
            self.cloud_system.update(delta_time)
        if self.smoke_system:
            self.smoke_system.update(delta_time)
        if self.ship:
            self.ship.update(delta_time)
        
        # Set time uniform for main shader
        self.shader.use()
        self.shader.set_float("time", current_time)
        
        # CORRECT RENDER ORDER:
        
        # 0. Draw clouds (sky) - render first so they appear in background
        if self.cloud_system:
            self.cloud_system.draw(view, projection, light_pos, view_pos)
        
        # 1. Draw advanced mountains (terrain generation with noise)
        for mountain in self.mountains:
            mountain.draw(view, projection, light_pos, view_pos)
        
        # 2. Draw terrain (ground and river channel) - uses main shader
        self.terrain.draw(view, projection, light_pos, view_pos)
        
        # 3. Draw water - uses WATER SHADER (different from terrain!)
        self.water.draw(view, projection, light_pos, view_pos)
        
        # 3.5 Draw ship on the river
        if self.ship:
            self.ship.draw(view, projection, light_pos, view_pos)
        
        # 4. Draw other objects - use main shader
        self.road.draw(view, projection, light_pos, view_pos)
        self.bridge.draw(view, projection, light_pos, view_pos)
        self.house.draw(view, projection, light_pos, view_pos, position=(5.0, -0.25, 0.0))
        
        # Draw pyramid roof (positioned above house)
        self.roof.draw(view, projection, light_pos, view_pos, position=(5.0, 0.55, 0.0))
        
        # 5. Draw procedural cars on the road
        for car in self.cars:
            car.draw(view, projection, light_pos, view_pos)
        
        # 6. Draw trees
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
        
        # 6.5 Draw logs around trees
        for log, log_pos, log_rot in self.logs:
            log.draw(view, projection, light_pos, view_pos, log_pos, log_rot)
        
        # 7. Draw Christmas tree forest on left side of river
        self.shader.use()
        self.shader.set_mat4("view", view)
        self.shader.set_mat4("projection", projection)
        self.shader.set_vec3("lightPos", light_pos)
        self.shader.set_vec3("viewPos", view_pos)
        self.shader.set_vec3("lightColor", (1.0, 1.0, 1.0))
        
        # Bind texture once for all trees (major optimization)
        texture_bound = False
        if self.christmas_trees and self.christmas_trees[0]['tree'].tree_texture:
            self.christmas_trees[0]['tree'].tree_texture.bind(0)
            self.shader.set_sampler("texture_diffuse1", 0)
            self.shader.set_bool("useTexture", True)
            texture_bound = True
        
        for tree_data in self.christmas_trees:
            tree = tree_data['tree']
            pos = tree_data['position']
            scale = tree_data['scale']
            
            for part in tree.tree_parts:
                # Create model matrix with scale
                part_pos = (
                    pos[0] + part['position'][0] * scale,
                    pos[1] + part['position'][1] * scale,
                    pos[2] + part['position'][2] * scale
                )
                model = glm.translate(glm.mat4(1.0), glm.vec3(part_pos[0], part_pos[1], part_pos[2]))
                model = glm.scale(model, glm.vec3(scale, scale, scale))
                
                self.shader.set_mat4("model", model)
                self.shader.set_vec3("objectColor", part['color'])
                part['mesh'].draw(self.shader)
        
        if not texture_bound:
            self.shader.set_bool("useTexture", False)
        
        # 8. Draw smoke from chimney
        if self.smoke_system:
            self.smoke_system.draw(view, projection, light_pos, view_pos)
    
    def _shutdown(self):
        """Cleanup resources."""
        print("Shutting down...")
        
        # DEBUG: Print camera position
        if self.camera:
            print("\n" + "="*60)
            print("DEBUG: CAMERA POSITION AT SHUTDOWN")
            print("="*60)
            pos = self.camera.position
            front = self.camera.front
            up = self.camera.up
            yaw = self.camera.yaw
            pitch = self.camera.pitch
            
            print(f"Position: ({pos.x:.2f}, {pos.y:.2f}, {pos.z:.2f})")
            print(f"Front: ({front.x:.2f}, {front.y:.2f}, {front.z:.2f})")
            print(f"Up: ({up.x:.2f}, {up.y:.2f}, {up.z:.2f})")
            print(f"Yaw: {yaw:.2f}°")
            print(f"Pitch: {pitch:.2f}°")
            print("="*60)
            print("\nTo use this position, copy these values to the Camera initialization")
            print("="*60 + "\n")
        
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