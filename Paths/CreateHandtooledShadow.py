#MenuTitle: Create Handtool
#Created by Kyle Wayne Benson
# -*- coding: utf-8 -*-
__doc__="""
Create a handtool effect (inner shadow + border) for selected glyphs
"""

import vanilla
from vanilla import *
import GlyphsApp
from Foundation import NSClassFromString
from GlyphsApp import Glyphs, GSLayer, GSPath

class HandtoolEffect(object):
    def __init__(self):
        # Window 'self.w':
        windowWidth = 280
        windowHeight = 240
        windowWidthResize = 100
        windowHeightResize = 0
        self.w = vanilla.Window(
            (windowWidth, windowHeight),
            "Create Handtool Effect",
            minSize=(windowWidth, windowHeight),
            maxSize=(windowWidth + windowWidthResize, windowHeight + windowHeightResize),
            autosaveName="com.kylewaynebenson.HandtoolEffect.mainwindow"
        )
        
        # UI elements:
        YOffset = 10
        
        self.w.text_title = vanilla.TextBox((15, YOffset, -15, 30), 
            "Create handtool effect with inner shadow and border:", sizeStyle='small')
        
        YOffset += 35
        
        # Border size
        self.w.text_border = vanilla.TextBox((15, YOffset, 80, 20), "Border size:", sizeStyle='regular')
        self.w.borderSize = vanilla.EditText((100, YOffset, 60, 21), "10", sizeStyle='regular')
        
        YOffset += 30
        
        # Inner shadow settings
        self.w.text_shadow = vanilla.TextBox((15, YOffset, -15, 20), 
            "Inner shadow offset (units):", sizeStyle='small')
        
        YOffset += 25
        
        self.w.text_shadowX = vanilla.TextBox((15, YOffset, 20, 20), "X:", sizeStyle='regular')
        self.w.shadowX = vanilla.EditText((40, YOffset, 60, 21), "-40", sizeStyle='regular')
        
        self.w.text_shadowY = vanilla.TextBox((120, YOffset, 20, 20), "Y:", sizeStyle='regular')
        self.w.shadowY = vanilla.EditText((145, YOffset, 60, 21), "0", sizeStyle='regular')
        
        YOffset += 35
        
        # Checkboxes
        self.w.allMasters = vanilla.CheckBox((15, YOffset, 200, 20), "Apply to all masters", value=False)
        
        YOffset += 25

        # Run Button:
        self.w.runButton = vanilla.Button((-130, -20-15, -15, -15), "Create Handtool", 
            sizeStyle='regular', callback=self.HandtoolMain)
        self.w.setDefaultButton(self.w.runButton)

        # Open window and focus on it:
        self.w.open()
        self.w.makeKey()

    def HandtoolMain(self, sender):
        try:
            # Get OffsetCurve filter class
            offsetFilterClass = NSClassFromString("GlyphsFilterOffsetCurve")
            Font = Glyphs.font
            
            if not Font:
                Glyphs.showNotification("Handtool Effect", "No font open")
                return
            
            # Get parameters
            try:
                borderSize = float(self.w.borderSize.get())
                shadowX = float(self.w.shadowX.get())
                shadowY = float(self.w.shadowY.get())
            except ValueError:
                Glyphs.showNotification("Handtool Effect", "Invalid numeric values")
                return
            
            allMasters = self.w.allMasters.get()
            
            glyphsChanged = []
            
            # Determine which masters to process
            if allMasters:
                masters = Font.masters
            else:
                masters = [Font.selectedFontMaster]
            
            selectedGlyphs = set([layer.parent for layer in Font.selectedLayers if layer.parent])
            
            if not selectedGlyphs:
                Glyphs.showNotification("Handtool Effect", "No glyphs selected")
                return
            
            for glyph in selectedGlyphs:
                glyphsChanged.append(glyph.name)
                
                for master in masters:
                    srcLayer = glyph.layers[master.id]

                    if len(srcLayer.paths) == 0:
                        continue

                    # 1) Start with cleaned outline
                    baseLayer = srcLayer.copy()
                    baseLayer.removeOverlap()
                    baseLayer.correctPathDirection()

                    # Store cleaned paths
                    cleanPaths = [p.copy() for p in baseLayer.paths]
                    # count
                    numShapes = len(cleanPaths)

                    # 2) Create inset version for the shadow source
                    insetLayer = GSLayer()
                    for p in cleanPaths:
                        insetLayer.paths.append(p.copy())
                    
                    insetLayer.removeOverlap()
                    insetLayer.correctPathDirection()
                    # double to shrink inward
                    borderSizeDouble = borderSize * 2

                    # Apply offset filter using the class method
                    offsetFilterClass.offsetLayer_offsetX_offsetY_makeStroke_autoStroke_position_metrics_error_shadow_capStyleStart_capStyleEnd_keepCompatibleOutlines_(
                        insetLayer,
                        borderSizeDouble, borderSizeDouble,
                        True,  # makeStroke
                        False,  # autoStroke
                        0.5,  # position
                        None,  # metrics
                        None,  # error
                        None,  # shadow
                        0,  # capStyleStart
                        0,  # capStyleEnd
                        False  # keepCompatibleOutlines
                    )
                    
                    insetPaths = [p.copy() for p in insetLayer.paths]
                    
                    # Delete offset shapes
                    if len(insetPaths) > numShapes:
                        # Sort paths by area
                        pathAreas = [(p, abs(p.area())) for p in insetPaths]
                        pathAreas.sort(key=lambda x: x[1], reverse=False)
                        # The offset paths are the largest 'numShapes' areas
                        pathsToKeep = [p[0] for p in pathAreas[:numShapes]]
                        insetPaths = pathsToKeep

                    # Remove overlaps using a temporary layer
                    tempLayer = GSLayer()
                    for p in insetPaths:
                        tempLayer.paths.append(p.copy())
                    tempLayer.removeOverlap()
                    tempLayer.correctPathDirection()
                    insetPaths = [p.copy() for p in tempLayer.paths]

                    # 3) Create inner shadow by shifting the original shape
                    shadowLayer = GSLayer()
                    for p in cleanPaths:
                        shadowPath = p.copy()
                        for node in shadowPath.nodes:
                            node.position = (node.position.x + shadowX, node.position.y + shadowY)
                        shadowLayer.paths.append(shadowPath)

                    # 4) Crop shadow to the part offset shape
                    # Use the "big rectangle" method for clean boolean operations
                    # Get bounds of all paths to create a big rectangle
                    margin = 400
                    allNodes = []
                    for p in cleanPaths:
                        for node in p.nodes:
                            allNodes.append(node.position)
                    for p in shadowLayer.paths:
                        for node in p.nodes:
                            allNodes.append(node.position)
                    
                    if allNodes:
                        minX = min(n.x for n in allNodes) - margin
                        maxX = max(n.x for n in allNodes) + margin
                        minY = min(n.y for n in allNodes) - margin
                        maxY = max(n.y for n in allNodes) + margin
                        
                        # Create big rectangle (clockwise = filled)
                        from GlyphsApp import GSNode
                        bigRect = GSPath()
                        bigRect.closed = True
                        bigRect.nodes = [
                            GSNode((minX, minY)),
                            GSNode((maxX, minY)),
                            GSNode((maxX, maxY)),
                            GSNode((minX, maxY))
                        ]
                        
                        # Create mask layer: big rect + reversed original (original becomes a hole)
                        maskLayer = GSLayer()
                        maskLayer.paths.append(bigRect)
                        for p in insetPaths:
                            holePath = p.copy()
                            holePath.reverse()
                            maskLayer.paths.append(holePath)
                        maskLayer.removeOverlap()
                        maskLayer.correctPathDirection()
                        
                        # Intersect shadow with mask
                        visibleShadowLayer = GSLayer()
                        
                        # Add shadow
                        for p in shadowLayer.paths:
                            visibleShadowLayer.paths.append(p.copy())
                        
                        # Add mask
                        for p in maskLayer.paths:
                            visibleShadowLayer.paths.append(p.copy())
                        
                        # Union then subtract to get intersection
                        visibleShadowLayer.removeOverlap()
                        

                        # Now subtract the mask (reversed) to keep only shadow part
                        for p in maskLayer.paths:
                            cutPath = p.copy()
                            cutPath.reverse()
                            visibleShadowLayer.paths.append(cutPath)
                        
                        visibleShadowLayer.removeOverlap()
                        
                        innerShadowPaths = [p.copy() for p in visibleShadowLayer.paths]
                    else:
                        innerShadowPaths = []

                    # 5) Build final layer: original outline + visible shadow
                    finalLayer = GSLayer()
                    # Add inner shadow paths
                    for p in innerShadowPaths:
                        finalLayer.paths.append(p.copy())

                    # Add the original clean outline
                    for p in cleanPaths:
                        finalLayer.paths.append(p.copy())

                    finalLayer.correctPathDirection()
                    finalLayer.removeOverlap()
                    finalLayer.correctPathDirection()

                    # Copy attributes and replace layer
                    finalLayer.layerId = srcLayer.layerId
                    finalLayer.associatedMasterId = srcLayer.associatedMasterId
                    finalLayer.width = srcLayer.width
                    
                    glyph.layers[master.id] = finalLayer
            
            # Report results
            if glyphsChanged:
                print("Created handtool effect for: %s" % ", ".join(glyphsChanged))
                Glyphs.showNotification("Handtool Effect", "Applied to %d glyph(s)" % len(glyphsChanged))
                
        except Exception as e:
            # Print error
            Glyphs.showMacroWindow()
            print("Create Handtool Error: %s" % e)
            import traceback
            print(traceback.format_exc())

# Run the script
HandtoolEffect()