"""
Configuration settings.
"""

# Window
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
WINDOW_TITLE = "Riverside Landscape 3D"

# Colors
BACKGROUND_COLOR = (0.53, 0.81, 0.98, 1.0)  # Sky blue

# Paths
SHADER_DIR = "assets/shaders"
TEXTURE_DIR = "assets/textures"
MODEL_DIR = "assets/models"

# Camera
INITIAL_CAMERA_POSITION = (0.0, 3.0, 10.0)
INITIAL_CAMERA_FRONT = (0.0, -0.3, -1.0)
INITIAL_CAMERA_UP = (0.0, 1.0, 0.0)
MOUSE_SENSITIVITY = 0.1
CAMERA_SPEED = 5.0

# Rendering
FOV = 45.0
NEAR_PLANE = 0.1
FAR_PLANE = 100.0
