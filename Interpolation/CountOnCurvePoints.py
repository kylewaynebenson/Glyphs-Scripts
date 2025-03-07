#MenuTitle: Count On Curve Points
#Created by Kyle Wayne Benson
# -*- coding: utf-8 -*-
__doc__="""
Count and compare on curve points between layers
"""
import vanilla.dialogs as vd
import GlyphsApp

def countMyNodes( thisLayer):
	nodeTotal = 0
	for thisPath in thisLayer.paths:
		for thisNode in thisPath.nodes:
			if (thisNode.type == GSCURVE) or (thisNode.type == LINE):
				nodeTotal += 1
	return nodeTotal

try:
	font = Glyphs.font
	# get active layer
	layer = font.selectedLayers[0]
	# get glyph of this layer
	glyph = layer.parent
	
	# access all layers of this glyph
	
	Glyphs.showMacroWindow()
	message_text = "Oncurve points\n\n"
	for layer in glyph.layers:
		print(layer.name, ": ", countMyNodes( layer))
		message_text += layer.name + ": " + str(countMyNodes(layer)) + "\n"
	vd.message(message_text)

except Exception as e:
	# print error
	Glyphs.showMacroWindow()
	print("CountOnCurvePoints Error: %s" % e)
