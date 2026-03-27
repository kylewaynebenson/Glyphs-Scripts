# MenuTitle: Create Corner Components
# -*- coding: utf-8 -*-
__doc__ = """
Creates multiple _corner glyphs with graduated sizes.
Each corner component is a square with rounded corners based on the specified curve tension.
"""

from GlyphsApp import Glyphs, GSGlyph, GSLayer, GSPath, GSNode
from vanilla import FloatingWindow, TextBox, EditText, Slider, CheckBox, Button
import math


class CreateCornerComponentsDialog(object):

    def __init__(self):
        # Window setup
        windowWidth = 280
        windowHeight = 220
        
        self.w = FloatingWindow((windowWidth, windowHeight), "Create Corner Components")
        
        lineHeight = 22
        padding = 10
        y = padding
        
        # Count
        self.w.countLabel = TextBox((padding, y + 2, 100, lineHeight), "Count:")
        self.w.countField = EditText((120, y, -padding, lineHeight), "2")
        y += lineHeight + 8
        
        # Curve tension
        self.w.tensionLabel = TextBox((padding, y + 2, 100, lineHeight), "Curve tension:")
        self.w.tensionField = EditText((120, y, 50, lineHeight), "55")
        self.w.tensionPercent = TextBox((175, y + 2, 30, lineHeight), "%")
        y += lineHeight + 8
        
        # Smallest size
        self.w.smallLabel = TextBox((padding, y + 2, 100, lineHeight), "Smallest size:")
        self.w.smallField = EditText((120, y, -padding, lineHeight), "10")
        y += lineHeight + 8
        
        # Largest size
        self.w.largeLabel = TextBox((padding, y + 2, 100, lineHeight), "Largest size:")
        self.w.largeField = EditText((120, y, -padding, lineHeight), "20")
        y += lineHeight + 8
        
        # Round up checkbox
        self.w.roundUp = CheckBox((padding, y, -padding, lineHeight), "Round up to integer", value=True)
        y += lineHeight + 16
        
        # Create button
        self.w.createButton = Button((padding, y, -padding, lineHeight + 4), "Create", callback=self.create_corners)
        
        self.w.center()
        self.w.open()

    def calculate_sizes(self, count, smallest, largest, round_up):
        """Calculate the sizes for each corner component."""
        if count == 1:
            sizes = [smallest]
        else:
            step = (largest - smallest) / (count - 1)
            sizes = [smallest + step * i for i in range(count)]
        
        if round_up:
            sizes = [math.ceil(s) for s in sizes]
        
        return sizes

    def create_corner_path(self, size, tension):
        """
        Create a corner path (quarter circle approximation) with given size and tension.
        The corner component should be a right-angle corner with a curve.
        """
        path = GSPath()
        
        # Calculate handle length based on tension
        # Tension of ~55% gives a good circular approximation
        handle_length = size * (tension / 100.0)
        
        # Create the corner path
        # Start at origin (the corner point)
        # The path goes: down from origin, curves, then goes left to end
        
        # Node 1: Start point (top of the corner) - LINE node
        node1 = GSNode()
        node1.position = (0, size)
        node1.type = 'line'
        path.nodes.append(node1)
        
        # Node 2: Off-curve handle for the curve
        node2 = GSNode()
        node2.position = (0, size - handle_length)
        node2.type = 'offcurve'
        path.nodes.append(node2)
        
        # Node 3: Off-curve handle for the curve
        node3 = GSNode()
        node3.position = (size - handle_length, 0)
        node3.type = 'offcurve'
        path.nodes.append(node3)
        
        # Node 4: End point (right side of the corner) - CURVE node
        node4 = GSNode()
        node4.position = (size, 0)
        node4.type = 'curve'
        path.nodes.append(node4)
        
        path.closed = False
        return path

    def create_corners(self, sender):
        """Main function to create the corner components."""
        try:
            # Get values from dialog
            count = int(self.w.countField.get())
            tension = float(self.w.tensionField.get())
            smallest = float(self.w.smallField.get())
            largest = float(self.w.largeField.get())
            round_up = self.w.roundUp.get()
            
            # Validate inputs
            if count < 1:
                print("❌ Count must be at least 1")
                return
            if tension < 0 or tension > 100:
                print("❌ Tension must be between 0 and 100")
                return
            if smallest > largest:
                print("❌ Smallest size cannot be larger than largest size")
                return
            
            font = Glyphs.font
            if not font:
                print("❌ No font open")
                return
            
            # Calculate sizes
            sizes = self.calculate_sizes(count, smallest, largest, round_up)
            
            print("=== Creating Corner Components ===")
            print(f"Count: {count}, Tension: {tension}%, Sizes: {sizes}")
            print()
            
            created_count = 0
            
            for size in sizes:
                # Format size for glyph name (remove decimal if whole number)
                if size == int(size):
                    size_str = str(int(size))
                else:
                    size_str = str(size)
                
                glyph_name = f"_corner.{size_str}x{size_str}"
                
                # Check if glyph already exists
                existing_glyph = font.glyphs[glyph_name]
                if existing_glyph:
                    print(f"⚠️ Glyph '{glyph_name}' already exists, skipping")
                    continue
                
                # Create new glyph
                new_glyph = GSGlyph(glyph_name)
                font.glyphs.append(new_glyph)
                
                # Create the corner path for each master
                for master in font.masters:
                    layer = new_glyph.layers[master.id]
                    layer.width = 0  # Corner components typically have 0 width
                    
                    # Create and add the corner path
                    corner_path = self.create_corner_path(size, tension)
                    layer.paths.append(corner_path)
                
                print(f"✓ Created '{glyph_name}'")
                created_count += 1
            
            print()
            if created_count > 0:
                print(f"🎉 Successfully created {created_count} corner component(s)")
            else:
                print("No new corner components were created")
            
            self.w.close()
            
        except ValueError as e:
            print(f"❌ Invalid input: Please enter valid numbers")
            print(f"   Error: {e}")
        except Exception as e:
            Glyphs.showMacroWindow()
            print(f"❌ Error creating corner components: {e}")
            import traceback
            print(traceback.format_exc())


CreateCornerComponentsDialog()
