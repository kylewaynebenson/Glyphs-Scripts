#MenuTitle: Randomly Move Points 
#Created by Kyle Wayne Benson
# -*- coding: utf-8 -*-
__doc__="""
Randomly move the x and y of all selected points.
"""

import vanilla
from vanilla import *
import GlyphsApp
import random

class RandomlyMove( object ):
	def __init__( self ):
		# Window 'self.w':
		windowWidth  = 250
		windowHeight = 190
		windowWidthResize  = 300 # user can resize width by this value
		windowHeightResize = 0   # user can resize height by this value
		self.w = vanilla.Window(
			( windowWidth, windowHeight ), # default window size
			"Randomly Move Points", # window title
			minSize = ( windowWidth, windowHeight ), # minimum size (for resizing)
			maxSize = ( windowWidth + windowWidthResize, windowHeight + windowHeightResize ), # maximum size (for resizing)
			autosaveName = "com.kylewaynebenson.RandomlyMove.mainwindow" # stores last window position and size
		)
		
		# UI elements:
		YOffset = 10
		
		self.w.text_1 = vanilla.TextBox( (15, YOffset, -15, 30), "Randomly move all points by:", sizeStyle='small' )
		
		LineHeight = 25
		YOffset += LineHeight
		
		self.w.text_2 = vanilla.TextBox( ( 15, YOffset, 80, 20), "Range", sizeStyle='regular' )
		self.w.moveRange = vanilla.EditText( ( 65, YOffset, 40, 21), "3", sizeStyle='regular' )

		LineHeight = 30
		YOffset += LineHeight

		self.w.text_3 = vanilla.TextBox( ( 15, YOffset, 80, 20), "Grid", sizeStyle='regular' )
		self.w.moveGrid = vanilla.EditText( ( 65, YOffset, 40, 21), "2", sizeStyle='regular' )

		LineHeight = 30
		YOffset += LineHeight
		
		self.w.checkBox = CheckBox((15, YOffset, 0, 20), "Only move OCPs", value=False)
		
		# Run Button:
		self.w.runButton = vanilla.Button((-130, -20-15, -15, -15), "Shake", sizeStyle='regular', callback=self.RamdonlyMovePoints )
		self.w.setDefaultButton( self.w.runButton )
		
		# Open window and focus on it:
		self.w.open()
		self.w.makeKey()


	def RamdonlyMovePoints( self, sender ):
		Font = Glyphs.font
		selectedLayers = Font.selectedLayers
		moveRange = float(self.w.moveRange.get())
		moveGrid = abs(float(self.w.moveGrid.get()) / 2)
		if moveGrid == 0:
			moveGrid = 1
		try:
			for thisLayer in selectedLayers:
				thisLayer.parent.beginUndo()
				for thisPath in thisLayer.paths:
					for thisNode in thisPath.nodes:
						if (self.w.checkBox.get() == True):
							if (thisNode.type == GSCURVE) or (thisNode.type == LINE):
								thisNode.x += (random.randint(-moveRange,moveRange) * moveGrid)
								thisNode.y += (random.randint(-moveRange,moveRange) * moveGrid)
						else:
							thisNode.x += (random.randint(-moveRange,moveRange) * moveGrid)
							thisNode.y += (random.randint(-moveRange,moveRange) * moveGrid)
						
					thisPath.checkConnections()
				thisLayer.parent.endUndo()
		except Exception as e:
			# print error
			Glyphs.showMacroWindow()
			print("Move Points Error: %s" % e)

RandomlyMove()
