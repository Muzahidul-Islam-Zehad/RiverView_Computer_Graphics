"""
Scene manager for managing all objects and rendering.
"""

from src.core.camera import Camera
from src.core.shader import Shader
from src.rendering.water import Water
from src.objects.terrain import Terrain
from src.objects.bridge import Bridge
from src.objects.house import House
from src.objects.primitives import create_plane
import config


class SceneManager:
    """Manages all objects in the scene."""

    def __init__(self, camera, shader_default, shader_water):
        """
        Initialize scene manager.
        
        Args:
            camera: Camera object
            shader_default: Default shader program
            shader_water: Water shader program
        """
        self.camera = camera
        self.shader_default = shader_default
        self.shader_water = shader_water
        
        self.objects = []
        self.water = None
        self.terrain = None
        
        self._create_scene()

    def _create_scene(self):
        """Create all scene objects."""
        # Terrain
        self.terrain = Terrain(position=(0, -5, 0), width=50, depth=50, height=10)
        self.objects.append(self.terrain)
        
        # Water
        water_mesh = create_plane(width=10, depth=10, segments=20)
        self.water = Water(water_mesh, position=(0, 0, 0), size=(10, 1, 10))
        self.objects.append(self.water)
        
        # Bridge
        bridge = Bridge(position=(0, 0, 0))
        self.objects.append(bridge)
        
        # House
        house = House(position=(10, -5, 0))
        self.objects.append(house)

    def update(self, delta_time):
        """Update all objects."""
        for obj in self.objects:
            if hasattr(obj, 'update'):
                obj.update(delta_time)

    def render(self):
        """Render all objects."""
        for obj in self.objects:
            if hasattr(obj, 'draw'):
                obj.draw()

    def add_object(self, obj):
        """Add object to scene."""
        self.objects.append(obj)

    def remove_object(self, obj):
        """Remove object from scene."""
        if obj in self.objects:
            self.objects.remove(obj)

    def get_camera(self):
        """Get scene camera."""
        return self.camera

    def get_objects(self):
        """Get all scene objects."""
        return self.objects
