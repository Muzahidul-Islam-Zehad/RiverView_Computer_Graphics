#!/usr/bin/env python3
"""
Simple test script to verify OpenGL and GLFW setup.
"""

import glfw
import OpenGL.GL as gl

def test_opengl():
    # Initialize GLFW
    if not glfw.init():
        print("❌ Failed to initialize GLFW")
        return False
    
    # Configure window
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)
    
    # Create window
    window = glfw.create_window(800, 600, "OpenGL Test", None, None)
    if not window:
        print("❌ Failed to create GLFW window")
        glfw.terminate()
        return False
    
    glfw.make_context_current(window)
    
    # Test OpenGL
    print("✅ GLFW initialized successfully")
    print(f"✅ OpenGL version: {gl.glGetString(gl.GL_VERSION).decode()}")
    print(f"✅ Renderer: {gl.glGetString(gl.GL_RENDERER).decode()}")
    
    glfw.destroy_window(window)
    glfw.terminate()
    return True

if __name__ == "__main__":
    test_opengl()