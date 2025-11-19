"""
Pure Python noise functions for terrain generation.
No external dependencies required.
"""

import math
import random
import numpy as np

class PurePythonNoise:
    @staticmethod
    def random_gradient(ix, iy):
        """Random gradient vector using hash function."""
        random.seed(ix * 1619 + iy * 31337)
        angle = random.random() * math.pi * 2
        return math.cos(angle), math.sin(angle)
    
    @staticmethod
    def dot_grid_gradient(ix, iy, x, y):
        """Compute dot product between distance and gradient vectors."""
        gradient = PurePythonNoise.random_gradient(ix, iy)
        dx = x - ix
        dy = y - iy
        return dx * gradient[0] + dy * gradient[1]
    
    @staticmethod
    def perlin_noise(x, y):
        """2D Perlin noise implementation in pure Python."""
        # Determine grid cell coordinates
        x0 = math.floor(x)
        x1 = x0 + 1
        y0 = math.floor(y)
        y1 = y0 + 1
        
        # Determine interpolation weights
        sx = x - x0
        sy = y - y0
        
        # Interpolate between grid point gradients
        n0 = PurePythonNoise.dot_grid_gradient(x0, y0, x, y)
        n1 = PurePythonNoise.dot_grid_gradient(x1, y0, x, y)
        ix0 = PurePythonNoise.lerp(n0, n1, sx)
        
        n0 = PurePythonNoise.dot_grid_gradient(x0, y1, x, y)
        n1 = PurePythonNoise.dot_grid_gradient(x1, y1, x, y)
        ix1 = PurePythonNoise.lerp(n0, n1, sx)
        
        value = PurePythonNoise.lerp(ix0, ix1, sy)
        return value
    
    @staticmethod
    def lerp(a, b, t):
        """Linear interpolation."""
        return a + t * (b - a)
    
    @staticmethod
    def fractal_noise(x, y, octaves=4, persistence=0.5, lacunarity=2.0):
        """Fractal noise using multiple octaves of Perlin noise."""
        value = 0.0
        amplitude = 1.0
        frequency = 1.0
        max_value = 0.0
        
        for i in range(octaves):
            value += PurePythonNoise.perlin_noise(x * frequency, y * frequency) * amplitude
            max_value += amplitude
            amplitude *= persistence
            frequency *= lacunarity
        
        return value / max_value
    
    @staticmethod
    def ridge_noise(x, y, octaves=4, lacunarity=2.0, gain=0.5, offset=1.0):
        """Ridge noise for sharp mountain features."""
        result = 0.0
        frequency = 1.0
        amplitude = 0.5
        weight = 1.0
        
        for i in range(octaves):
            # Get noise value
            n = PurePythonNoise.perlin_noise(x * frequency, y * frequency)
            
            # Ridge transformation
            n = offset - abs(n)
            n *= n
            n *= weight
            weight = n * gain
            if weight > 1.0: weight = 1.0
            if weight < 0.0: weight = 0.0
            
            result += n * amplitude
            amplitude *= lacunarity
            frequency *= lacunarity
        
        return result