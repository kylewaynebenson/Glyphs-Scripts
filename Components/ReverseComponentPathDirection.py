# MenuTitle: Reverse Component Path Direction
# Description: Reverses the path direction of a selected component.
# -*- coding: utf-8 -*-

import vanilla
import GlyphsApp

class ReverseComponentPathDirection(object):
    def __init__(self):
        # Window dimensions
        width = 300
        height = 150

        # Create window
        self.w = vanilla.Window((width, height), "Reverse Component Path Direction")
        
        # Checkboxes
        self.w.applyAllMasters = vanilla.CheckBox((10, 20, -10, 25), "Apply on all masters")
        self.w.closeAfterRun = vanilla.CheckBox((10, 50, -10, 25), "Close popup after running")
        self.w.closeAfterRun.set(True)  # Default checked
        
        # Run button
        self.w.runButton = vanilla.Button((10, 80, -10, 30), "Reverse Path Direction", self.reversePathDirection)
        
        # Open window
        self.w.open()

    def reversePathDirection(self, sender):
        font = Glyphs.font
        selectedLayers = font.selectedLayers

        for layer in selectedLayers:
            component = next((c for c in layer.components if c.selected), None)
            if component:
                # Toggle the orientation property (-1 or 1)
                component.attributes['reversePaths'] = False if component.attributes['reversePaths'] == True else True
                
                # Apply to all masters if checkbox is checked
                if self.w.applyAllMasters.get():
                    for masterLayer in font.glyphs[layer.parent.name].layers:
                        for masterComponent in masterLayer.components:
                            if masterComponent.name == component.name:
                                masterComponent.attributes['reversePaths'] = False if masterComponent.attributes['reversePaths'] == True else True
        
        # Close window if checkbox is checked
        if self.w.closeAfterRun.get():
            self.w.close()

ReverseComponentPathDirection()
