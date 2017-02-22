#MenuTitle: Create Drop Shadow
#Created by Kyle Wayne Benson
# -*- coding: utf-8 -*-
__doc__="""
Replace each selected glyphs with a drop shadow
"""

import vanilla
from vanilla import *
import GlyphsApp

class DropShadow( object ):
	def __init__( self ):
		# Window 'self.w':
		windowWidth  = 250
		windowHeight = 180
		windowWidthResize  = 300 # user can resize width by this value
		windowHeightResize = 0   # user can resize height by this value
		self.w = vanilla.Window(
			( windowWidth, windowHeight ), # default window size
			"Create Drop Shadow", # window title
			minSize = ( windowWidth, windowHeight ), # minimum size (for resizing)
			maxSize = ( windowWidth + windowWidthResize, windowHeight + windowHeightResize ), # maximum size (for resizing)
			autosaveName = "com.kylewaynebenson.DropShadow.mainwindow" # stores last window position and size
		)
		
		# UI elements:
		YOffset = 10
		
		self.w.text_1 = vanilla.TextBox( (15, YOffset, -15, 30), "Create drop shadow that is this many units removed from original drawing:", sizeStyle='small' )
		
		LineHeight = 40
		YOffset += LineHeight
		
		self.w.text_2 = vanilla.TextBox( ( 15, YOffset, 20, 20), "X:", sizeStyle='regular' )
		self.w.xAxis = vanilla.EditText( ( 40, YOffset, 50, 21), "-20", sizeStyle='regular' )
		self.w.text_3 = vanilla.TextBox( (-95, YOffset, 20, 20), "Y:", sizeStyle='regular' )
		self.w.yAxis = vanilla.EditText( (-20-50, YOffset, -20, 21), "-20", sizeStyle='regular' )

		LineHeight = 30
		YOffset += LineHeight

		self.w.text_4 = vanilla.TextBox( (15, YOffset, 42, 20), "Offset:", sizeStyle='regular' )
		self.w.offset = vanilla.EditText( (62, YOffset, 50, 21), "0", sizeStyle='regular' )
		self.w.checkBox = CheckBox((-110, YOffset, 0, 20), "Keep letters", value=False)
		
		YOffset += LineHeight
		
		# Run Button:
		self.w.runButton = vanilla.Button((-130, -20-15, -15, -15), "Create Shadows", sizeStyle='regular', callback=self.DropShadowMain )
		self.w.setDefaultButton( self.w.runButton )

		# Open window and focus on it:
		self.w.open()
		self.w.makeKey()


	def DropShadowMain( self, sender ):
		self.offsetCurveFilter = NSClassFromString("GlyphsFilterOffsetCurve")
		pathOp = GSPathOperator.alloc().init()
		Font = Glyphs.font
		selectedLayers = Font.selectedLayers
		xAxis = float(self.w.xAxis.get())
		yAxis = float(self.w.yAxis.get())
		offsetX = float(self.w.offset.get())
		offsetY = float(self.w.offset.get())
		glyphsChanged = []
		try:

			for thisLayer in selectedLayers:

				glyphsChanged.append( thisLayer.parent.name )
				thisLayer.parent.beginUndo() # wrapper for undo function

				thisLayer.correctPathDirection() #
				thisLayer.correctPathDirection() #
				thisLayer.correctPathDirection() #

				shadowPathList = NSMutableArray.array()
				prePathList = NSMutableArray.array()
				
				#save original outline
				for thisPath in thisLayer.paths:
					newPath = GSPath()
					for n in thisPath.nodes:
						newNode = GSNode()
						setX = n.x + xAxis
						setY = n.y + yAxis
						newNode.type = n.type
						newNode.setPosition_((setX, setY))
						newPath.addNode_( newNode )
					newPath.closed = thisPath.closed
					shadowPathList.append( newPath )
					prePathList.append( thisPath )

				self.offsetCurveFilter.offsetLayer_offsetX_offsetY_makeStroke_position_error_shadow_( thisLayer, offsetX, offsetY, False, 0.5, None, None )

				for thisPath in thisLayer.paths:
					shadowPathList.append( thisPath )

				pathOp.removeOverlapPaths_error_( shadowPathList, None)

				#reverse shadow
				for thisPath in thisLayer.paths:
					thisPath.reverse()

				#punch out the old drawing
				for shadowPath in shadowPathList:
					thisLayer.addPath_( shadowPath )

				thisLayer.removeOverlap()

				if (self.w.checkBox.get() == True):
					for prePath in prePathList:
						thisLayer.addPath_( prePath )


				thisLayer.correctPathDirection()
				thisLayer.parent.endUndo() # wrapper for undo function

			print "Created drop shadow for these glyphs:", glyphsChanged

		except Exception, e:
			# print error
			Glyphs.showMacroWindow()
			print "Create Drop Shadow Error: %s" % e

DropShadow()
