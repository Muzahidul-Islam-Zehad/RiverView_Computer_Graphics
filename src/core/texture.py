"""
Texture loading and management class.
"""

import OpenGL.GL as gl
from PIL import Image
import numpy as np

class Texture:
    def __init__(self, filepath):
        self.texture_id = None
        self._load_texture(filepath)
    
    def _load_texture(self, filepath):
        """Load texture from file."""
        try:
            print(f"Loading texture: {filepath}")
            
            # Load image
            image = Image.open(filepath)
            
            # Convert RGBA to RGB if it has an alpha channel
            if image.mode == 'RGBA':
                print(f"Converting RGBA to RGB (removing transparency)")
                # Create a white background
                background = Image.new('RGB', image.size, (255, 255, 255))
                # Paste the image on the white background using the alpha channel as mask
                background.paste(image, mask=image.split()[3])
                image = background
            elif image.mode != 'RGB':
                image = image.convert('RGB')
            
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
            img_data = np.array(image, dtype=np.uint8)
            
            # Generate texture
            self.texture_id = gl.glGenTextures(1)
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture_id)
            
            # Set texture parameters
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
            
            # Always use RGB format now (no transparency)
            format = gl.GL_RGB
            
            # Upload texture data
            gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, format, image.width, image.height, 
                          0, format, gl.GL_UNSIGNED_BYTE, img_data)
            gl.glGenerateMipmap(gl.GL_TEXTURE_2D)
            
            print(f"✅ Texture loaded: {filepath} ({image.width}x{image.height})")
            
        except Exception as e:
            print(f"❌ Failed to load texture {filepath}: {e}")
            raise
    
    def bind(self, texture_unit=0):
        """Bind texture to texture unit."""
        if self.texture_id:
            gl.glActiveTexture(gl.GL_TEXTURE0 + texture_unit)
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture_id)
    
    def __del__(self):
        """Clean up texture."""
        if hasattr(self, 'texture_id') and self.texture_id:
            try:
                gl.glDeleteTextures(1, [self.texture_id])
            except:
                pass