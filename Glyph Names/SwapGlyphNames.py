# MenuTitle: Swap Glyph Names
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Takes a list of glyphname1=glyphname2 pairs and swaps glyph names in the font accordingly. When you input "A=A.ss12", A becomes A.ss12 and A.ss12 becomes A. Optionally updates component references.
"""

import vanilla
import uuid
from AppKit import NSFont
from GlyphsApp import Glyphs


class SwapGlyphNames:
	def __init__(self):
		# Default preferences
		self.preferences = {
			"renameList": "A=A.ss01",
			"allFonts": False,
			"updateComponents": False,
		}
		# Window 'self.w':
		windowWidth = 250
		windowHeight = 200
		windowWidthResize = 800  # user can resize width by this value
		windowHeightResize = 800  # user can resize height by this value
		self.w = vanilla.FloatingWindow(
			(windowWidth, windowHeight),  # default window size
			"Swap Glyph Names",  # window title
			minSize=(windowWidth, windowHeight),  # minimum size (for resizing)
			maxSize=(windowWidth + windowWidthResize, windowHeight + windowHeightResize),  # maximum size (for resizing)
		)

		# UI elements:
		self.w.text_1 = vanilla.TextBox((10, 12 + 2, -10, 14), "Add lines like glyph1=glyph2 to swap:", sizeStyle='small')
		self.w.renameList = vanilla.TextEditor((1, 40, -1, -70), self.preferences["renameList"], callback=self.savePreferences)
		self.w.renameList.getNSTextView().setFont_(NSFont.userFixedPitchFontOfSize_(-1.0))
		self.w.renameList.getNSTextView().turnOffLigatures_(1)
		self.w.renameList.getNSTextView().useStandardLigatures_(0)
		self.w.renameList.selectAll()

		self.w.updateComponents = vanilla.CheckBox((10, -65, 250, 20), "Keep composite glyphs unchanged (maintain old design)", value=self.preferences["updateComponents"], callback=self.savePreferences, sizeStyle="small")
		self.w.allFonts = vanilla.CheckBox((10, -40, 100, 20), "⚠️ ALL Fonts", value=self.preferences["allFonts"], callback=self.savePreferences, sizeStyle="small")

		# Run Button:
		self.w.runButton = vanilla.Button((-100, -35, -15, -15), "Swap", callback=self.SwapGlyphNamesMain)

		# Open window and focus on it:
		self.w.open()
		self.w.makeKey()

	def savePreferences(self, sender=None):
		"""Save current UI state to preferences"""
		self.preferences["renameList"] = self.w.renameList.get()
		self.preferences["allFonts"] = self.w.allFonts.get()
		self.preferences["updateComponents"] = self.w.updateComponents.get()

	def SwapGlyphNamesMain(self, sender):
		try:
			# clear macro window log:
			Glyphs.clearLog()

			# update settings to the latest user input:
			self.savePreferences()

			if self.preferences["allFonts"]:
				theseFonts = Glyphs.fonts
			else:
				theseFonts = [Glyphs.font, ]

			for thisFont in theseFonts:
				print(f"Processing font: {thisFont.familyName}")
				
				# Collect all swap pairs first
				swapPairs = []
				for thisLine in self.preferences["renameList"].splitlines():
					if thisLine.strip() and "=" in thisLine:
						parts = thisLine.split("=")
						if len(parts) == 2:
							glyphName1 = parts[0].strip()
							glyphName2 = parts[1].strip()
							if glyphName1 and glyphName2:
								swapPairs.append((glyphName1, glyphName2))

				# Perform the swaps
				for glyphName1, glyphName2 in swapPairs:
					glyph1 = thisFont.glyphs[glyphName1]
					glyph2 = thisFont.glyphs[glyphName2]
					
					if glyph1 and glyph2:
						print(f"Swapping: {glyphName1} ↔ {glyphName2}")
						
						# Create unique temporary name to avoid conflicts
						tempName = f"__temp_swap_{uuid.uuid4().hex[:8]}"
						
						# Perform three-way swap
						glyph1.name = tempName
						glyph2.name = glyphName1
						glyph1.name = glyphName2
						
						# Swap export status
						glyph1Export = glyph1.export
						glyph1.export = glyph2.export
						glyph2.export = glyph1Export
						
					elif glyph1 and not glyph2:
						print(f"Renaming: {glyphName1} → {glyphName2} (target doesn't exist)")
						glyph1.name = glyphName2
					elif not glyph1 and glyph2:
						print(f"Renaming: {glyphName2} → {glyphName1} (source doesn't exist)")
						glyph2.name = glyphName1
					else:
						print(f"Warning: Neither {glyphName1} nor {glyphName2} found in font.")

				# Update components if requested
				if self.preferences["updateComponents"]:
					print("Updating component references to maintain old designs...")
					self.updateComponentReferences(thisFont, swapPairs)
				else:
					print("Component references unchanged - composite glyphs will use new designs automatically")

			print("Swap operation completed!")

			self.w.close()  # delete if you want window to stay open
		except Exception as e:
			# brings macro window to front and reports error:
			Glyphs.showMacroWindow()
			print(f"Swap Glyph Names Error: {e}")
			import traceback
			print(traceback.format_exc())

	def updateComponentReferences(self, font, swapPairs):
		"""Update component references to maintain old designs after glyph name swap"""
		# Create a mapping of old names to new names
		nameMapping = {}
		for name1, name2 in swapPairs:
			nameMapping[name1] = name2
			nameMapping[name2] = name1
		
		# Go through all glyphs and update component references
		# This ensures composite glyphs keep their original appearance
		componentsUpdated = 0
		for glyph in font.glyphs:
			for layer in glyph.layers:
				for component in layer.components:
					oldComponentName = component.componentName
					if oldComponentName in nameMapping:
						newComponentName = nameMapping[oldComponentName]
						component.componentName = newComponentName
						print(f"  Updated component in {glyph.name}: {oldComponentName} → {newComponentName}")
						componentsUpdated += 1
		
		if componentsUpdated > 0:
			print(f"  Total components updated: {componentsUpdated}")
		else:
			print("  No components needed updating")


SwapGlyphNames()