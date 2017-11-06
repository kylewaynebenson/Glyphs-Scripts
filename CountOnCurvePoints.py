#MenuTitle: Count On Curve Points
#Created by Kyle Wayne Benson
# -*- coding: utf-8 -*-
__doc__="""
Count and compare on curve points between masters
"""

import GlyphsApp

def countMyNodes( thisLayer):
	nodeTotal = 0
	for thisPath in thisLayer.paths:
		for thisNode in thisPath.nodes:
			if (thisNode.type == GSCURVE) or (thisNode.type == LINE):
				nodeTotal += 1
	return nodeTotal


font = Glyphs.font
# get active layer
layer = font.selectedLayers[0]
# get glyph of this layer
glyph = layer.parent

# access all layers of this glyph


try:
	Glyphs.showMacroWindow()
	for layer in glyph.layers:
	        print layer.name, ": ", countMyNodes( layer)

except Exception, e:
	# print error
	Glyphs.showMacroWindow()
	print "CountOnCurvePoints Error: %s" % e
