#MenuTitle: Set Spacing Groups
# -*- coding: utf-8 -*-
# Created by Kyle Wayne Benson December 10, 2017
__doc__="""
Set Spacing Groups to spacing.extension if .extension is added
"""

import GlyphsApp

Font = Glyphs.font
FontMaster = Font.selectedFontMaster
selectedLayers = Font.selectedLayers
selectedLayer = selectedLayers[0]
try:
	# until v2.1:
	selection = selectedLayer.selection()
except:
	# since v2.2:
	selection = selectedLayer.selection

def glyphExists(glyphName):
	return glyphName in Font.glyphs

Glyphs.showMacroWindow()
for thisLayer in selectedLayers:
	thisGlyph = thisLayer.parent
	try:
		thisGlyph.beginUndo()
		guideName = "spacing." + thisGlyph.name.rsplit('.', 2)[1]
		if glyphExists(guideName):
			thisGlyph.leftMetricsKey = guideName
			thisGlyph.rightMetricsKey = guideName
		thisGlyph.endUndo()
	except:
		print "!\t" + thisGlyph.name + "\t is not a special character and has not been changed"
