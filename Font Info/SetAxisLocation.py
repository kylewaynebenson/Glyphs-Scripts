# MenuTitle: Set Axis Location
# -*- coding: utf-8 -*-
__doc__ = """
Sets the axis location custom parameter in all active instances.
Optionally includes inactive instances and can use weight/width classes instead of axis coordinates.
"""

import vanilla
from GlyphsApp import Glyphs

class SetAxisLocationDialog:
    """Dialog for setting axis location parameters"""
    
    def __init__(self):
        # Default preferences
        self.preferences = {
            "includeInactive": False,
            "setWidthByClass": False,
            "setWeightByClass": False,
        }
        
        # Window setup
        self.w = vanilla.Window((320, 200), "Set Axis Location", minSize=(320, 200))
        
        # Checkboxes
        y = 20
        self.w.includeInactive = vanilla.CheckBox((20, y, 280, 20), "Include inactive instances", 
                                                  value=self.preferences["includeInactive"], 
                                                  callback=self.savePreferences)
        
        y += 30
        self.w.setWidthByClass = vanilla.CheckBox((20, y, 280, 20), "Set width using width class", 
                                                  value=self.preferences["setWidthByClass"], 
                                                  callback=self.savePreferences)
        
        y += 30
        self.w.setWeightByClass = vanilla.CheckBox((20, y, 280, 20), "Set weight using weight class", 
                                                   value=self.preferences["setWeightByClass"], 
                                                   callback=self.savePreferences)
        
        # Info text
        y += 40
        self.w.infoText = vanilla.TextBox((20, y, 280, 60), 
                                          "If weight/width class options are unchecked, "
                                          "the script will use the axis coordinates set in each instance.",
                                          sizeStyle="small")
        
        # Buttons
        y += 70
        self.w.cancelButton = vanilla.Button((20, y, 80, 20), "Cancel", callback=self.cancelCallback)
        self.w.runButton = vanilla.Button((220, y, 80, 20), "Set Locations", callback=self.runCallback)
        self.w.setDefaultButton(self.w.runButton)
        
        # Open window and focus on it
        self.w.open()
        self.w.makeKey()
    
    def savePreferences(self, sender=None):
        """Save current UI state to preferences"""
        self.preferences["includeInactive"] = self.w.includeInactive.get()
        self.preferences["setWidthByClass"] = self.w.setWidthByClass.get()
        self.preferences["setWeightByClass"] = self.w.setWeightByClass.get()
    
    def cancelCallback(self, sender):
        """Handle Cancel button click"""
        self.w.close()
    
    def runCallback(self, sender):
        """Handle Run button click"""
        # Update preferences
        self.savePreferences()
        
        # Run the main function
        set_axis_locations(self.preferences)
        
        # Close dialog
        self.w.close()

def set_axis_locations(options):
    """Set axis location custom parameters based on options"""
    
    # Check if we have a font open
    font = Glyphs.font
    if not font:
        print("No font open")
        return
    
    if not font.instances:
        print("No instances found in font")
        return
    
    print(f"Setting axis locations with options: {options}")
    
    # Get instances to process
    if options["includeInactive"]:
        instances_to_process = font.instances
        print(f"Processing all {len(font.instances)} instances (including inactive)")
    else:
        instances_to_process = [instance for instance in font.instances if instance.active]
        print(f"Processing {len(instances_to_process)} active instances")
    
    if not instances_to_process:
        print("No instances to process")
        return
    
    # Process each instance
    for instance in instances_to_process:
        axis_locations = []
        
        # Process each axis in the font
        for i, axis in enumerate(font.axes):
            axis_name = axis.name
            axis_tag = axis.axisTag
            
            # Determine the value to use for this axis
            if axis_tag == "wght" and options["setWeightByClass"]:
                # Use weight class
                weight_value = get_weight_from_class(instance.weightClass)
                axis_locations.append(create_axis_location_entry(axis_name, weight_value))
                print(f"  {instance.name}: {axis_name} = {weight_value} (from weight class {instance.weightClass})")
                
            elif axis_tag == "wdth" and options["setWidthByClass"]:
                # Use width class
                width_value = get_width_from_class(instance.widthClass)
                axis_locations.append(create_axis_location_entry(axis_name, width_value))
                print(f"  {instance.name}: {axis_name} = {width_value} (from width class {instance.widthClass})")
                
            else:
                # Use axis coordinates from instance
                try:
                    coord_value = instance.coordinateForAxisIndex_(i)
                    axis_locations.append(create_axis_location_entry(axis_name, coord_value))
                    print(f"  {instance.name}: {axis_name} = {coord_value} (from axis coordinates)")
                except Exception as e:
                    print(f"  Error getting axis value for {instance.name}, {axis_name}: {e}")
        
        # Set the axis location parameter
        if axis_locations:
            instance.customParameters["Axis Location"] = tuple(axis_locations)
            print(f"  Set Axis Location for {instance.name}")
        else:
            print(f"  No axis location set for {instance.name} (no valid values found)")
    
    print("Axis location setting completed!")

def create_axis_location_entry(axis_name, location_value):
    """Create an axis location entry dictionary"""
    from Foundation import NSDictionary
    return NSDictionary.alloc().initWithObjects_forKeys_((axis_name, location_value), ("Axis", "Location"))

def get_weight_from_class(weight_class):
    """Convert weight class to weight axis value"""
    # Standard weight class to weight axis mapping
    weight_mapping = {
        100: 100,   # Thin
        200: 200,   # Extra Light
        300: 300,   # Light
        400: 400,   # Regular
        500: 500,   # Medium
        600: 600,   # Semi Bold
        700: 700,   # Bold
        800: 800,   # Extra Bold
        900: 900,   # Black
    }
    
    return weight_mapping.get(weight_class, weight_class)

def get_width_from_class(width_class):
    """Convert width class to width axis value"""
    # Standard width class to width axis percentage mapping
    width_mapping = {
        1: 50,    # Ultra Condensed
        2: 62.5,  # Extra Condensed
        3: 75,    # Condensed
        4: 87.5,  # Semi Condensed
        5: 100,   # Normal
        6: 112.5, # Semi Expanded
        7: 125,   # Expanded
        8: 150,   # Extra Expanded
        9: 200,   # Ultra Expanded
    }
    
    return width_mapping.get(width_class, 100)

# Run the script
if __name__ == "__main__":
    # Check if we have a font open
    font = Glyphs.font
    if not font:
        print("No font open")
    else:
        # Show the dialog
        dialog = SetAxisLocationDialog()