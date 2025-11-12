"""
Ship class for rendering and animating a ship.
"""

from src.rendering.model import Model
from src.objects.primitives import create_cube
import config
import numpy as np


class Ship(Model):
    """Class to define and render a ship with movement."""

    def __init__(self, position=(0, 0, 0), path_radius=3.0):
        """
        Initialize ship.
        
        Args:
            position: Initial position
            path_radius: Radius of circular path
        """
        hull = create_cube(size=1.0)
        super().__init__([hull], position)
        
        self.ship_color = config.COLOR_WOOD
        self.path_radius = path_radius
        self.time = 0.0
        self.speed = config.SHIP_SPEED

    def update(self, delta_time):
        """Update ship position along path."""
        self.time += delta_time
        
        # Circular path
        angle = self.time * self.speed
        x = self.path_radius * np.cos(angle)
        z = self.path_radius * np.sin(angle)
        
        self.set_position(x, self.position[1], z)
        self.set_rotation(0, np.degrees(angle), 0)

    def draw(self):
        """Draw the ship."""
        super().draw()
