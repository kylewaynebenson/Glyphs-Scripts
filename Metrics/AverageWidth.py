#MenuTitle: Average Width
#Created by Kyle Wayne Benson
# -*- coding: utf-8 -*-
__doc__="""
Figure out the average width of selected glyphs in a layer
"""

import vanilla.dialogs as vd
import GlyphsApp


def averageWidth():
	Glyphs.clearLog()
	try:
		averageWidth = 0
		count = 0
		alreadyCheckedGlyphs = []
		msg_txt = ""
		for layer in Glyphs.font.selectedLayers:
			thisGlyph = layer.parent
			
			if thisGlyph.name is None: continue
			if thisGlyph.name == "None": continue
			if thisGlyph.name in alreadyCheckedGlyphs: continue # this will omitt glyphs.width that was already checked
			
			averageWidth += layer.width
			count += 1
			print("\t", thisGlyph.name)
			msg_txt += "'" + str(thisGlyph.name) + "' " + "width: " + str(layer.width) + "\n"
			print("\t" "Width =>", layer.width)
			alreadyCheckedGlyphs.append(thisGlyph.name)
			
		averageWidth = averageWidth/count
		print("Average Width =>", averageWidth)
		msg_txt += "\n\nAverage Width: %s" % averageWidth
		vd.message(msg_txt)

	except Exception as e:
		# print error
		Glyphs.showMacroWindow()
		print("Change Width Centered Error: %s" % e)

averageWidth()
