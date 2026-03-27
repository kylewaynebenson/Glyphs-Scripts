#MenuTitle: Enable Automatic Alignment
#Created by Kyle Wayne Benson
# -*- coding: utf-8 -*-
__doc__="""
Enable automatic alignment for all components in selected glyphs across all layers.
"""

import vanilla
from GlyphsApp import Glyphs

class EnableAutomaticAlignment(object):
    def __init__(self):
        # Window
        windowWidth = 280
        windowHeight = 100
        self.w = vanilla.Window(
            (windowWidth, windowHeight),
            "Enable Automatic Alignment",
            minSize=(windowWidth, windowHeight),
            maxSize=(windowWidth, windowHeight),
            autosaveName="com.kylewaynebenson.EnableAutomaticAlignment.mainwindow"
        )
        
        # UI elements
        YOffset = 15
        
        self.w.text_info = vanilla.TextBox((15, YOffset, -15, 20), 
            "Enable alignment for selected glyphs:", sizeStyle='regular')
        
        YOffset += 30
        
        # Checkbox for close after running
        self.w.closeAfterRun = vanilla.CheckBox((15, YOffset, 200, 20), 
            "Close window after running", value=True)
        
        YOffset += 30
        
        # Run Button
        self.w.runButton = vanilla.Button((-130, -20-15, -15, -15), "Enable Alignment", 
            sizeStyle='regular', callback=self.enableAlignment)
        self.w.setDefaultButton(self.w.runButton)
        
        # Open window
        self.w.open()
        self.w.makeKey()
    
    def enableAlignment(self, sender):
        try:
            Font = Glyphs.font
            
            if not Font:
                Glyphs.showNotification("Enable Alignment", "No font open")
                return
            
            selectedGlyphs = set([layer.parent for layer in Font.selectedLayers if layer.parent])
            
            if not selectedGlyphs:
                Glyphs.showNotification("Enable Alignment", "No glyphs selected")
                return
            
            glyphsChanged = []
            componentsChanged = 0
            
            for glyph in selectedGlyphs:
                glyphModified = False
                
                # Process all layers of the glyph
                for layer in glyph.layers:
                    # Enable automatic alignment for all components in this layer
                    for component in layer.components:
                        if not component.automaticAlignment:
                            component.automaticAlignment = True
                            componentsChanged += 1
                            glyphModified = True
                
                if glyphModified:
                    glyphsChanged.append(glyph.name)
            
            # Report results
            if glyphsChanged:
                print("Enabled automatic alignment for: %s" % ", ".join(glyphsChanged))
                print("Total components changed: %d" % componentsChanged)
                Glyphs.showNotification("Enable Alignment", 
                    "Enabled alignment for %d component(s) in %d glyph(s)" % (componentsChanged, len(glyphsChanged)))
            else:
                Glyphs.showNotification("Enable Alignment", "All components already aligned")
            
            # Close window if checkbox is checked
            if self.w.closeAfterRun.get():
                self.w.close()
                
        except Exception as e:
            Glyphs.showMacroWindow()
            print("Enable Alignment Error: %s" % e)
            import traceback
            print(traceback.format_exc())

# Run the script
EnableAutomaticAlignment()
