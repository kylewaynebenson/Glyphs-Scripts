#MenuTitle: Keep Largest Path
#Created by Kyle Wayne Benson
# -*- coding: utf-8 -*-
__doc__="""
deletes everything except for the largest path
"""

import GlyphsApp
thisFont = Glyphs.font # frontmost font
thisFontMaster = thisFont.selectedFontMaster # active master
listOfSelectedLayers = thisFont.selectedLayers # active layers of selected glyphs

def keepLargestPath( thisLayer ):
	indexesOfPathsToBeRemoved = []
	layerarea = []
	for thisPath in thisLayer.paths:
		layerarea.append(thisPath.area())

	numberOfPaths = len(thisLayer.paths)
	for thisPathNumber in range( numberOfPaths ):
		if thisPathNumber < numberOfPaths:
			thisPath = thisLayer.paths[thisPathNumber]
			if thisPath.area() != max(layerarea):
				indexesOfPathsToBeRemoved.append( thisPathNumber )

	if indexesOfPathsToBeRemoved:
		for thatIndex in reversed( sorted( indexesOfPathsToBeRemoved )):
			thisLayer.removePathAtIndex_( thatIndex )


for thisLayer in listOfSelectedLayers:
	thisGlyph = thisLayer.parent
	thisGlyph.beginUndo() # begin undo grouping
	keepLargestPath( thisLayer )
	thisGlyph.endUndo()   # end undo grouping
