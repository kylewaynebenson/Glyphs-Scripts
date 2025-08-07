# MenuTitle: Mirror anchor across masters
# -*- coding: utf-8 -*-
__doc__="""
Takes a selected anchor and places it in corresponding positions 
across all masters based on positioning relative to zones and sides.
"""

import math
from vanilla import Window, PopUpButton, CheckBox, Button, TextBox

class MirrorAnchorDialog:
    """Dialog for mirror anchor settings"""
    
    def __init__(self):
        # Window setup
        self.w = Window((300, 200), "Mirror Anchor Settings", minSize=(300, 200))
        
        # Y-axis positioning dropdown
        y = 20
        self.w.yAxisLabel = TextBox((20, y, 100, 20), "Y-axis position:")
        self.w.yAxisPopup = PopUpButton((130, y, 150, 20), [
            "Baseline", "X-height", "Cap-height", "Center", "Ascender", "Descender", "Proportional"
        ])
        self.w.yAxisPopup.set(2)  # Default to Cap-height
        
        # X-axis positioning dropdown
        y += 30
        self.w.xAxisLabel = TextBox((20, y, 100, 20), "X-axis position:")
        self.w.xAxisPopup = PopUpButton((130, y, 150, 20), [
            "Left", "Center", "Right", "Proportional"
        ])
        self.w.xAxisPopup.set(1)  # Default to Center
        
        # Maintain relative distance checkbox
        y += 30
        self.w.maintainDistance = CheckBox((20, y, 260, 20), "Maintain relative distance from reference")
        self.w.maintainDistance.set(True)
        
        # Close after running checkbox
        y += 30
        self.w.closeAfterRunning = CheckBox((20, y, 200, 20), "Close after running")
        self.w.closeAfterRunning.set(True)
        
        # Buttons
        y += 40
        self.w.cancelButton = Button((20, y, 80, 20), "Cancel", callback=self.cancelCallback)
        self.w.okButton = Button((200, y, 80, 20), "OK", callback=self.okCallback)
        self.w.setDefaultButton(self.w.okButton)
        
        # Result storage
        self.result = None
        
    def okCallback(self, sender):
        """Handle OK button click"""
        y_options = ["baseline", "x-height", "cap-height", "center", "ascender", "descender", "proportional"]
        x_options = ["left", "center", "right", "proportional"]
        
        self.result = {
            'y_position': y_options[self.w.yAxisPopup.get()],
            'x_position': x_options[self.w.xAxisPopup.get()],
            'maintain_distance': self.w.maintainDistance.get(),
            'close_after_running': self.w.closeAfterRunning.get()
        }
        
        if self.result['close_after_running']:
            self.w.close()
        
        # Run the mirror function with the selected options
        mirror_anchor_with_options(self.result)
        
    def cancelCallback(self, sender):
        """Handle Cancel button click"""
        self.w.close()
        
    def show(self):
        """Show the dialog"""
        self.w.open()
from vanilla import Window, PopUpButton, CheckBox, Button, TextBox

def get_font_zones(master):
    """Get the key vertical zones for a master"""
    zones = {}
    zones['baseline'] = 0
    
    # Helper function to safely get a metric
    def get_metric(metric_name, default_value):
        try:
            # Try to get from master first
            value = getattr(master, metric_name, None)
            if value is not None:
                return value
        except:
            pass
        
        try:
            # Try to get from font's custom parameters
            value = master.font.customParameters[metric_name]
            if value is not None:
                return value
        except:
            pass
        
        # Fall back to default
        return default_value
    
    zones['x-height'] = get_metric('xHeight', 500)
    zones['cap-height'] = get_metric('capHeight', 700)
    zones['ascender'] = get_metric('ascender', 800)
    zones['descender'] = get_metric('descender', -200)
    
    return zones

def get_glyph_bounds(layer):
    """Get the left and right bounds of a glyph layer"""
    if layer.bounds:
        return layer.bounds.origin.x, layer.bounds.origin.x + layer.bounds.size.width
    return 0, layer.width

def is_near_zone(y_pos, zone_value, tolerance=10):
    """Check if a position is within tolerance of a zone"""
    return abs(y_pos - zone_value) <= tolerance

def is_near_side(x_pos, left_bound, right_bound, tolerance=10):
    """Check if a position is within tolerance of left or right side"""
    return abs(x_pos - left_bound) <= tolerance or abs(x_pos - right_bound) <= tolerance

def is_near_middle(pos, min_val, max_val, tolerance_percent=5):
    """Check if a position is within percentage tolerance of the middle"""
    middle = (min_val + max_val) / 2
    range_size = max_val - min_val
    tolerance = range_size * (tolerance_percent / 100.0)
    return abs(pos - middle) <= tolerance

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
    
    # Get reference measurements from current master
    current_zones = get_font_zones(current_master)
    current_left, current_right = get_glyph_bounds(current_layer)
    
    # Calculate reference distance if maintaining relative distance
    reference_distance = None
    if options['maintain_distance']:
        reference_distance = calculate_reference_distance(
            anchor_pos, options, current_zones, current_left, current_right, current_layer.width
        )
        print(f"Reference distance: {reference_distance}")
    
    # Apply to all other masters
    for master in font.masters:
        if master == current_master:
            continue
            
        target_layer = current_glyph.layers[master.id]
        if not target_layer:
            continue
            
        # Calculate new position based on options
        new_pos = calculate_new_position_with_options(
            options, master, target_layer, anchor_pos, reference_distance
        )
        
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

def calculate_reference_distance(anchor_pos, options, zones, left_bound, right_bound, glyph_width):
    """Calculate the reference distance from the anchor to the specified reference point"""
    
    # Calculate Y distance
    y_ref = get_y_reference_position(options['y_position'], zones)
    y_distance = anchor_pos.y - y_ref
    
    # Calculate X distance  
    x_ref = get_x_reference_position(options['x_position'], left_bound, right_bound, glyph_width)
    x_distance = anchor_pos.x - x_ref
    
    return {'x': x_distance, 'y': y_distance}

def get_y_reference_position(y_position, zones):
    """Get the Y coordinate for the specified reference position"""
    position_map = {
        'baseline': zones['baseline'],
        'x-height': zones['x-height'], 
        'cap-height': zones['cap-height'],
        'center': (zones['cap-height'] + zones['baseline']) / 2,
        'ascender': zones['ascender'],
        'descender': zones['descender']
    }
    return position_map.get(y_position, zones['baseline'])

def get_x_reference_position(x_position, left_bound, right_bound, glyph_width):
    """Get the X coordinate for the specified reference position"""
    if x_position == 'left':
        return left_bound
    elif x_position == 'right':
        return right_bound
    elif x_position == 'center':
        return (left_bound + right_bound) / 2
    else:  # proportional - use glyph center
        return glyph_width / 2

def calculate_new_position_with_options(options, target_master, target_layer, original_pos, reference_distance):
    """Calculate new anchor position based on user options"""
    
    target_zones = get_font_zones(target_master)
    target_left, target_right = get_glyph_bounds(target_layer)
    
    if options['maintain_distance'] and reference_distance:
        # Use relative distance from reference point
        y_ref = get_y_reference_position(options['y_position'], target_zones)
        x_ref = get_x_reference_position(options['x_position'], target_left, target_right, target_layer.width)
        
        new_y = y_ref + reference_distance['y']
        new_x = x_ref + reference_distance['x']
    else:
        # Use proportional positioning based on original analysis
        if options['y_position'] == 'proportional':
            # Use the original proportional logic
            ratio = original_pos.y / target_zones['cap-height'] if target_zones['cap-height'] != 0 else 0
            new_y = target_zones['cap-height'] * ratio
        else:
            new_y = get_y_reference_position(options['y_position'], target_zones)
        
        if options['x_position'] == 'proportional':
            # Use the original proportional logic  
            current_zones = get_font_zones(target_master)  # This might need the original master
            ratio = 0.5  # Default to center for proportional
            new_x = target_left + (target_right - target_left) * ratio
        else:
            new_x = get_x_reference_position(options['x_position'], target_left, target_right, target_layer.width)
    
    # Create a new point using the correct Glyphs constructor
    try:
        # Try NSPoint first (available in Glyphs environment)
        from Foundation import NSPoint
        return NSPoint(new_x, new_y)
    except ImportError:
        # Fallback: create a simple point object or use tuple
        class Point:
            def __init__(self, x, y):
                self.x = x
                self.y = y
        return Point(new_x, new_y)
def mirror_anchor():
    """Main function to mirror the selected anchor across masters (original function)"""
    
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
    
    # Get reference measurements from current master
    current_zones = get_font_zones(current_master)
    current_left, current_right = get_glyph_bounds(current_layer)
    current_width = current_right - current_left
    
    # Analyze anchor position relative to zones and bounds
    y_analysis = analyze_y_position(anchor_pos.y, current_zones)
    x_analysis = analyze_x_position(anchor_pos.x, current_left, current_right, current_layer.width)
    
    print(f"Y-axis analysis: {y_analysis}")
    print(f"X-axis analysis: {x_analysis}")
    
    # Apply to all other masters
    for master in font.masters:
        if master == current_master:
            continue
            
        target_layer = current_glyph.layers[master.id]
        if not target_layer:
            continue
            
        # Calculate new position based on analysis
        new_pos = calculate_new_position(
            x_analysis, y_analysis, 
            master, target_layer, 
            anchor_pos
        )
        
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
    
    # Get reference measurements from current master
    current_zones = get_font_zones(current_master)
    current_left, current_right = get_glyph_bounds(current_layer)
    current_width = current_right - current_left
    
    # Analyze anchor position relative to zones and bounds
    y_analysis = analyze_y_position(anchor_pos.y, current_zones)
    x_analysis = analyze_x_position(anchor_pos.x, current_left, current_right, current_layer.width)
    
    print(f"Y-axis analysis: {y_analysis}")
    print(f"X-axis analysis: {x_analysis}")
    
    # Apply to all other masters
    for master in font.masters:
        if master == current_master:
            continue
            
        target_layer = current_glyph.layers[master.id]
        if not target_layer:
            continue
            
        # Calculate new position based on analysis
        new_pos = calculate_new_position(
            x_analysis, y_analysis, 
            master, target_layer, 
            anchor_pos
        )
        
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

def analyze_y_position(y_pos, zones):
    """Analyze vertical position relative to font zones"""
    analysis = {}
    
    # Check proximity to each zone
    for zone_name, zone_value in zones.items():
        if is_near_zone(y_pos, zone_value):
            analysis['type'] = 'zone_relative'
            analysis['zone'] = zone_name
            analysis['offset'] = y_pos - zone_value
            return analysis
    
    # Check if it's in the middle between major zones
    cap_baseline_middle = (zones['cap-height'] + zones['baseline']) / 2
    if is_near_middle(y_pos, zones['baseline'], zones['cap-height']):
        analysis['type'] = 'middle'
        analysis['zone_pair'] = ('baseline', 'cap-height')
        return analysis
    
    xheight_baseline_middle = (zones['x-height'] + zones['baseline']) / 2
    if is_near_middle(y_pos, zones['baseline'], zones['x-height']):
        analysis['type'] = 'middle'
        analysis['zone_pair'] = ('baseline', 'x-height')
        return analysis
    
    # Default: use proportional positioning
    analysis['type'] = 'proportional'
    analysis['baseline_ratio'] = y_pos / zones['cap-height'] if zones['cap-height'] != 0 else 0
    return analysis

def analyze_x_position(x_pos, left_bound, right_bound, glyph_width):
    """Analyze horizontal position relative to glyph bounds"""
    analysis = {}
    
    # Check proximity to sides
    if is_near_side(x_pos, left_bound, right_bound):
        if abs(x_pos - left_bound) <= abs(x_pos - right_bound):
            analysis['type'] = 'side_relative'
            analysis['side'] = 'left'
            analysis['offset'] = x_pos - left_bound
        else:
            analysis['type'] = 'side_relative'
            analysis['side'] = 'right'
            analysis['offset'] = x_pos - right_bound
        return analysis
    
    # Check if it's in the middle horizontally
    if is_near_middle(x_pos, left_bound, right_bound):
        analysis['type'] = 'middle'
        return analysis
    
    # Check proximity to glyph width boundaries (for spacing)
    if is_near_side(x_pos, 0, glyph_width):
        if abs(x_pos - 0) <= abs(x_pos - glyph_width):
            analysis['type'] = 'width_relative'
            analysis['side'] = 'left'
            analysis['offset'] = x_pos
        else:
            analysis['type'] = 'width_relative'
            analysis['side'] = 'right'
            analysis['offset'] = x_pos - glyph_width
        return analysis
    
    # Default: use proportional positioning
    analysis['type'] = 'proportional'
    if right_bound != left_bound:
        analysis['ratio'] = (x_pos - left_bound) / (right_bound - left_bound)
    else:
        analysis['ratio'] = 0.5
    return analysis

def calculate_new_position(x_analysis, y_analysis, target_master, target_layer, original_pos):
    """Calculate new anchor position based on analysis"""
    
    # Calculate Y position
    target_zones = get_font_zones(target_master)
    
    if y_analysis['type'] == 'zone_relative':
        new_y = target_zones[y_analysis['zone']] + y_analysis['offset']
    elif y_analysis['type'] == 'middle':
        zone1, zone2 = y_analysis['zone_pair']
        new_y = (target_zones[zone1] + target_zones[zone2]) / 2
    else:  # proportional
        new_y = target_zones['cap-height'] * y_analysis['baseline_ratio']
    
    # Calculate X position
    target_left, target_right = get_glyph_bounds(target_layer)
    
    if x_analysis['type'] == 'side_relative':
        if x_analysis['side'] == 'left':
            new_x = target_left + x_analysis['offset']
        else:
            new_x = target_right + x_analysis['offset']
    elif x_analysis['type'] == 'width_relative':
        if x_analysis['side'] == 'left':
            new_x = x_analysis['offset']
        else:
            new_x = target_layer.width + x_analysis['offset']
    elif x_analysis['type'] == 'middle':
        new_x = (target_left + target_right) / 2
    else:  # proportional
        new_x = target_left + (target_right - target_left) * x_analysis['ratio']
    
    # Create a new point using the correct Glyphs constructor
    try:
        # Try NSPoint first (available in Glyphs environment)
        from Foundation import NSPoint
        return NSPoint(new_x, new_y)
    except ImportError:
        # Fallback: create a simple point object or use tuple
        class Point:
            def __init__(self, x, y):
                self.x = x
                self.y = y
        return Point(new_x, new_y)

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