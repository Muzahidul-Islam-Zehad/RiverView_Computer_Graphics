"""
Shader class for loading, compiling, and managing OpenGL shaders.
"""

import OpenGL.GL as gl
import os
import numpy as np
import glm

class Shader:
    def __init__(self, vertex_path, fragment_path):
        """Load and compile shaders from files."""
        self.program_id = None
        self._compile_shader(vertex_path, fragment_path)
    
    def _compile_shader(self, vertex_path, fragment_path):
        """Compile vertex and fragment shaders and link them into a program."""
        # Read shader source code
        vertex_code = self._load_shader_file(vertex_path)
        fragment_code = self._load_shader_file(fragment_path)
        
        # Compile shaders
        vertex_shader = self._compile_shader_part(gl.GL_VERTEX_SHADER, vertex_code)
        fragment_shader = self._compile_shader_part(gl.GL_FRAGMENT_SHADER, fragment_code)
        
        # Create shader program and link
        self.program_id = gl.glCreateProgram()
        gl.glAttachShader(self.program_id, vertex_shader)
        gl.glAttachShader(self.program_id, fragment_shader)
        gl.glLinkProgram(self.program_id)
        
        # Check for linking errors
        if not gl.glGetProgramiv(self.program_id, gl.GL_LINK_STATUS):
            info_log = gl.glGetProgramInfoLog(self.program_id)
            raise Exception(f"Shader program linking failed:\n{info_log}")
        
        # Clean up individual shaders
        gl.glDeleteShader(vertex_shader)
        gl.glDeleteShader(fragment_shader)
        
        print(f"Shader program {self.program_id} compiled successfully!")
    
    def _load_shader_file(self, filepath):
        """Load shader source code from file."""
        try:
            with open(filepath, 'r') as file:
                return file.read()
        except Exception as e:
            raise Exception(f"Failed to load shader file {filepath}: {e}")
    
    def _compile_shader_part(self, shader_type, source_code):
        """Compile a single shader part (vertex or fragment)."""
        shader_id = gl.glCreateShader(shader_type)
        gl.glShaderSource(shader_id, source_code)
        gl.glCompileShader(shader_id)
        
        # Check for compilation errors
        if not gl.glGetShaderiv(shader_id, gl.GL_COMPILE_STATUS):
            info_log = gl.glGetShaderInfoLog(shader_id)
            shader_type_str = "VERTEX" if shader_type == gl.GL_VERTEX_SHADER else "FRAGMENT"
            raise Exception(f"{shader_type_str} shader compilation failed:\n{info_log}")
        
        return shader_id
    
    def use(self):
        """Activate this shader program."""
        gl.glUseProgram(self.program_id)
    
    def set_bool(self, name, value):
        """Set a boolean uniform."""
        gl.glUniform1i(gl.glGetUniformLocation(self.program_id, name), int(value))
    
    def set_int(self, name, value):
        """Set an integer uniform."""
        gl.glUniform1i(gl.glGetUniformLocation(self.program_id, name), value)
    
    def set_float(self, name, value):
        """Set a float uniform."""
        gl.glUniform1f(gl.glGetUniformLocation(self.program_id, name), value)
    
    def set_vec3(self, name, value):
        """Set a vec3 uniform."""
        gl.glUniform3f(gl.glGetUniformLocation(self.program_id, name), value[0], value[1], value[2])
    
    def set_mat4(self, name, value):
        """Set a mat4 uniform."""
        # Convert to numpy array for PyOpenGL
        if isinstance(value, np.ndarray):
            matrix_array = value
        else:
            # Manual conversion for glm matrices
            matrix_array = np.zeros(16, dtype=np.float32)
            for i in range(4):
                for j in range(4):
                    matrix_array[i*4 + j] = value[i][j]
        
        gl.glUniformMatrix4fv(
            gl.glGetUniformLocation(self.program_id, name), 
            1, 
            gl.GL_FALSE, 
            matrix_array
        )