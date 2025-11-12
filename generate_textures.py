#!/usr/bin/env python3
"""
Generate simple placeholder textures.
"""

from PIL import Image, ImageDraw
import os

def create_grass_texture():
    """Create a simple grass texture."""
    size = 256
    img = Image.new('RGB', (size, size), color=(100, 200, 100))
    draw = ImageDraw.Draw(img)
    
    # Add some grass-like patterns
    for i in range(1000):
        x = np.random.randint(0, size)
        y = np.random.randint(0, size)
        color = (80, 180, 80) if np.random.random() > 0.5 else (120, 220, 120)
        draw.point((x, y), fill=color)
    
    return img

def create_road_texture():
    """Create a simple road texture."""
    size = 256
    img = Image.new('RGB', (size, size), color=(100, 100, 100))
    draw = ImageDraw.Draw(img)
    
    # Add some road-like patterns
    for i in range(500):
        x = np.random.randint(0, size)
        y = np.random.randint(0, size)
        color = (80, 80, 80) if np.random.random() > 0.7 else (120, 120, 120)
        draw.point((x, y), fill=color)
    
    return img

def create_water_texture():
    """Create a simple water texture."""
    size = 256
    img = Image.new('RGB', (size, size), color=(100, 150, 255))
    draw = ImageDraw.Draw(img)
    
    # Add some wave-like patterns
    for i in range(200):
        x = np.random.randint(0, size)
        y = np.random.randint(0, size)
        color = (80, 130, 240) if np.random.random() > 0.5 else (120, 170, 255)
        draw.point((x, y), fill=color)
    
    return img

def main():
    """Generate all placeholder textures."""
    textures_dir = "assets/textures"
    os.makedirs(textures_dir, exist_ok=True)
    
    # Generate textures
    grass_img = create_grass_texture()
    road_img = create_road_texture()
    water_img = create_water_texture()
    
    # Save textures
    grass_img.save(f"{textures_dir}/grass.png")
    road_img.save(f"{textures_dir}/road.png")
    water_img.save(f"{textures_dir}/water.png")
    
    print("Generated placeholder textures:")
    print("- grass.png")
    print("- road.png") 
    print("- water.png")

if __name__ == "__main__":
    import numpy as np
    main()