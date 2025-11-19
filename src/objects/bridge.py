"""
Bridge class - Realistic suspension bridge spanning the river.
Features: tall towers, main cables, vertical suspender cables, railings, and textured deck.
"""

import numpy as np
from rendering.mesh import Mesh
from objects.primitives import create_cube_with_uv
from utils.transformations import create_model_matrix

class Bridge:
    def __init__(self, shader):
        self.shader = shader
        self.cube_mesh = None
        self.cylinder_mesh = None
        
        self._setup_bridge()
    
    def _setup_bridge(self):
        """Setup bridge components."""
        cube_vertices = create_cube_with_uv()
        self.cube_mesh = Mesh(cube_vertices)
    
    def _draw_cylinder(self, position, scale, color):
        """Draw a cylinder approximation using scaled cube."""
        model = create_model_matrix(position=position, scale=scale)
        self.shader.set_mat4("model", model)
        self.shader.set_vec3("objectColor", color)
        self.cube_mesh.draw(self.shader)
    
    def draw(self, view, projection, light_pos, view_pos):
        """Draw a realistic suspension bridge."""
        self.shader.use()
        self.shader.set_mat4("view", view)
        self.shader.set_mat4("projection", projection)
        self.shader.set_vec3("lightPos", light_pos)
        self.shader.set_vec3("viewPos", view_pos)
        self.shader.set_vec3("lightColor", (1.0, 1.0, 1.0))
        
        # === BRIDGE PARAMETERS ===
        bridge_center = -3.0
        bridge_width = 3.0  # Wider deck
        bridge_length = 50.0  # Much much longer bridge
        tower_height = 4.5
        tower_x_left = bridge_center - bridge_length / 2.5
        tower_x_right = bridge_center + bridge_length / 2.5
        deck_y = 1.8
        tower_base_y = -0.2
        bridge_z_offset = -8.0  # Move bridge further back
        
        # ===== TOWERS (Dual Columns - Left and Right sides of bridge) =====
        tower_color = (0.3, 0.3, 0.35)  # Dark gray steel
        
        # Left tower - positioned on LEFT SIDE of bridge
        left_tower_col1_model = create_model_matrix(
            position=(tower_x_left, tower_base_y + tower_height/2, -bridge_width/2 - 0.3 + bridge_z_offset),
            scale=(0.25, tower_height, 0.25)
        )
        self.shader.set_mat4("model", left_tower_col1_model)
        self.shader.set_vec3("objectColor", tower_color)
        self.cube_mesh.draw(self.shader)
        
        # Left tower - second column on LEFT SIDE of bridge
        left_tower_col2_model = create_model_matrix(
            position=(tower_x_left, tower_base_y + tower_height/2, bridge_width/2 + 0.3 + bridge_z_offset),
            scale=(0.25, tower_height, 0.25)
        )
        self.shader.set_mat4("model", left_tower_col2_model)
        self.shader.set_vec3("objectColor", tower_color)
        self.cube_mesh.draw(self.shader)
        
        # Right tower - positioned on RIGHT SIDE of bridge
        right_tower_col1_model = create_model_matrix(
            position=(tower_x_right, tower_base_y + tower_height/2, -bridge_width/2 - 0.3 + bridge_z_offset),
            scale=(0.25, tower_height, 0.25)
        )
        self.shader.set_mat4("model", right_tower_col1_model)
        self.shader.set_vec3("objectColor", tower_color)
        self.cube_mesh.draw(self.shader)
        
        # Right tower - second column on RIGHT SIDE of bridge
        right_tower_col2_model = create_model_matrix(
            position=(tower_x_right, tower_base_y + tower_height/2, bridge_width/2 + 0.3 + bridge_z_offset),
            scale=(0.25, tower_height, 0.25)
        )
        self.shader.set_mat4("model", right_tower_col2_model)
        self.shader.set_vec3("objectColor", tower_color)
        self.cube_mesh.draw(self.shader)
        
        # ===== MAIN CABLES (thick steel cables) =====
        main_cable_color = (0.2, 0.2, 0.25)  # Very dark steel
        cable_y_top = tower_base_y + tower_height + 0.3
        
        # Left main cable
        cable_length = np.sqrt((tower_x_right - tower_x_left)**2 + (cable_y_top - deck_y)**2)
        cable_angle = np.arctan2(cable_y_top - deck_y, tower_x_right - tower_x_left)
        cable_center_x = (tower_x_left + tower_x_right) / 2
        cable_center_y = (cable_y_top + deck_y) / 2
        
        # Note: Using cube to approximate cable (in real scenario, would use cylinder)
        left_cable_model = create_model_matrix(
            position=(cable_center_x, cable_center_y, -bridge_width/2 - 0.2 + bridge_z_offset),
            scale=(cable_length * 0.95, 0.08, 0.08)
        )
        self.shader.set_mat4("model", left_cable_model)
        self.shader.set_vec3("objectColor", main_cable_color)
        self.cube_mesh.draw(self.shader)
        
        # Right main cable (mirrored)
        right_cable_model = create_model_matrix(
            position=(cable_center_x, cable_center_y, bridge_width/2 + 0.2 + bridge_z_offset),
            scale=(cable_length * 0.95, 0.08, 0.08)
        )
        self.shader.set_mat4("model", right_cable_model)
        self.shader.set_vec3("objectColor", main_cable_color)
        self.cube_mesh.draw(self.shader)
        
        # ===== THIN VERTICAL SUPPORT COLUMNS (from cables to deck) =====
        column_color = (0.25, 0.25, 0.30)  # Dark steel
        base_column_height = cable_y_top - deck_y
        column_width = 0.12  # Very thin columns
        num_support_columns = 30  # Many more columns for longer bridge
        column_spacing = bridge_length / (num_support_columns + 1)
        
        # Left side support columns (connecting cables to deck)
        for i in range(num_support_columns):
            col_x = bridge_center - bridge_length/2 + (i + 1) * column_spacing
            
            # Create wavy pattern - columns have different heights
            wave_factor = np.sin((i / num_support_columns) * np.pi * 2) * 0.4
            column_height = base_column_height + wave_factor
            column_center_y = deck_y + column_height/2
            
            # Left side column
            left_support = create_model_matrix(
                position=(col_x, column_center_y, -bridge_width/2 - 0.2 + bridge_z_offset),
                scale=(column_width, column_height, column_width)
            )
            self.shader.set_mat4("model", left_support)
            self.shader.set_vec3("objectColor", column_color)
            self.cube_mesh.draw(self.shader)
            
            # Right side column
            right_support = create_model_matrix(
                position=(col_x, column_center_y, bridge_width/2 + 0.2 + bridge_z_offset),
                scale=(column_width, column_height, column_width)
            )
            self.shader.set_mat4("model", right_support)
            self.shader.set_vec3("objectColor", column_color)
            self.cube_mesh.draw(self.shader)
        
        # ===== BRIDGE DECK =====
        deck_color = (0.35, 0.32, 0.28)  # Brown-gray asphalt
        deck_model = create_model_matrix(
            position=(bridge_center, deck_y, bridge_z_offset),
            scale=(bridge_length, 0.25, bridge_width)
        )
        self.shader.set_mat4("model", deck_model)
        self.shader.set_vec3("objectColor", deck_color)
        self.cube_mesh.draw(self.shader)
        
        # ===== DECK STRIPES (center line) =====
        stripe_color = (1.0, 1.0, 1.0)  # White
        stripe_y = deck_y + 0.14  # Slightly above deck
        num_stripes = 12
        stripe_spacing = bridge_length / num_stripes
        
        for i in range(num_stripes):
            stripe_x = bridge_center - bridge_length/2 + i * stripe_spacing + stripe_spacing/2
            stripe_model = create_model_matrix(
                position=(stripe_x, stripe_y, bridge_z_offset),
                scale=(stripe_spacing * 0.4, 0.01, 0.15)
            )
            self.shader.set_mat4("model", stripe_model)
            self.shader.set_vec3("objectColor", stripe_color)
            self.cube_mesh.draw(self.shader)
        
        
        # ===== CORNER RAILINGS =====
        railing_color = (0.4, 0.4, 0.42)  # Light-medium gray
        railing_height = 0.8
        railing_thickness = 0.15
        
        # Front-left corner railing
        front_left_railing = create_model_matrix(
            position=(bridge_center - bridge_length/2, deck_y + railing_height/2, -bridge_width/2 - 0.1 + bridge_z_offset),
            scale=(0.5, railing_height, railing_thickness)
        )
        self.shader.set_mat4("model", front_left_railing)
        self.shader.set_vec3("objectColor", railing_color)
        self.cube_mesh.draw(self.shader)
        
        # Front-right corner railing
        front_right_railing = create_model_matrix(
            position=(bridge_center - bridge_length/2, deck_y + railing_height/2, bridge_width/2 + 0.1 + bridge_z_offset),
            scale=(0.5, railing_height, railing_thickness)
        )
        self.shader.set_mat4("model", front_right_railing)
        self.shader.set_vec3("objectColor", railing_color)
        self.cube_mesh.draw(self.shader)
        
        # Back-left corner railing
        back_left_railing = create_model_matrix(
            position=(bridge_center + bridge_length/2, deck_y + railing_height/2, -bridge_width/2 - 0.1 + bridge_z_offset),
            scale=(0.5, railing_height, railing_thickness)
        )
        self.shader.set_mat4("model", back_left_railing)
        self.shader.set_vec3("objectColor", railing_color)
        self.cube_mesh.draw(self.shader)
        
        # Back-right corner railing
        back_right_railing = create_model_matrix(
            position=(bridge_center + bridge_length/2, deck_y + railing_height/2, bridge_width/2 + 0.1 + bridge_z_offset),
            scale=(0.5, railing_height, railing_thickness)
        )
        self.shader.set_mat4("model", back_right_railing)
        self.shader.set_vec3("objectColor", railing_color)
        self.cube_mesh.draw(self.shader)