#MenuTitle: Create Handtool
#Created by Kyle Wayne Benson
# -*- coding: utf-8 -*-
__doc__="""
Create a handtool effect (inner shadow + border) for selected glyphs
"""

import vanilla
from vanilla import *
import GlyphsApp
from GlyphsApp import Glyphs, GSLayer, GSPath, GSNode

class HandtoolEffect(object):
    def __init__(self):
        # Window 'self.w':
        windowWidth = 280
        windowHeight = 270
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
            "Thin stroke is a measure of the most narrow width of the existing glyph design:", sizeStyle='small')
        
        YOffset += 35
        
        # Thinnest part of letter
        self.w.text_thinnest = vanilla.TextBox((15, YOffset, 100, 20), "Thin stroke:", sizeStyle='regular')
        self.w.thinnestPart = vanilla.EditText((180, YOffset, 60, 21), "5", sizeStyle='regular')

        YOffset += 30

        # Inner shadow settings
        self.w.text_export = vanilla.TextBox((15, YOffset, -15, 20), 
            "These relate to the final handtooled look:", sizeStyle='small')
        
        YOffset += 25

        # Border size
        self.w.text_border = vanilla.TextBox((15, YOffset, 80, 20), "Border size:", sizeStyle='regular')
        self.w.borderSize = vanilla.EditText((180, YOffset, 60, 21), "10", sizeStyle='regular')
        
        YOffset += 35

        self.w.text_shadow = vanilla.TextBox((15, YOffset, 80, 20), "Shadow:", sizeStyle='regular')
        self.w.text_shadowX = vanilla.TextBox((100, YOffset, 20, 20), "X:", sizeStyle='regular')
        self.w.shadowX = vanilla.EditText((125, YOffset, 40, 21), "-40", sizeStyle='regular')

        self.w.text_shadowY = vanilla.TextBox((170, YOffset, 20, 20), "Y:", sizeStyle='regular')
        self.w.shadowY = vanilla.EditText((195, YOffset, 40, 21), "0", sizeStyle='regular')

        YOffset += 30
        
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
    
    def applyOffsetToPaths(self, paths, offsetValue):
        """Apply offset to paths and return new paths"""
        import objc
        OffsetCurveFilter = objc.lookUpClass("GlyphsFilterOffsetCurve")
        
        newPaths = []
        for path in paths:
            # offsetPath returns a list of new paths
            result = OffsetCurveFilter.offsetPath_offsetX_offsetY_makeStroke_position_objects_capStyleStart_capStyleEnd_(
                path, 
                offsetValue, 
                offsetValue, 
                False,  # makeStroke = False for pure offset
                0.5,    # position
                False,  # objects
                0,      # capStyleStart
                0       # capStyleEnd
            )
            if result:
                for newPath in result:
                    newPaths.append(newPath)
        
        return newPaths

    def HandtoolMain(self, sender):
        try:
            Font = Glyphs.font
            
            if not Font:
                Glyphs.showNotification("Handtool Effect", "No font open")
                return
            
            # Get parameters
            try:
                borderSize = float(self.w.borderSize.get())
                shadowX = float(self.w.shadowX.get())
                shadowY = float(self.w.shadowY.get())
                thinnestPart = float(self.w.thinnestPart.get())
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

                    # Store cleaned paths (keep original clean for final outline)
                    cleanPaths = [p.copy() for p in baseLayer.paths]

                    # 2) Create inset version for the shadow boundary
                    # First, smooth out thin parts using thinnestPart value
                    print("Smoothing thin parts for inset: offset in by %f, then out by %f" % (thinnestPart, thinnestPart))
                    
                    thinnestPart = thinnestPart / 2.0
                    # Start with clean paths for smoothing
                    smoothPaths = self.applyOffsetToPaths(cleanPaths, -thinnestPart)
                    
                    # Create temp layer for cleanup
                    tempLayer = GSLayer()
                    for p in smoothPaths:
                        tempLayer.paths.append(p)
                    tempLayer.removeOverlap()
                    tempLayer.correctPathDirection()
                    smoothPaths = [p.copy() for p in tempLayer.paths]
                    
                    # Then offset outward by thinnestPart to restore size
                    smoothPaths = self.applyOffsetToPaths(smoothPaths, thinnestPart)
                    
                    # Create temp layer for final cleanup
                    tempLayer2 = GSLayer()
                    for p in smoothPaths:
                        tempLayer2.paths.append(p)
                    tempLayer2.removeOverlap()
                    tempLayer2.correctPathDirection()
                    smoothedPaths = [p.copy() for p in tempLayer2.paths]
                    
                    # Now apply the actual border inset to the smoothed paths
                    insetLayer = GSLayer()
                    
                    # Apply offset to the smoothed paths
                    insetValue = -borderSize
                    print("Applying inset offset: %f" % insetValue)
                    
                    insetPaths = self.applyOffsetToPaths(smoothedPaths, insetValue)
                    
                    # Add the offset paths to the layer
                    for p in insetPaths:
                        insetLayer.paths.append(p)
                    
                    insetLayer.removeOverlap()
                    insetLayer.correctPathDirection()
                    # Update insetPaths with the final cleaned paths
                    insetPaths = [p.copy() for p in insetLayer.paths]

                    # 3) Create inner shadow by shifting the original shape
                    shadowLayer = GSLayer()
                    for p in cleanPaths:
                        shadowPath = p.copy()
                        for node in shadowPath.nodes:
                            node.position = (node.position.x + shadowX, node.position.y + shadowY)
                        shadowLayer.paths.append(shadowPath)

                    # 4) Crop shadow to the part between original and inset
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
                        bigRect = GSPath()
                        bigRect.closed = True
                        bigRect.nodes = [
                            GSNode((minX, minY)),
                            GSNode((maxX, minY)),
                            GSNode((maxX, maxY)),
                            GSNode((minX, maxY))
                        ]
                        
                        # Create mask layer: big rect + reversed inset (inset becomes a hole)
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