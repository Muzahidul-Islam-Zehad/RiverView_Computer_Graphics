#!/usr/bin/env python3
"""
Simple test to verify OpenGL/GLFW setup.
"""

import glfw
import OpenGL.GL as gl

def main():
    # Initialize GLFW
    if not glfw.init():
        print("❌ Failed to initialize GLFW")
        return
    
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
        return
    
    glfw.make_context_current(window)
    
    # Set up OpenGL
    gl.glClearColor(0.2, 0.3, 0.8, 1.0)  # Blue background
    
    print("✅ OpenGL test window created successfully!")
    print(f"✅ OpenGL version: {gl.glGetString(gl.GL_VERSION).decode()}")
    print(f"✅ Renderer: {gl.glGetString(gl.GL_RENDERER).decode()}")
    print("✅ Press ESC to close the window")
    
    # Main loop
    while not glfw.window_should_close(window):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        glfw.swap_buffers(window)
        glfw.poll_events()
        
        # Close on ESC
        if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(window, True)
    
    glfw.destroy_window(window)
    glfw.terminate()
    print("✅ Test completed successfully!")

if __name__ == "__main__":
    main()