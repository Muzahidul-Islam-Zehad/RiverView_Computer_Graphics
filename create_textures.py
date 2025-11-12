#!/usr/bin/env python3
"""
Generate visible texture patterns.
"""

from PIL import Image, ImageDraw
import os
import random

def create_grass_texture():
    """Create a visible grass texture."""
    size = 256
    img = Image.new('RGB', (size, size), color=(100, 200, 100))
    draw = ImageDraw.Draw(img)
    
    # Draw visible grass blades
    for i in range(500):
        x = random.randint(0, size-1)
        y = random.randint(0, size-1)
        length = random.randint(5, 15)
        color = (80, 180, 80) if random.random() > 0.5 else (120, 220, 120)
        
        # Draw a grass blade
        for j in range(length):
            if y + j < size:
                draw.point((x, y + j), fill=color)
    
    # Add some dark spots
    for i in range(100):
        x = random.randint(0, size-1)
        y = random.randint(0, size-1)
        draw.point((x, y), fill=(60, 140, 60))
    
    return img

def create_road_texture():
    """Create a visible road texture."""
    size = 256
    img = Image.new('RGB', (size, size), color=(80, 80, 80))
    draw = ImageDraw.Draw(img)
    
    # Add road markings
    for i in range(0, size, 20):
        draw.line([(i, 0), (i, size)], fill=(120, 120, 120), width=1)
    
    # Add some random spots
    for i in range(200):
        x = random.randint(0, size-1)
        y = random.randint(0, size-1)
        color = (100, 100, 100) if random.random() > 0.5 else (60, 60, 60)
        draw.point((x, y), fill=color)
    
    return img

def create_water_texture():
    """Create a visible water texture."""
    size = 256
    img = Image.new('RGB', (size, size), color=(80, 130, 255))
    draw = ImageDraw.Draw(img)
    
    # Draw wave patterns
    for i in range(0, size, 10):
        for j in range(0, size, 10):
            color = (100, 150, 255) if (i + j) % 20 == 0 else (60, 110, 240)
            draw.rectangle([i, j, i+8, j+8], fill=color)
    
    return img

def create_concrete_texture():
    """Create concrete texture for bridge."""
    size = 256
    img = Image.new('RGB', (size, size), color=(180, 180, 180))
    draw = ImageDraw.Draw(img)
    
    # Add concrete patterns
    for i in range(0, size, 15):
        draw.line([(i, 0), (i, size)], fill=(160, 160, 160), width=1)
        draw.line([(0, i), (size, i)], fill=(160, 160, 160), width=1)
    
    return img

def main():
    """Generate all textures."""
    textures_dir = "assets/textures"
    os.makedirs(textures_dir, exist_ok=True)
    
    print("Generating visible textures...")
    
    grass_img = create_grass_texture()
    road_img = create_road_texture() 
    water_img = create_water_texture()
    concrete_img = create_concrete_texture()
    
    grass_img.save(f"{textures_dir}/grass.png")
    road_img.save(f"{textures_dir}/road.png")
    water_img.save(f"{textures_dir}/water.png")
    concrete_img.save(f"{textures_dir}/concrete.png")
    
    print("✅ Generated visible textures:")
    print("   - grass.png (green with grass blades)")
    print("   - road.png (gray with lines)")
    print("   - water.png (blue with wave pattern)")
    print("   - concrete.png (gray with grid)")

if __name__ == "__main__":
    main()