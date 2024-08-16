# MenuTitle: Mirror Components Across Masters
# -*- coding: utf-8 -*-
__doc__="""
Mirrors the components of the active layer to all other masters, updating any discrepancies.
"""

import GlyphsApp
from vanilla import *

class MirrorComponentsAcrossMastersDialog(object):

    def __init__(self):
        self.w = FloatingWindow((300, 130), "Mirror Components Across Masters")
        self.w.infoText = TextBox((10, 10, -10, 44), "This script will update components in all masters to match the active layer.")
        self.w.closeAfter = CheckBox((10, 60, -10, 20), "Close popup after running", value=True)
        self.w.mirrorButton = Button((10, 90, -10, 20), "Mirror Components", callback=self.mirrorComponents)
        self.w.center()
        self.w.open()

    def mirrorComponents(self, sender):
        font = Glyphs.font
        if not font:
            print("No font open")
            return
        
        selectedLayers = font.selectedLayers
        if not selectedLayers:
            print("No glyph selected")
            return
        
        for activeLayer in selectedLayers:
            glyph = activeLayer.parent
            print(f"Processing glyph: {glyph.name}")
            print(f"Active layer: {activeLayer.name}")
            
            # Get the components of the active layer
            activeComponents = [shape for shape in activeLayer.shapes if isinstance(shape, GSComponent)]
            print(f"Active layer has {len(activeComponents)} components:")
            for i, comp in enumerate(activeComponents):
                print(f"  Component {i+1}: {comp.componentName} at position {comp.position}")
            
            for master in font.masters:
                if master.id == activeLayer.master.id:
                    print(f"Skipping active master: {master.name}")
                    continue  # Skip the active master
                
                layer = glyph.layers[master.id]
                print(f"Processing master: {master.name}")
                
                # Log existing components
                existingComponents = [shape for shape in layer.shapes if isinstance(shape, GSComponent)]
                print(f"  Before: Layer has {len(existingComponents)} components")
                
                # Remove all existing shapes (including components)
                layer.shapes = []
                print("  Removed all existing shapes")
                
                # Copy components from active layer
                for comp in activeComponents:
                    newComp = comp.copy()
                    layer.shapes.append(newComp)
                    print(f"  Added component: {newComp.componentName} at position {newComp.position}")
                
                print(f"  After: Layer now has {len(layer.shapes)} shapes")
            
            glyph.updateGlyphInfo()

        font.enableUpdateInterface()
        print("Mirroring components complete")
        
        if self.w.closeAfter.get():
            self.w.close()

MirrorComponentsAcrossMastersDialog()