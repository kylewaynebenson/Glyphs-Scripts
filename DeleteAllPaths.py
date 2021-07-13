#MenuTitle: Delete All Paths
#Created by Kyle Wayne Benson
# -*- coding: utf-8 -*-
__doc__="""
Finds and deletes all paths
"""
from AppKit import NSMutableIndexSet
import GlyphsApp
thisFont = Glyphs.font # frontmost font
thisFontMaster = thisFont.selectedFontMaster # active master
listOfSelectedLayers = thisFont.selectedLayers # active layers of selected glyphs

def deleteSmallestPath( thisLayer ):
	indexesOfPathsToBeRemoved = []
#	layerarea = []
#	for thisPath in thisLayer.paths:
#		layerarea.append(thisPath.area())
	if Glyphs.versionNumber >= 3:
		# Glyphs 3 code
		for index, shape in enumerate(thisLayer.shapes):
			if shape.shapeType == GSShapeTypePath:
				indexesOfPathsToBeRemoved.append(index)
		try:
			indexes = NSMutableIndexSet.alloc().init()
			for i in indexesOfPathsToBeRemoved:
				
				indexes.addIndex_(i)
			thisLayer.removeShapesAtIndexes_(indexes)
		except Exception as e:
			print(e)

	else:
		# Glyphs 2 code
		numberOfPaths = len(thisLayer.paths)
		for thisPathNumber in range( numberOfPaths ):
			indexesOfPathsToBeRemoved.append( thisPathNumber )
		
		if indexesOfPathsToBeRemoved:
			for thatIndex in reversed( sorted( indexesOfPathsToBeRemoved ) ):
				thisLayer.removePathAtIndex_( thatIndex )

thisFont.disableUpdateInterface() # suppresses UI updates in Font View

for thisLayer in listOfSelectedLayers:
	thisGlyph = thisLayer.parent
	thisGlyph.beginUndo() # begin undo grouping
	deleteSmallestPath( thisLayer )
	thisGlyph.endUndo()   # end undo grouping

thisFont.enableUpdateInterface() # re-enables UI updates in Font View