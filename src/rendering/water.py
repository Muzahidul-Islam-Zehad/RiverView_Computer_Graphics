"""
Water rendering class with wave animation.
"""

from src.rendering.model import Model
from glm import mat4, translate, rotate, scale, radians
import numpy as np


class Water(Model):
    """Specialized model for water with wave animation."""

    def __init__(self, mesh, position=(0, 0, 0), size=(10, 1, 10), wave_amplitude=0.1, wave_freq=2.0):
        """
        Initialize water surface.
        
        Args:
            mesh: Mesh object for water geometry
            position: Position of water surface
            size: Dimensions (width, height, depth)
            wave_amplitude: Wave amplitude in units
            wave_freq: Wave frequency in Hz
        """
        super().__init__([mesh], position)
        self.size = list(size)
        self.wave_amplitude = wave_amplitude
        self.wave_frequency = wave_freq
        self.time = 0.0

    def update(self, delta_time):
        """Update animation time."""
        self.time += delta_time

    def get_model_matrix(self):
        """Get model matrix for water."""
        m = mat4(1.0)
        m = translate(m, self.position)
        m = scale(m, self.size)
        return m

    def get_wave_time(self):
        """Get current time for wave shader."""
        return self.time
