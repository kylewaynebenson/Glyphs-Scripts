#MenuTitle: Add Local Guidelines
# -*- coding: utf-8 -*-
__doc__="""
Adds guidelines accross font based on guides found in various guide.extension glyphs
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


def addAndSelectGuideline( thisLayer, originPoint, angle ):
	"""Adds a guideline in thisLayer at originPoint, at angle."""
	try:
		myGuideline = GSGuideLine()
		myGuideline.position = originPoint
		myGuideline.angle = angle
		thisLayer.addGuideLine_( myGuideline )
		thisLayer.clearSelection()
		thisLayer.addSelection_( myGuideline )
		return True
	except Exception as e:
		print e
		return False

def bringBackGuidelines( thisGlyph ):
	"""Pulls the Guidline info from a glyph"""
	# try:
	# 	myGuideline = GSGuideLine()
	# 	myGuideline.position = originPoint
	# 	myGuideline.angle = angle
	# 	thisLayer.addGuideLine_( myGuideline )
	# 	thisLayer.clearSelection()
	# 	thisLayer.addSelection_( myGuideline )
	# 	return True
	# except Exception as e:
	# 	print e
	# 	return False

for thisLayer in selectedLayers:
	thisGlyph = thisLayer.parent
	if thisGlyph.name.find("guide."):
		# delete guidelines:
		thisGlyph.beginUndo()
		thisLayer.guideLines = []
		thisGlyph.endUndo()
	guideName = thisGlyph.name.rsplit('.', 1)[1]
	guideLineOriginGlyph = "guide." + guideName
	print guideLineOriginGlyph
	# guidelineOrigin = NSPoint( centerX, centerY )
	
	guidelineAngle = 0.0
	
	# thisGlyph.beginUndo()
	# if not addAndSelectGuideline( thisLayer, guidelineOrigin, guidelineAngle ):
	# 	print "Error: Could not add guideline."
	# thisGlyph.endUndo()
