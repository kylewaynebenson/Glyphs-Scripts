#MenuTitle: Simplify Shape
#Created by Kyle Wayne Benson
# -*- coding: utf-8 -*-
__doc__="""
Reduce amount of nodes. Best for grungy and textured vectors.
"""

import vanilla
import GlyphsApp

class SimplifyShape( object ):
	def __init__( self ):
		# Window 'self.w':
		windowWidth  = 250
		windowHeight = 140
		windowWidthResize  = 300 # user can resize width by this value
		windowHeightResize = 0   # user can resize height by this value
		self.w = vanilla.Window(
			( windowWidth, windowHeight ), # default window size
			"Simplify Shape", # window title
			minSize = ( windowWidth, windowHeight ), # minimum size (for resizing)
			maxSize = ( windowWidth + windowWidthResize, windowHeight + windowHeightResize ), # maximum size (for resizing)
			autosaveName = "com.kylewaynebenson.SimplifyShape.mainwindow" # stores last window position and size
		)
		
		# UI elements:
		YOffset = 10
		
		self.w.text_1 = vanilla.TextBox( (15, YOffset, -15, 30), "Simplify all paths by 1 out of every", sizeStyle='small' )
		
		LineHeight = 25
		YOffset += LineHeight
		
		self.w.nodeCount = vanilla.EditText( ( 15, YOffset, 40, 21), "3", sizeStyle='regular' )
		self.w.text_2 = vanilla.TextBox( ( 65, YOffset, 80, 20), "nodes", sizeStyle='regular' )
		
		# Run Button:
		self.w.runButton = vanilla.Button((-130, -20-15, -15, -15), "Simplify", sizeStyle='regular', callback=self.SimplifyShapeMain )
		self.w.setDefaultButton( self.w.runButton )
		
		# Open window and focus on it:
		self.w.open()
		self.w.makeKey()

	
	def deletePoints( self, thisLayer, nodeCount ):
		for thisPath in thisLayer.paths:
			counter = 0
			pathlength = len(thisPath)
			for i in range(pathlength)[::-1]:
				thisNode = thisPath.nodes[i]
				if (thisNode.type == GSCURVE) or (thisNode.type == LINE):
					counter += 1
					if counter == nodeCount:
						thisPath.removeNodeCheckKeepShape_( thisNode )
						counter = 0

	def deleteOverlappingPoints( self, thisLayer):
		for i in range(len(thisLayer.paths))[::-1]:
			thisPath = thisLayer.paths[i]
			for a, b in zip(thisPath.nodes, thisPath.nodes[1:]):
				if (int(a.x) == int(b.x)) & (int(a.y) == int(b.y)):
					thisPath.removeNodeCheckKeepShape_(b)

	def countMyNodes( self, thisLayer):
		nodeTotal = 0
		for thisPath in thisLayer.paths:
			for thisNode in thisPath.nodes:
				if (thisNode.type == GSCURVE) or (thisNode.type == LINE):
					nodeTotal += 1
		return nodeTotal

	def SimplifyShapeMain( self, sender ):
		Font = Glyphs.font
		selectedLayers = Font.selectedLayers
		nodeCount = float(self.w.nodeCount.get())

		try:
			for thisLayer in selectedLayers:

				thisLayer.parent.beginUndo() # wrapper for undo function

				print thisLayer.name
				print "On curve node count:", self.countMyNodes( thisLayer)
				
				self.deletePoints( thisLayer, nodeCount )
				self.deleteOverlappingPoints( thisLayer )
				
				print "New on curve node count:", self.countMyNodes( thisLayer)

				thisLayer.parent.endUndo() # wrapper for undo function

		except Exception, e:
			# print error
			Glyphs.showMacroWindow()
			print "Simplify Shape Error: %s" % e

SimplifyShape()
