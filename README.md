# RiversideLandscape3D

A 3D graphics application showcasing a scenic riverside landscape with mountains, water, a bridge, a ship, and a house.

## Project Structure

```
.
├── main.py                          # Entry point of the application
├── config.py                        # Stores window settings, colors, paths, etc.
│
├── src/                             # Main source code directory
│   ├── core/
│   │   ├── __init__.py
│   │   ├── application.py           # Main application loop and GLFW window management
│   │   ├── camera.py                # Camera class (movement, matrices)
│   │   ├── shader.py                # Shader compilation and management class
│   │   └── texture.py               # Texture loading class
│   │
│   ├── rendering/
│   │   ├── __init__.py
│   │   ├── mesh.py                  # Mesh class (VAO, VBO, EBO, drawing)
│   │   ├── model.py                 # Model class (composed of multiple meshes)
│   │   └── water.py                 # Specialized class for water rendering (with time-based animation)
│   │
│   ├── objects/
│   │   ├── __init__.py
│   │   ├── primitives.py            # Functions to generate cube, plane, sphere, etc.
│   │   ├── bridge.py                # Class to define and render the bridge
│   │   ├── ship.py                  # Class to define and render the ship (with movement logic)
│   │   ├── house.py                 # Class to define and render the countryside house
│   │   └── terrain.py               # Class for generating and rendering the mountains and riverbank
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── loaders.py               # Functions for loading OBJ files, images, etc.
│   │   ├── transformations.py       # Helper functions for common transformations
│   │   └── clock.py                 # Class to manage time and animation deltas
│   │
│   └── scene/
│       ├── __init__.py
│       └── scene_manager.py         # Manages all objects in the world, calls their update/draw methods
│
├── assets/
│   ├── shaders/
│   │   ├── default.vert             # Basic vertex shader
│   │   ├── default.frag             # Basic fragment shader
│   │   ├── water.vert               # Vertex shader for water (with wave animation)
│   │   └── water.frag               # Fragment shader for water (with transparency/reflection)
│   │
│   ├── textures/                    # Directory for all texture images
│   │   ├── grass.jpg
│   │   ├── mountain_rock.jpg
│   │   ├── water.png                # (Semi-transparent with ripples)
│   │   ├── road.jpg
│   │   ├── bridge_concrete.jpg
│   │   ├── ship_hull.jpg
│   │   ├── house_wall.jpg
│   │   └── house_roof.jpg
│   │
│   └── models/                      # (Optional) For pre-made 3D models if you don't generate everything procedurally
│       ├── tree.obj
│       └── car.obj
│
├── requirements.txt                 # Lists Python dependencies (glfw, PyOpenGL, numpy, PyGLM)
└── README.md                        # Project description and setup instructions
```

## Requirements

- Python 3.8+
- See `requirements.txt` for dependencies

## Installation

1. **Navigate to the project:**
```bash
cd D:\Computer Graphics Project\simulation
```

2. **Activate the virtual environment (if you have one):**
```bash
# On Windows:
.venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python main.py
```

The application will open a window displaying a 3D riverside landscape.

## Configuration

Edit `config.py` to customize:
- Window size and title
- Camera settings
- Colors and lighting
- Asset paths
- Animation speeds
- Debug options

## Architecture

### Core Classes

- **Application**: Manages GLFW window and OpenGL context
- **Camera**: Handles view and projection matrices
- **Shader**: Compiles and manages GLSL programs
- **Mesh**: Manages vertex data (VAO, VBO, EBO)
- **Model**: Container for meshes with transformation

### Scene Objects

- **Terrain**: Ground and mountains
- **Water**: Animated water surface with wave shader
- **Bridge**: Simple bridge structure
- **Ship**: Animated ship moving in a circular path
- **House**: Countryside house

### Utilities

- **Clock**: Frame timing and FPS calculation
- **loaders**: Asset loading functions
- **transformations**: Matrix helper functions
- **primitives**: Geometry generation (cube, plane, sphere, cylinder)

## Features

- ✓ 3D graphics rendering with OpenGL 3.3
- ✓ Shader system with vertex and fragment shaders
- ✓ Water animation with wave shader
- ✓ Moving ship with circular path
- ✓ Terrain and landscape
- ✓ Camera system
- ✓ Modular architecture

## Future Enhancements

- [ ] Texture mapping for all objects
- [ ] Improved lighting (Phong/PBR)
- [ ] Normal mapping
- [ ] Shadow mapping
- [ ] Particle effects
- [ ] Skybox
- [ ] Audio
- [ ] OBJ file loading
- [ ] Collision detection
- [ ] Input handling (WASD camera movement)

## Controls

*(To be implemented)*
- WASD: Camera movement
- Mouse: Camera rotation
- Scroll: Zoom
- ESC: Exit

## License

This project is provided as-is for educational purposes.

## Author

Created as a graphics programming learning project.
