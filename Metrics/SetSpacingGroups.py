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
		extension = thisGlyph.name.rsplit('.', 2)[1]
		leftGuideName = "_space." + extension[:3]
		rightGuideName = "_space." + extension[-3:]
		if "=_space." not in str(thisGlyph.leftMetricsKey):
			if (leftGuideName != thisGlyph.name):
				if glyphExists(leftGuideName):
					thisGlyph.color = 7 # change color dark blue
					thisGlyph.leftMetricsKey = leftGuideName
		else:
			print( "!\t" + thisGlyph.name + "\t has _space formula LSB")
		if "=_space." not in str(thisGlyph.rightMetricsKey):
			if (rightGuideName != thisGlyph.name):				
				if glyphExists(rightGuideName):
					thisGlyph.color = 8 # change color purple
					thisGlyph.rightMetricsKey = rightGuideName
				if (glyphExists(leftGuideName) & glyphExists(rightGuideName)):
					thisGlyph.color = 9 # change color magenta
		else:
			print( "!\t" + thisGlyph.name + "\t has _space formula RSB")
		thisGlyph.endUndo()
	except:
		print( "!\t" + thisGlyph.name + "\t is not special")
