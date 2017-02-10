#MenuTitle: Create Drop Shadow
#Created by Kyle Wayne Benson
# -*- coding: utf-8 -*-
__doc__="""
Replace each selected glyphs with a drop shadow
"""

import vanilla
import GlyphsApp

class DropShadow( object ):
	def __init__( self ):
		# Window 'self.w':
		windowWidth  = 250
		windowHeight = 150
		windowWidthResize  = 300 # user can resize width by this value
		windowHeightResize = 0   # user can resize height by this value
		self.w = vanilla.FloatingWindow(
			( windowWidth, windowHeight ), # default window size
			"Create Drop Shadow", # window title
			minSize = ( windowWidth, windowHeight ), # minimum size (for resizing)
			maxSize = ( windowWidth + windowWidthResize, windowHeight + windowHeightResize ), # maximum size (for resizing)
			autosaveName = "com.kylewaynebenson.DropShadow.mainwindow" # stores last window position and size
		)
		
		# UI
		self.w.text_1 = vanilla.TextBox( (15, 10, -15, 30), "Create drop shadow that is this many units removed from original drawing:", sizeStyle='small' )

		self.w.text_2 = vanilla.TextBox( ( 15, 60, 20, 20), "X:", sizeStyle='small' )
		self.w.xAxis = vanilla.EditText( ( 40, 60-1, 50, 19), "10", sizeStyle='small' )
		self.w.text_3 = vanilla.TextBox( (-95, 60, 20, 20), "Y:", sizeStyle='small' )
		self.w.yAxis = vanilla.EditText( (-20-50, 60-1, -20, 19), "10", sizeStyle='small' )
		
		# Run Button
		self.w.runButton = vanilla.Button((-130, -20-15, -15, -15), "Create Shadows", sizeStyle='regular', callback=self.DropShadowMain )
		self.w.setDefaultButton( self.w.runButton )
		
		# Open window and focus
		self.w.open()
		self.w.makeKey()

	def DropShadowMain( self, sender ):
	def DropShadowMain( self, sender ):
		Font = Glyphs.font
		selectedLayers = Font.selectedLayers
		xAxis = float(self.w.xAxis.get())
		yAxis = float(self.w.yAxis.get())
		shouldBeOdd = False
		if yAxis < 0:
			shouldBeOdd = True
		try:
			for thisLayer in selectedLayers:
				newPathList = []
				for thisPath in thisLayer.paths:
					newPath = thisPath.copy()
					for thisNode in newPath.nodes:
						thisNode.x += xAxis
						thisNode.y += yAxis
					newPath.reverse()
					newPathList.append( newPath )
				thisLayer.paths.extend( newPathList )
				thisLayer.removeOverlap()
				counter = 0
				delList = []
				for thisPath in thisLayer.paths:
					if shouldBeOdd:
						if counter % 2 == 0:
							delList.append( thisPath )
					else:
						if counter % 2 != 0:
							delList.append( thisPath )
					counter += 1
				thisLayer.paths = list(set(thisLayer.paths).difference(set(delList)))
		except Exception, e:
			# brings macro window to front and reports error:
			Glyphs.showMacroWindow()
			print "Create Drop Shadow Error: %s" % e

DropShadow()
