"""
Utility functions for common transformations and matrix operations.
"""

import numpy as np
import glm

def glm_to_array(matrix):
    """Convert glm matrix to numpy array for PyOpenGL."""
    # Manual conversion - extract each element from the glm matrix
    arr = np.zeros(16, dtype=np.float32)
    for i in range(4):
        for j in range(4):
            arr[i*4 + j] = matrix[i][j]
    return arr

def create_model_matrix(position=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1)):
    """Create model matrix with position, rotation, and scale."""
    model = glm.mat4(1.0)
    
    # Translation
    model = glm.translate(model, glm.vec3(position))
    
    # Rotation
    pitch, yaw, roll = rotation
    model = glm.rotate(model, glm.radians(pitch), glm.vec3(1.0, 0.0, 0.0))
    model = glm.rotate(model, glm.radians(yaw), glm.vec3(0.0, 1.0, 0.0))
    model = glm.rotate(model, glm.radians(roll), glm.vec3(0.0, 0.0, 1.0))
    
    # Scale
    model = glm.scale(model, glm.vec3(scale))
    
    return glm_to_array(model)

def create_view_matrix(camera_pos, camera_front, camera_up):
    """Create view matrix for camera."""
    view = glm.lookAt(
        glm.vec3(camera_pos),
        glm.vec3(camera_pos) + glm.vec3(camera_front),
        glm.vec3(camera_up)
    )
    return glm_to_array(view)

def create_projection_matrix(fov, aspect_ratio, near_plane, far_plane):
    """Create perspective projection matrix."""
    projection = glm.perspective(
        glm.radians(fov),
        aspect_ratio,
        near_plane,
        far_plane
    )
    return glm_to_array(projection)