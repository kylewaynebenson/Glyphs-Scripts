#MenuTitle: Delete All Paths
#Created by Kyle Wayne Benson
# -*- coding: utf-8 -*-
__doc__="""
Finds and deletes all paths
"""

import GlyphsApp
thisFont = Glyphs.font # frontmost font
thisFontMaster = thisFont.selectedFontMaster # active master
listOfSelectedLayers = thisFont.selectedLayers # active layers of selected glyphs

def deleteSmallestPath( thisLayer ):
	indexesOfPathsToBeRemoved = []
	layerarea = []
	for thisPath in thisLayer.paths:
		layerarea.append(thisPath.area())

	numberOfPaths = len(thisLayer.paths)
	for thisPathNumber in range( numberOfPaths ):
		indexesOfPathsToBeRemoved.append( thisPathNumber )
	
	if indexesOfPathsToBeRemoved:
		for thatIndex in reversed( sorted( indexesOfPathsToBeRemoved )):
			thisLayer.removePathAtIndex_( thatIndex )

thisFont.disableUpdateInterface() # suppresses UI updates in Font View

for thisLayer in listOfSelectedLayers:
	thisGlyph = thisLayer.parent
	thisGlyph.beginUndo() # begin undo grouping
	deleteSmallestPath( thisLayer )
	thisGlyph.endUndo()   # end undo grouping

thisFont.enableUpdateInterface() # re-enables UI updates in Font View