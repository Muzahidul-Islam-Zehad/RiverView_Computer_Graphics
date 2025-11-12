"""
Model class composed of multiple meshes.
"""

from glm import mat4, translate, rotate, scale, radians


class Model:
    """Represents a 3D model composed of meshes."""

    def __init__(self, meshes=None, position=(0, 0, 0), rotation=(0, 0, 0), scale_val=(1, 1, 1)):
        """
        Initialize model.
        
        Args:
            meshes: List of Mesh objects
            position: Initial position (x, y, z)
            rotation: Initial rotation (x, y, z) in degrees
            scale_val: Initial scale (x, y, z)
        """
        self.meshes = meshes or []
        self.position = list(position)
        self.rotation = list(rotation)
        self.scale = list(scale_val)

    def add_mesh(self, mesh):
        """Add a mesh to the model."""
        self.meshes.append(mesh)

    def get_model_matrix(self):
        """Get the model transformation matrix."""
        m = mat4(1.0)
        m = translate(m, self.position)
        m = rotate(m, radians(self.rotation[0]), (1, 0, 0))
        m = rotate(m, radians(self.rotation[1]), (0, 1, 0))
        m = rotate(m, radians(self.rotation[2]), (0, 0, 1))
        m = scale(m, self.scale)
        return m

    def draw(self):
        """Draw all meshes in the model."""
        for mesh in self.meshes:
            mesh.draw()

    def delete(self):
        """Delete all meshes."""
        for mesh in self.meshes:
            mesh.delete()

    def set_position(self, x, y, z):
        """Set model position."""
        self.position = [x, y, z]

    def set_rotation(self, x, y, z):
        """Set model rotation in degrees."""
        self.rotation = [x, y, z]

    def set_scale(self, x, y, z):
        """Set model scale."""
        self.scale = [x, y, z]
