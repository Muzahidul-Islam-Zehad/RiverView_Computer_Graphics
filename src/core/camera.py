"""
Camera class for controlling view and projection matrices.
"""

import numpy as np
from glm import mat4, vec3, lookAt, perspective, radians


class Camera:
    """Manages camera position, view, and projection matrices."""

    def __init__(self, position, target, up, fov=45.0, aspect=1.33, near=0.1, far=100.0):
        """
        Initialize the camera.
        
        Args:
            position: Initial camera position (vec3 or tuple)
            target: Look-at target (vec3 or tuple)
            up: Up vector (vec3 or tuple)
            fov: Field of view in degrees
            aspect: Aspect ratio (width/height)
            near: Near clipping plane
            far: Far clipping plane
        """
        self.position = vec3(position)
        self.target = vec3(target)
        self.up = vec3(up)
        self.fov = fov
        self.aspect = aspect
        self.near = near
        self.far = far

    def get_view_matrix(self):
        """Return the view matrix."""
        return lookAt(self.position, self.target, self.up)

    def get_projection_matrix(self):
        """Return the projection matrix."""
        return perspective(radians(self.fov), self.aspect, self.near, self.far)

    def move(self, direction, distance):
        """
        Move the camera in a given direction.
        
        Args:
            direction: Direction vector (vec3)
            distance: Distance to move
        """
        direction = vec3(direction)
        self.position += direction * distance
        self.target += direction * distance

    def pan(self, right, up):
        """
        Pan the camera (strafe and vertical movement).
        
        Args:
            right: Strafe distance (positive = right)
            up: Vertical distance (positive = up)
        """
        forward = self.target - self.position
        right_vec = np.cross([forward.x, forward.y, forward.z], [self.up.x, self.up.y, self.up.z])
        right_vec = right_vec / (np.linalg.norm(right_vec) + 1e-6)
        
        self.position += vec3(right_vec) * right
        self.target += vec3(right_vec) * right
        
        self.position += self.up * up
        self.target += self.up * up

    def rotate(self, yaw, pitch):
        """
        Rotate the camera around its position (FPS-style).
        
        Args:
            yaw: Horizontal rotation in degrees
            pitch: Vertical rotation in degrees
        """
        # This would require more complex implementation with quaternions
        # Simplified version - can be expanded
        pass

    def zoom(self, factor):
        """
        Zoom in/out by adjusting FOV.
        
        Args:
            factor: Zoom factor (positive = zoom in)
        """
        self.fov = max(5.0, min(90.0, self.fov - factor))
