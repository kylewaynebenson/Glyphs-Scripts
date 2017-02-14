#MenuTitle: Create Cast Shadow
#Created by Kyle Wayne Benson
# -*- coding: utf-8 -*-
__doc__="""
Replace each selected glyphs with a cast shadow
"""

import vanilla
import GlyphsApp

class CastShadow( object ):
	def __init__( self ):
		# Window 'self.w':
		windowWidth  = 250
		windowHeight = 180
		windowWidthResize  = 300 # user can resize width by this value
		windowHeightResize = 0   # user can resize height by this value
		self.w = vanilla.Window(
			( windowWidth, windowHeight ), # default window size
			"Create Cast Shadow", # window title
			minSize = ( windowWidth, windowHeight ), # minimum size (for resizing)
			maxSize = ( windowWidth + windowWidthResize, windowHeight + windowHeightResize ), # maximum size (for resizing)
			autosaveName = "com.kylewaynebenson.CastShadow.mainwindow" # stores last window position and size
		)
		
		# UI elements:
		self.w.text_1 = vanilla.TextBox( (15, 10, -15, 30), "Create Cast shadow that is this many units removed from original drawing:", sizeStyle='small' )

		self.w.text_2 = vanilla.TextBox( ( 15, 60, 20, 20), "X:", sizeStyle='regular' )
		self.w.xAxis = vanilla.EditText( ( 40, 60-1, 50, 21), "-20", sizeStyle='regular' )
		self.w.text_3 = vanilla.TextBox( (-95, 60, 20, 20), "Y:", sizeStyle='regular' )
		self.w.yAxis = vanilla.EditText( (-20-50, 60-1, -20, 21), "-20", sizeStyle='regular' )

		self.w.text_4 = vanilla.TextBox( (15, 90, 52, 20), "Stroke:", sizeStyle='regular' )
		self.w.offset = vanilla.EditText( (68, 90-1, 50, 21), "4", sizeStyle='regular' )

		self.w.text_5 = vanilla.TextBox( (-110, 90, 52, 20), "Gap:", sizeStyle='regular' )
		self.w.gap = vanilla.EditText( (-70, 90-1, 50, 21), "0", sizeStyle='regular' )
		
		
		# Run Button:
		self.w.runButton = vanilla.Button((-130, -20-15, -15, -15), "Create Shadows", sizeStyle='regular', callback=self.CastShadowMain )
		self.w.setDefaultButton( self.w.runButton )
		
		# Open window and focus on it:
		self.w.open()
		self.w.makeKey()

	
	def DeleteStrayPoints( self, thisLayer ):
		for i in range(len(thisLayer.paths))[::-1]:
			thisPath = thisLayer.paths[i]
			for a, b in zip(thisPath.nodes, thisPath.nodes[1:]):
				if (a.type == b.type):
					if (int(a.x) == int(b.x)) & ((abs(int(a.y) - int(b.y)) == 1) | (abs(int(b.y) - int(a.y)) == 1)):
						thisPath.removeNodeCheckKeepShape_(b)

	def CastShadowMain( self, sender ):
		pathOp = GSPathOperator.alloc().init()
		self.offsetCurveFilter = NSClassFromString("GlyphsFilterOffsetCurve")
		Font = Glyphs.font
		selectedLayers = Font.selectedLayers
		xAxis = float(self.w.xAxis.get())
		yAxis = float(self.w.yAxis.get())
		offsetX = float(self.w.offset.get())
		offsetY = float(self.w.offset.get())
		shadowLen = int(max(abs(yAxis), abs(xAxis)))
		distance = int(self.w.gap.get())
		glyphsChanged = []
		try:

			for thisLayer in selectedLayers:

				glyphsChanged.append( thisLayer.parent.name )
				thisLayer.parent.beginUndo() # wrapper for undo function

				thisLayer.correctPathDirection() # double counter (B and 8) get missed here?
				thisLayer.correctPathDirection() # single counters (D O) get bad now too

				addPathList = NSMutableArray.array()
				prePathList = NSMutableArray.array()
				
				#save original outline
				for thisPath in thisLayer.paths:
					prePathList.append( thisPath )

				for thisPath in thisLayer.paths:
					count = 1 + distance
					for i in range(shadowLen):
						newPath = GSPath()
						#each layer of the cast shadow
						for n in thisPath.nodes:
							newNode = GSNode()
							# print "new guy \n"
							# print thisNode.x, thisNode.y
							if xAxis < 0:
								setX = n.x - count
							if yAxis < 0:
								setY = n.y - count
							if xAxis > 0:
								setX = n.x + count
							if yAxis > 0:
								setY = n.y + count
							newNode.type = n.type
							newNode.setPosition_((setX, setY))
							newPath.addNode_( newNode )
						#add shadow stack duplicate array
						newPath.closed = thisPath.closed
						addPathList.append( newPath )
						count += 1
				
				#merge shadow into path
				for thisPath in addPathList:
					thisLayer.addPath_( thisPath )
				
				thisLayer.removeOverlap()
				self.DeleteStrayPoints( thisLayer )

				#offset shadow
				if (offsetX != 0) & (offsetY != 0): #setting stroke thickness
					self.offsetCurveFilter.offsetLayer_offsetX_offsetY_makeStroke_position_error_shadow_( thisLayer, offsetX, offsetY, False, 0.5, None, None )

				#reverse shadow
				for thisPath in thisLayer.paths:
					thisPath.reverse()
				
				#punch out the old drawing
				pathOp.removeOverlapPaths_error_( prePathList, None)
				for thisPath in prePathList:
					thisLayer.addPath_( thisPath )
				
				thisLayer.correctPathDirection()
				thisLayer.parent.endUndo() # wrapper for undo function

			print "Created cast shadow for these glyphs:", glyphsChanged
		

		except Exception, e:
			# print error
			Glyphs.showMacroWindow()
			print "Create Cast Shadow Error: %s" % e

CastShadow()
