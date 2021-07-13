#MenuTitle: Change Width Centered
#Created by Kyle Wayne Benson
# -*- coding: utf-8 -*-
__doc__="""
Kind of like a multiplexer, but more boring. Uniformly changes width, but keeps character centered.
"""

import vanilla
import GlyphsApp

class ChangeWidthCentered( object ):
	def __init__( self ):
		# Window 'self.w':
		windowWidth  = 250
		windowHeight = 130
		windowWidthResize  = 300 # user can resize width by this value
		windowHeightResize = 0   # user can resize height by this value
		self.w = vanilla.Window(
			( windowWidth, windowHeight ), # default window size
			"Change Width Centered", # window title
			minSize = ( windowWidth, windowHeight ), # minimum size (for resizing)
			maxSize = ( windowWidth + windowWidthResize, windowHeight + windowHeightResize ), # maximum size (for resizing)
			autosaveName = "com.kylewaynebenson.ChangeWidthCentered.mainwindow" # stores last window position and size
		)
		
		# UI elements:
		self.w.text_1 = vanilla.TextBox( (15, 10, -15, 30), "Change new width to:", sizeStyle='small' )

		self.w.newWidth = vanilla.EditText( ( 15, 40-1, 50, 21), "750", sizeStyle='regular' )

		self.w.checkBox = vanilla.CheckBox((-120, 40, 0, 20), "All layers", value=False)
		
		# Run Button:
		self.w.runButton = vanilla.Button((-130, -20-15, -15, -15), "Change Width", sizeStyle='regular', callback=self.changeWidth )
		self.w.setDefaultButton( self.w.runButton )
		
		self.w.open()
		self.w.makeKey()


	def changeWidth( self, sender ):
		NewWidth = float(self.w.newWidth.get())
		AllLayers = self.w.checkBox.get()
		Glyphs.clearLog()
		Glyphs.showMacroWindow()
		try:
			for layer in Glyphs.font.selectedLayers:
				thisGlyph = layer.parent
				print("\n", thisGlyph.name)
				allLayers = len(thisGlyph.layers)
				count = 0
				if AllLayers == True:
					for thisLayer in thisGlyph.layers:
						AddToSides = (NewWidth - thisLayer.width) / 2
						print("\t", thisLayer.name)
						print("\t", "\t", "Current Width =>", thisLayer.width)
						print("\t", "\t", "Added to Sides =>", AddToSides)
						thisLayer.LSB = thisLayer.LSB + AddToSides
						thisLayer.RSB = thisLayer.RSB + AddToSides
						print("\t", "\t", "New Width =>", thisLayer.width)
				else:
					AddToSides = (NewWidth - layer.width) / 2
					print("\t", layer.name)
					print("\t", "\t", "Current Width =>", layer.width)
					print("\t", "\t", "Added to Sides =>", AddToSides)
					layer.LSB = layer.LSB + AddToSides
					layer.RSB = layer.RSB + AddToSides
					print("\t", "\t", "New Width =>", layer.width)
				if count == allLayers:
					thisGlyph.color = 6
		except Exception, e:
			# print error
			Glyphs.showMacroWindow()
			print("Change Width Centered Error: %s" % e)

ChangeWidthCentered()
