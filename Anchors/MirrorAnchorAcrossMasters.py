# MenuTitle: Mirror anchor across masters
# -*- coding: utf-8 -*-
__doc__="""
Takes a selected anchor and places it in corresponding positions 
across all masters based on positioning relative to shape bounds.
"""

from vanilla import Window, PopUpButton, CheckBox, Button, TextBox
from GlyphsApp import Glyphs, GSAnchor

class MirrorAnchorDialog:
    """Dialog for mirror anchor settings"""
    
    def __init__(self):
        # Window setup
        self.w = Window((300, 200), "Mirror Anchor Settings", minSize=(300, 200))
        
        # Y-axis positioning dropdown
        y = 20
        self.w.yAxisLabel = TextBox((20, y, 100, 20), "Y-axis position:")
        self.w.yAxisPopup = PopUpButton((130, y, 150, 20), [
            "Top", "Center", "Bottom"
        ])
        self.w.yAxisPopup.set(0)  # Default to Top
        
        # X-axis positioning dropdown
        y += 30
        self.w.xAxisLabel = TextBox((20, y, 100, 20), "X-axis position:")
        self.w.xAxisPopup = PopUpButton((130, y, 150, 20), [
            "Left", "Center", "Right"
        ])
        self.w.xAxisPopup.set(2)  # Default to Right
        
        # Relative to shapes checkbox
        y += 30
        self.w.relativeToShapes = CheckBox((20, y, 260, 20), "Relative to shapes")
        self.w.relativeToShapes.set(True)
        
        # Close after running checkbox
        y += 30
        self.w.closeAfterRunning = CheckBox((20, y, 200, 20), "Close after running")
        self.w.closeAfterRunning.set(True)
        
        # Buttons
        y += 40
        self.w.cancelButton = Button((20, y, 80, 20), "Cancel", callback=self.cancelCallback)
        self.w.okButton = Button((200, y, 80, 20), "OK", callback=self.okCallback)
        self.w.setDefaultButton(self.w.okButton)
        
    def okCallback(self, sender):
        """Handle OK button click"""
        y_options = ["top", "center", "bottom"]
        x_options = ["left", "center", "right"]
        
        options = {
            'y_position': y_options[self.w.yAxisPopup.get()],
            'x_position': x_options[self.w.xAxisPopup.get()],
            'relative_to_shapes': self.w.relativeToShapes.get(),
            'close_after_running': self.w.closeAfterRunning.get()
        }
        
        # Run the mirror function with the selected options
        mirror_anchor_with_options(options)
        
        if options['close_after_running']:
            self.w.close()
        
    def cancelCallback(self, sender):
        """Handle Cancel button click"""
        self.w.close()
        
    def show(self):
        """Show the dialog"""
        self.w.open()


def get_glyph_bounds(layer):
    """Get the left and right bounds of a glyph layer"""
    if layer.bounds:
        return layer.bounds.origin.x, layer.bounds.origin.x + layer.bounds.size.width
    return 0, layer.width


def mirror_anchor_with_options(options):
    """Mirror anchor with user-specified options"""
    
    # Check if we have a font open
    font = Glyphs.font
    if not font:
        print("No font open")
        return
    
    # Check if we have a glyph selected
    if not font.selectedLayers:
        print("No glyph selected")
        return
    
    current_layer = font.selectedLayers[0]
    current_glyph = current_layer.parent
    current_master = current_layer.associatedFontMaster
    
    # Check if we have an anchor selected
    selection = current_layer.selection
    selected_anchor = None
    
    for item in selection:
        if item.__class__.__name__ == "GSAnchor":
            selected_anchor = item
            break
    
    if not selected_anchor:
        print("No anchor selected")
        return
    
    anchor_name = selected_anchor.name
    anchor_pos = selected_anchor.position
    print(f"Mirroring anchor '{anchor_name}' from position ({anchor_pos.x}, {anchor_pos.y})")
    print(f"Options: {options}")
    
    # Get current layer bounds
    current_left, current_right = get_glyph_bounds(current_layer)
    current_bottom = current_layer.bounds.origin.y if current_layer.bounds else 0
    current_top = current_bottom + (current_layer.bounds.size.height if current_layer.bounds else 0)
    
    # Calculate the offset from the reference point in the current layer
    offset_x = 0
    offset_y = 0
    
    if options['relative_to_shapes']:
        # Calculate offset from the specified reference point on the shape bounds
        if options['x_position'] == 'left':
            ref_x = current_left
        elif options['x_position'] == 'right':
            ref_x = current_right
        else:  # center
            ref_x = (current_left + current_right) / 2
        
        if options['y_position'] == 'top':
            ref_y = current_top
        elif options['y_position'] == 'bottom':
            ref_y = current_bottom
        else:  # center
            ref_y = (current_top + current_bottom) / 2
        
        # Store offsets from reference point
        offset_x = anchor_pos.x - ref_x
        offset_y = anchor_pos.y - ref_y
        print(f"Reference point: ({ref_x}, {ref_y}), Offset: ({offset_x}, {offset_y})")
    
    # Apply to all other masters
    for master in font.masters:
        if master == current_master:
            continue
            
        target_layer = current_glyph.layers[master.id]
        if not target_layer:
            continue
        
        # Get target layer bounds
        target_left, target_right = get_glyph_bounds(target_layer)
        target_bottom = target_layer.bounds.origin.y if target_layer.bounds else 0
        target_top = target_bottom + (target_layer.bounds.size.height if target_layer.bounds else 0)
        
        if options['relative_to_shapes']:
            # Calculate new reference point in target layer
            if options['x_position'] == 'left':
                new_ref_x = target_left
            elif options['x_position'] == 'right':
                new_ref_x = target_right
            else:  # center
                new_ref_x = (target_left + target_right) / 2
            
            if options['y_position'] == 'top':
                new_ref_y = target_top
            elif options['y_position'] == 'bottom':
                new_ref_y = target_bottom
            else:  # center
                new_ref_y = (target_top + target_bottom) / 2
            
            # Apply offset from reference point
            new_x = new_ref_x + offset_x
            new_y = new_ref_y + offset_y
        else:
            # Just use the specified position directly on the shape bounds
            if options['x_position'] == 'left':
                new_x = target_left
            elif options['x_position'] == 'right':
                new_x = target_right
            else:  # center
                new_x = (target_left + target_right) / 2
            
            if options['y_position'] == 'top':
                new_y = target_top
            elif options['y_position'] == 'bottom':
                new_y = target_bottom
            else:  # center
                new_y = (target_top + target_bottom) / 2
        
        # Create new position
        try:
            from Foundation import NSPoint
            new_pos = NSPoint(new_x, new_y)
        except ImportError:
            class Point:
                def __init__(self, x, y):
                    self.x = x
                    self.y = y
            new_pos = Point(new_x, new_y)
        
        # Find or create anchor in target layer
        target_anchor = None
        for anchor in target_layer.anchors:
            if anchor.name == anchor_name:
                target_anchor = anchor
                break
        
        if not target_anchor:
            target_anchor = GSAnchor()
            target_anchor.name = anchor_name
            target_layer.anchors.append(target_anchor)
        
        target_anchor.position = new_pos
        print(f"Placed anchor in {master.name} at ({new_pos.x}, {new_pos.y})")


# Run the script
if __name__ == "__main__":
    # Check if we have a font open and anchor selected first
    font = Glyphs.font
    if not font:
        print("No font open")
    elif not font.selectedLayers:
        print("No glyph selected")
    else:
        current_layer = font.selectedLayers[0]
        selection = current_layer.selection
        selected_anchor = None
        
        for item in selection:
            if item.__class__.__name__ == "GSAnchor":
                selected_anchor = item
                break
        
        if not selected_anchor:
            print("No anchor selected")
        else:
            # Show the dialog
            dialog = MirrorAnchorDialog()
            dialog.show()
