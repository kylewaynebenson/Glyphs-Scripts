#MenuTitle: Char Width to 725 Centered
# Created by Kyle Benson
# -*- coding: utf-8 -*-
__doc__="""
Uniformly change width in all layers but keep character centered"""

NewWidth = 725

Glyphs.clearLog()
Glyphs.showMacroWindow()
NewWidth = 725
for layer in Glyphs.font.selectedLayers:
	thisGlyph = layer.parent
	print "\n", thisGlyph.name
	allLayers = len(thisGlyph.layers)
	count = 0
	for thisLayer in thisGlyph.layers:
		AddToSides = (NewWidth - thisLayer.width) / 2
		print "\t", thisLayer.name
		print "\t", "\t", "Current Width =>", thisLayer.width
		print "\t", "\t", "Added to Sides =>", AddToSides
		thisLayer.LSB = thisLayer.LSB + AddToSides
		thisLayer.RSB = thisLayer.RSB + AddToSides
		print "\t", "\t", "New Width =>", thisLayer.width
	if count == allLayers:
		thisGlyph.color = 6
