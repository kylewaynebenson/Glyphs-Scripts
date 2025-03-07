# MenuTitle: Reset Component Scales to 100%
# -*- coding: utf-8 -*-
__doc__="""
Resets the scale of all components in the selected glyph to 100% with options for all masters and automatic alignment.
"""

import GlyphsApp
from vanilla import *

class ResetComponentScalesDialog(object):

    def __init__(self):
        self.w = FloatingWindow((300, 150), "Reset Component Scales")
        self.w.allMasters = CheckBox((10, 10, -10, 20), "Across all masters", value=True)
        self.w.autoAlign = CheckBox((10, 40, -10, 20), "Enable automatic alignment", value=True)
        self.w.closeAfter = CheckBox((10, 70, -10, 20), "Close popup after running", value=True)
        self.w.resetButton = Button((10, 100, -10, 20), "Reset Scales", callback=self.resetScales)
        self.w.center()
        self.w.open()

    def resetScales(self, sender):
        font = Glyphs.font
        if not font:
            print("No font open")
            return
        
        selectedLayers = font.selectedLayers
        if not selectedLayers:
            print("No glyph selected")
            return
        
        allMasters = self.w.allMasters.get()
        autoAlign = self.w.autoAlign.get()
        
        for layer in selectedLayers:
            glyph = layer.parent
            print(f"Processing glyph: {glyph.name}")
            
            if allMasters:
                layers = [glyph.layers[m.id] for m in font.masters]
            else:
                layers = [layer]
            
            for l in layers:
                print(f"  Processing layer: {l.name}")
                for component in l.components:
                    initial_scale = component.scale
                    initial_alignment = component.automaticAlignment
                    
                    if component.scale != (1, 1):
                        print(f"    Resetting component {component.componentName}")
                        print(f"      Initial scale: {initial_scale}")
                        component.scale = (1, 1)
                        print(f"      New scale: {component.scale}")
                    
                    if autoAlign:
                        print(f"      Initial automatic alignment: {initial_alignment}")
                        component.automaticAlignment = True
                        print(f"      New automatic alignment: {component.automaticAlignment}")
                    
                    if component.scale != (1, 1) or (autoAlign and not component.automaticAlignment):
                        print(f"    Warning: Failed to update component {component.componentName}")
            
            glyph.updateGlyphInfo()

        font.enableUpdateInterface()
        print("Component scales reset complete")
        
        if self.w.closeAfter.get():
            self.w.close()

ResetComponentScalesDialog()