#MenuTitle: Keep Largest Path
#Created by Kyle Wayne Benson
#Description: Deletes all paths in selected glyphs except for the largest path.
# -*- coding: utf-8 -*-
__doc__="""
deletes everything except for the largest path
"""

from AppKit import NSMutableIndexSet
import GlyphsApp
thisFont = Glyphs.font # frontmost font
thisFontMaster = thisFont.selectedFontMaster # active master
listOfSelectedLayers = thisFont.selectedLayers # active layers of selected glyphs

def deleteLargestPath( thisLayer ):
	layerarea = []
	for thisPath in thisLayer.paths:
		layerarea.append(thisPath.area())
	if Glyphs.versionNumber >= 3:
		# Glyphs 3 code
		pathsToBeRemoved = NSMutableIndexSet.alloc().init()

		for i, thisPath in enumerate(thisLayer.shapes) :
			if thisPath.area() != max(layerarea):
				pathsToBeRemoved.addIndex_( i )


		thisLayer.removeShapesAtIndexes_( pathsToBeRemoved )
	else:
		# Glyphs 2 code
		indexesOfPathsToBeRemoved = []

		numberOfPaths = len(thisLayer.paths)
		for thisPathNumber in range( numberOfPaths ):
			if thisPathNumber < (numberOfPaths - 1):
				thisPath = thisLayer.paths[thisPathNumber]
				if thisPath.area() != max(layerarea):
					indexesOfPathsToBeRemoved.append( thisPathNumber )
		
		if indexesOfPathsToBeRemoved:
			for thatIndex in reversed( sorted( indexesOfPathsToBeRemoved )):
				thisLayer.removePathAtIndex_( thatIndex )

thisFont.disableUpdateInterface() # suppresses UI updates in Font View

for thisLayer in listOfSelectedLayers:
	thisGlyph = thisLayer.parent
	thisGlyph.beginUndo() # begin undo grouping
	deleteLargestPath( thisLayer )
	thisGlyph.endUndo()   # end undo grouping

thisFont.enableUpdateInterface() # re-enables UI updates in Font View