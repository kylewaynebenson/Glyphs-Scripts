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
		windowHeight = 180
		windowWidthResize  = 300 # user can resize width by this value
		windowHeightResize = 0   # user can resize height by this value
		self.w = vanilla.FloatingWindow(
			( windowWidth, windowHeight ), # default window size
			"Create Drop Shadow", # window title
			minSize = ( windowWidth, windowHeight ), # minimum size (for resizing)
			maxSize = ( windowWidth + windowWidthResize, windowHeight + windowHeightResize ), # maximum size (for resizing)
			autosaveName = "com.kylewaynebenson.DropShadow.mainwindow" # stores last window position and size
		)
		
		# UI elements:
		self.w.text_1 = vanilla.TextBox( (15, 10, -15, 30), "Create drop shadow that is this many units removed from original drawing:", sizeStyle='small' )

		self.w.text_2 = vanilla.TextBox( ( 15, 60, 20, 20), "X:", sizeStyle='small' )
		self.w.xAxis = vanilla.EditText( ( 40, 60-1, 50, 19), "-20", sizeStyle='small' )
		self.w.text_3 = vanilla.TextBox( (-95, 60, 20, 20), "Y:", sizeStyle='small' )
		self.w.yAxis = vanilla.EditText( (-20-50, 60-1, -20, 19), "-20", sizeStyle='small' )

		# self.w.text_4 = vanilla.TextBox( (15, 90, 42, 20), "Offset:", sizeStyle='small' )
		# self.w.offset = vanilla.EditText( (62, 90-1, 50, 19), "0", sizeStyle='small' )
		
		
		# Run Button:
		self.w.runButton = vanilla.Button((-130, -20-15, -15, -15), "Create Shadows", sizeStyle='regular', callback=self.DropShadowMain )
		self.w.setDefaultButton( self.w.runButton )
		
		# Load Settings
		# if not self.LoadPreferences():
		# 	print "Note: 'Create Drop Shadow' could not load preferences."

		# Open window and focus on it:
		self.w.open()
		self.w.makeKey()

	############
	# Figure out saving later
	############
	# def SavePreferences( self, sender ):
	# 	try:
	# 		Glyphs.defaults["com.kylewaynebenson.DropShadow.xAxis"] = self.w.xAxis.get()
	# 		Glyphs.defaults["com.kylewaynebenson.DropShadow.yAxis"] = self.w.yAxis.get()
	# 	except:
	# 		return False
			
	# 	return True

	# def LoadPreferences( self ):
	# 	try:
	# 		self.w.xAxis.set( Glyphs.defaults["com.kylewaynebenson.DropShadow.xAxis"] )
	# 		self.w.yAxis.set( Glyphs.defaults["com.kylewaynebenson.DropShadow.yAxis"] )
	# 	except:
	# 		return False
			
	# 	return True


	def DropShadowMain( self, sender ):
		self.offsetCurveFilter = NSClassFromString("GlyphsFilterOffsetCurve")
		Font = Glyphs.font
		selectedLayers = Font.selectedLayers
		xAxis = float(self.w.xAxis.get())
		yAxis = float(self.w.yAxis.get())
		# offsetX = float(self.w.offset.get())
		# offsetY = float(self.w.offset.get())
		glyphsChanged = []
		try:
			# offsetLayer = []
			for thisLayer in selectedLayers:

				glyphsChanged.append( thisLayer.parent.name )
				thisLayer.parent.beginUndo() # wrapper for undo function

				thisLayer.correctPathDirection() # double counter (B and 8) get missed here?
				thisLayer.correctPathDirection() # single counters (D O) get bad now too
				thisLayer.correctPathDirection() # for some reason now everything is good
				addPathList = []
				negPathList = []
				for thisPath in thisLayer.paths:
					newPath = thisPath.copy()
					for thisNode in newPath.nodes:
						thisNode.x += xAxis
						thisNode.y += yAxis
					negPathList.append( thisPath )
					addPathList.append( newPath )
				thisLayer.paths.extend( addPathList )
				thisLayer.removeOverlap()
				############
				# offset doesn't work because you can't use this filter on a python array. Must be a font object
				############
				# self.offsetCurveFilter.offsetLayer_offsetX_offsetY_makeStroke_position_error_shadow_( negPathList, offsetX*0.5, offsetY*0.5, True, 0.5, None, None )
				for thisPath in negPathList:
					thisPath.reverse()
				thisLayer.paths.extend( negPathList )
				thisLayer.removeOverlap()
				thisLayer.correctPathDirection()

				thisLayer.parent.endUndo() # wrapper for undo function

			print "Created drop shadow for these glyphs:", glyphsChanged

		except Exception, e:
			# print error
			Glyphs.showMacroWindow()
			print "Create Drop Shadow Error: %s" % e

DropShadow()
