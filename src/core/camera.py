"""
Camera class for 3D navigation with mouse look.
"""

import glm
import numpy as np

class Camera:
    def __init__(self):
        # Camera attributes
        self.position = glm.vec3(-8.0, 4.0, 5.0)  # Position to view left side forest
        self.front = glm.vec3(0.2, -0.3, -1.0)  # Look toward the river and trees
        self.up = glm.vec3(0.0, 1.0, 0.0)
        self.right = glm.vec3(1.0, 0.0, 0.0)
        self.world_up = glm.vec3(0.0, 1.0, 0.0)
        
        # Euler angles
        self.yaw = -60.0
        self.pitch = -15.0
        
        # Camera options
        self.movement_speed = 5.0
        self.mouse_sensitivity = 0.1
        self.zoom = 45.0
        
        # Update camera vectors
        self._update_camera_vectors()
    
    def get_view_matrix(self):
        """Return the view matrix."""
        return glm.lookAt(self.position, self.position + self.front, self.up)
    
    def get_view_matrix_array(self):
        """Return view matrix as numpy array for OpenGL."""
        view = self.get_view_matrix()
        return self._glm_to_array(view)
    
    def process_keyboard(self, direction, delta_time):
        """Process keyboard input for camera movement."""
        velocity = self.movement_speed * delta_time
        
        if direction == "FORWARD":
            self.position += self.front * velocity
        if direction == "BACKWARD":
            self.position -= self.front * velocity
        if direction == "LEFT":
            self.position -= self.right * velocity
        if direction == "RIGHT":
            self.position += self.right * velocity
        if direction == "UP":
            self.position += self.world_up * velocity
        if direction == "DOWN":
            self.position -= self.world_up * velocity
    
    def process_mouse_movement(self, xoffset, yoffset, constrain_pitch=True):
        """Process mouse movement for camera look."""
        xoffset *= self.mouse_sensitivity
        yoffset *= self.mouse_sensitivity
        
        self.yaw += xoffset
        self.pitch += yoffset
        
        # Constrain pitch to avoid flip
        if constrain_pitch:
            if self.pitch > 89.0:
                self.pitch = 89.0
            if self.pitch < -89.0:
                self.pitch = -89.0
        
        # Update camera vectors
        self._update_camera_vectors()
    
    def process_mouse_scroll(self, yoffset):
        """Process mouse scroll for zoom."""
        self.zoom -= yoffset
        if self.zoom < 1.0:
            self.zoom = 1.0
        if self.zoom > 45.0:
            self.zoom = 45.0
    
    def _update_camera_vectors(self):
        """Update camera vectors based on yaw and pitch."""
        # Calculate new front vector
        front = glm.vec3()
        front.x = glm.cos(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))
        front.y = glm.sin(glm.radians(self.pitch))
        front.z = glm.sin(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))
        
        self.front = glm.normalize(front)
        
        # Re-calculate right and up vectors
        self.right = glm.normalize(glm.cross(self.front, self.world_up))
        self.up = glm.normalize(glm.cross(self.right, self.front))
    
    def _glm_to_array(self, matrix):
        """Convert glm matrix to numpy array."""
        arr = np.zeros(16, dtype=np.float32)
        for i in range(4):
            for j in range(4):
                arr[i*4 + j] = matrix[i][j]
        return arr