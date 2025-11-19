#!/usr/bin/env python3
"""
Generate realistic rock and mountain textures.
"""

from PIL import Image, ImageDraw, ImageFilter
import random
import os

def create_rock_texture():
    """Create a realistic rock texture."""
    size = 512
    img = Image.new('RGB', (size, size), color=(120, 120, 120))
    draw = ImageDraw.Draw(img)
    
    # Base rock color variations
    base_colors = [
        (100, 100, 100),  # Dark gray
        (130, 130, 130),  # Medium gray
        (80, 80, 80),     # Very dark gray
        (150, 150, 150),  # Light gray
    ]
    
    # Create rock patterns
    for i in range(10000):
        x = random.randint(0, size-1)
        y = random.randint(0, size-1)
        color = random.choice(base_colors)
        
        # Add some color variations for mineral deposits
        if random.random() < 0.1:
            color = (140, 120, 100)  # Brownish rock
        elif random.random() < 0.05:
            color = (100, 140, 120)  # Greenish rock
        
        size_var = random.randint(1, 3)
        for dx in range(size_var):
            for dy in range(size_var):
                if 0 <= x+dx < size and 0 <= y+dy < size:
                    draw.point((x+dx, y+dy), fill=color)
    
    # Add some cracks and fissures
    for i in range(50):
        start_x = random.randint(0, size-1)
        start_y = random.randint(0, size-1)
        length = random.randint(10, 30)
        
        for j in range(length):
            x = start_x + j
            y = start_y + random.randint(-1, 1)
            if 0 <= x < size and 0 <= y < size:
                draw.point((x, y), fill=(60, 60, 60))
    
    # Apply blur for more natural look
    img = img.filter(ImageFilter.GaussianBlur(1))
    
    return img

def create_snow_texture():
    """Create snow texture for mountain peaks."""
    size = 256
    img = Image.new('RGB', (size, size), color=(240, 240, 255))
    draw = ImageDraw.Draw(img)
    
    # Add some snow variation
    for i in range(2000):
        x = random.randint(0, size-1)
        y = random.randint(0, size-1)
        
        if random.random() < 0.3:
            color = (255, 255, 255)  # Pure white
        else:
            color = (230, 230, 245)  # Bluish white
        
        draw.point((x, y), fill=color)
    
    return img

def main():
    """Generate mountain textures."""
    textures_dir = "assets/textures"
    os.makedirs(textures_dir, exist_ok=True)
    
    print("Generating mountain textures...")
    
    rock_img = create_rock_texture()
    snow_img = create_snow_texture()
    
    rock_img.save(f"{textures_dir}/rock.png")
    snow_img.save(f"{textures_dir}/snow.png")
    
    print("✅ Generated mountain textures:")
    print("   - rock.png (realistic rock texture)")
    print("   - snow.png (snow texture for peaks)")

if __name__ == "__main__":
    main()