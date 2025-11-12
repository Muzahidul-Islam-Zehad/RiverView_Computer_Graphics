"""
Functions to generate basic 3D primitive shapes.
"""

import numpy as np

def create_triangle():
    """Create a simple triangle."""
    vertices = [-0.5, -0.5, 0.0, 0.5, -0.5, 0.0, 0.0, 0.5, 0.0]
    return np.array(vertices, dtype=np.float32)

def create_quad():
    """Create a simple quad."""
    vertices = [
        -0.5, -0.5, 0.0, 0.5, -0.5, 0.0, 0.5, 0.5, 0.0,
        0.5, 0.5, 0.0, -0.5, 0.5, 0.0, -0.5, -0.5, 0.0
    ]
    return np.array(vertices, dtype=np.float32)

def create_cube():
    """Create a cube."""
    vertices = [
        # Front face
        -0.5, -0.5, 0.5, 0.5, -0.5, 0.5, 0.5, 0.5, 0.5,
        0.5, 0.5, 0.5, -0.5, 0.5, 0.5, -0.5, -0.5, 0.5,
        # Back face
        -0.5, -0.5, -0.5, -0.5, 0.5, -0.5, 0.5, 0.5, -0.5,
        0.5, 0.5, -0.5, 0.5, -0.5, -0.5, -0.5, -0.5, -0.5,
        # Left face
        -0.5, -0.5, -0.5, -0.5, -0.5, 0.5, -0.5, 0.5, 0.5,
        -0.5, 0.5, 0.5, -0.5, 0.5, -0.5, -0.5, -0.5, -0.5,
        # Right face
        0.5, -0.5, 0.5, 0.5, -0.5, -0.5, 0.5, 0.5, -0.5,
        0.5, 0.5, -0.5, 0.5, 0.5, 0.5, 0.5, -0.5, 0.5,
        # Top face
        -0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, -0.5,
        0.5, 0.5, -0.5, -0.5, 0.5, -0.5, -0.5, 0.5, 0.5,
        # Bottom face
        -0.5, -0.5, -0.5, 0.5, -0.5, -0.5, 0.5, -0.5, 0.5,
        0.5, -0.5, 0.5, -0.5, -0.5, 0.5, -0.5, -0.5, -0.5
    ]
    return np.array(vertices, dtype=np.float32)

def create_plane(size=10.0):
    """Create a plane for ground."""
    half = size / 2.0
    vertices = [
        -half, 0.0, -half, half, 0.0, -half, half, 0.0, half,
        half, 0.0, half, -half, 0.0, half, -half, 0.0, -half
    ]
    return np.array(vertices, dtype=np.float32)