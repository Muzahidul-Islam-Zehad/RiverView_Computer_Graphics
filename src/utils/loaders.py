"""
Utility functions for loading assets.
"""

import os
from src.core.shader import Shader
from src.core.texture import Texture


def load_shader(vertex_path, fragment_path):
    """
    Load shader from vertex and fragment files.
    
    Args:
        vertex_path: Path to vertex shader
        fragment_path: Path to fragment shader
    
    Returns:
        Shader object
    """
    return Shader(vertex_path, fragment_path)


def load_texture(path, texture_unit=0):
    """
    Load texture from file.
    
    Args:
        path: Path to image file
        texture_unit: OpenGL texture unit
    
    Returns:
        Texture object
    """
    return Texture(path, texture_unit)


def load_obj(path):
    """
    Load OBJ file (placeholder).
    
    Args:
        path: Path to OBJ file
    
    Returns:
        Mesh object
    """
    # This is a placeholder - actual OBJ loading would require more implementation
    raise NotImplementedError("OBJ loading not yet implemented")
