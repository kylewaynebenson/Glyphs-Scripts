#MenuTitle: Delete X Path
#Created by Kyle Wayne Benson
# -*- coding: utf-8 -*-
__doc__="""
Finds and deletes a specific path, with the option to delete across all masters.
"""

from AppKit import NSMutableIndexSet
import GlyphsApp
from vanilla import Window, PopUpButton, CheckBox, Button, TextBox

class DeletePathDialog:
    """Dialog for delete path settings"""
    
    def __init__(self):
        # Window setup
        self.w = Window((300, 180), "Delete Path Settings", minSize=(300, 180))
        
        # Path selection dropdown
        y = 20
        self.w.pathLabel = TextBox((20, y, 100, 20), "Which path:")
        self.w.pathPopup = PopUpButton((130, y, 150, 20), [
            "Selected", "Smallest", "Largest", "First", "Last", "Second", "Third", "Fourth", "Fifth", "Sixth"
        ])
        self.w.pathPopup.set(0)  # Default to Selected
        
        # Delete across all masters checkbox
        y += 30
        self.w.allMasters = CheckBox((20, y, 260, 20), "Delete across all masters")
        self.w.allMasters.set(False)
        
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
        path_options = ["selected", "smallest", "largest", "first", "last", "second", "third", "fourth", "fifth", "sixth"]
        
        self.result = {
            'path_type': path_options[self.w.pathPopup.get()],
            'all_masters': self.w.allMasters.get(),
            'close_after_running': self.w.closeAfterRunning.get()
        }
        
        if self.result['close_after_running']:
            self.w.close()
        
        # Run the delete function with the selected options
        delete_path_with_options(self.result)
        
    def cancelCallback(self, sender):
        """Handle Cancel button click"""
        self.w.close()
        
    def show(self):
        """Show the dialog"""
        self.w.open()
thisFont = Glyphs.font # frontmost font
thisFontMaster = thisFont.selectedFontMaster # active master
listOfSelectedLayers = thisFont.selectedLayers # active layers of selected glyphs

def delete_path_with_options(options):
    """Delete paths with user-specified options"""
    
    # Check if we have a font open
    font = Glyphs.font
    if not font:
        print("No font open")
        return
    
    # Check if we have glyphs selected
    if not font.selectedLayers:
        print("No glyphs selected")
        return
    
    print(f"Deleting {options['path_type']} path(s)")
    print(f"Options: {options}")
    
    font.disableUpdateInterface() # suppresses UI updates in Font View
    
    for layer in font.selectedLayers:
        glyph = layer.parent
        glyph.beginUndo() # begin undo grouping
        
        # For "selected" mode, get the selected path index from the current layer
        selected_path_index = None
        if options['path_type'] == 'selected':
            selected_path_index = get_selected_path_index(layer)
            if selected_path_index is None:
                print(f"No path selected in {glyph.name}")
                glyph.endUndo()
                continue
        
        if options['all_masters']:
            # Delete from all masters
            for master in font.masters:
                target_layer = glyph.layers[master.id]
                if target_layer and target_layer.paths:
                    if options['path_type'] == 'selected':
                        # Use the same path index across all masters
                        delete_path_by_index(target_layer, selected_path_index)
                    else:
                        delete_specific_path(target_layer, options['path_type'])
        else:
            # Delete only from current layer
            if layer.paths:
                if options['path_type'] == 'selected':
                    delete_path_by_index(layer, selected_path_index)
                else:
                    delete_specific_path(layer, options['path_type'])
        
        glyph.endUndo() # end undo grouping
    
    font.enableUpdateInterface() # re-enables UI updates in Font View

def get_selected_path_index(layer):
    """Get the index of the currently selected path"""
    if not layer.paths:
        return None
    
    # Check if there's a selection
    if not layer.selection:
        return None
    
    # Find which path contains the selected nodes
    for i, path in enumerate(layer.paths):
        for node in path.nodes:
            if node in layer.selection:
                return i
    
    return None

def delete_path_by_index(layer, path_index):
    """Delete a path at a specific index (from layer.paths)"""
    if not layer.paths or path_index is None:
        return
    
    if path_index < 0 or path_index >= len(layer.paths):
        print(f"Path index {path_index} out of range (layer has {len(layer.paths)} paths)")
        return
    
    if Glyphs.versionNumber >= 3:
        # Glyphs 3 code - need to find the shape index that corresponds to this path index
        target_path = layer.paths[path_index]
        shape_index = None
        
        for i, shape in enumerate(layer.shapes):
            if hasattr(shape, 'nodes') and shape == target_path:
                shape_index = i
                break
        
        if shape_index is not None:
            pathsToBeRemoved = NSMutableIndexSet.alloc().init()
            pathsToBeRemoved.addIndex_(shape_index)
            layer.removeShapesAtIndexes_(pathsToBeRemoved)
        else:
            print(f"Could not find shape index for path {path_index}")
    else:
        # Glyphs 2 code
        layer.removePathAtIndex_(path_index)

def delete_specific_path(layer, path_type):
    """Delete a specific path based on the criteria"""
    
    if not layer.paths:
        print(f"No paths to delete in layer")
        return
    
    path_to_delete_index = get_path_index_to_delete(layer, path_type)
    
    if path_to_delete_index is None:
        print(f"Could not find {path_type} path to delete")
        return
    
    if Glyphs.versionNumber >= 3:
        # Glyphs 3 code
        pathsToBeRemoved = NSMutableIndexSet.alloc().init()
        pathsToBeRemoved.addIndex_(path_to_delete_index)
        layer.removeShapesAtIndexes_(pathsToBeRemoved)
    else:
        # Glyphs 2 code
        layer.removePathAtIndex_(path_to_delete_index)

def get_path_index_to_delete(layer, path_type):
    """Get the index of the path to delete based on criteria"""
    
    if not layer.paths:
        return None
    
    num_paths = len(layer.paths)
    
    if path_type == "smallest":
        areas = [path.area() for path in layer.paths]
        min_area = min(areas)
        return areas.index(min_area)
    
    elif path_type == "largest":
        areas = [path.area() for path in layer.paths]
        max_area = max(areas)
        return areas.index(max_area)
    
    elif path_type == "first":
        return 0
    
    elif path_type == "last":
        return num_paths - 1
    
    elif path_type == "second":
        return 1 if num_paths > 1 else None
    
    elif path_type == "third":
        return 2 if num_paths > 2 else None
    
    elif path_type == "fourth":
        return 3 if num_paths > 3 else None
    
    elif path_type == "fifth":
        return 4 if num_paths > 4 else None
    
    elif path_type == "sixth":
        return 5 if num_paths > 5 else None
    
    return None

def deleteLargestPath( thisLayer ):
	"""Original function - kept for backward compatibility"""
	layerarea = []
	for thisPath in thisLayer.paths:
		layerarea.append(thisPath.area())
	if Glyphs.versionNumber >= 3:
		# Glyphs 3 code
		pathsToBeRemoved = NSMutableIndexSet.alloc().init()

		for i, thisPath in enumerate(thisLayer.shapes) :
			if thisPath.area() == min(layerarea):
				pathsToBeRemoved.addIndex_( i )

		thisLayer.removeShapesAtIndexes_( pathsToBeRemoved )
	else:
		# Glyphs 2 code
		indexesOfPathsToBeRemoved = []

		numberOfPaths = len(thisLayer.paths)
		for thisPathNumber in range( numberOfPaths ):
			if thisPathNumber < (numberOfPaths - 1):
				thisPath = thisLayer.paths[thisPathNumber]
				if thisPath.area() == min(layerarea):
					indexesOfPathsToBeRemoved.append( thisPathNumber )
		
		if indexesOfPathsToBeRemoved:
			for thatIndex in reversed( sorted( indexesOfPathsToBeRemoved )):
				thisLayer.removePathAtIndex_( thatIndex )

# Run the script
if __name__ == "__main__":
    # Check if we have a font open and glyphs selected first
    font = Glyphs.font
    if not font:
        print("No font open")
    elif not font.selectedLayers:
        print("No glyphs selected")
    else:
        # Show the dialog
        dialog = DeletePathDialog()
        dialog.show()