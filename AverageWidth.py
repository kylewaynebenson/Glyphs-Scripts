#MenuTitle: Average Width
#Created by Kyle Wayne Benson
# -*- coding: utf-8 -*-
__doc__="""
Figure out the average width of selected glyphs in a layer
"""

import vanilla
import GlyphsApp


def averageWidth():
	Glyphs.clearLog()
	Glyphs.showMacroWindow()
	try:
		averageWidth = 0
		count = 0
		for layer in Glyphs.font.selectedLayers:
			thisGlyph = layer.parent
			averageWidth += layer.width
			count += 1
			print "\t", thisGlyph.name
			print "\t" "Width =>", layer.width
		averageWidth = averageWidth/count
		print "Average Width =>", averageWidth

	except Exception, e:
		# print error
		Glyphs.showMacroWindow()
		print "Change Width Centered Error: %s" % e

averageWidth()
