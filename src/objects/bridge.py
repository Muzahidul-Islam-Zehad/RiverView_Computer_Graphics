"""
Bridge class for rendering a bridge structure.
"""

from src.rendering.model import Model
from src.objects.primitives import create_cube
import config


class Bridge(Model):
    """Class to define and render a bridge."""

    def __init__(self, position=(0, 0, 0)):
        """
        Initialize bridge.
        
        Args:
            position: Position of bridge center
        """
        # Create bridge deck
        deck = create_cube(size=1.0)
        
        super().__init__([deck], position)
        self.bridge_color = config.COLOR_CONCRETE

    def draw(self):
        """Draw the bridge."""
        super().draw()

    def update(self, delta_time):
        """Update bridge state."""
        pass
