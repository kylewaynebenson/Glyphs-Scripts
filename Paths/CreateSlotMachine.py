#MenuTitle: Create Slot Machine
#Created by Kyle Wayne Benson
# -*- coding: utf-8 -*-
__doc__="""
Splits selected glyphs horizontally to create a slot machine wheel effect.
The glyph is shifted upward by the Y Shift amount, sliced at the top crop line,
and the overflow is repositioned below with the specified gap between the two halves —
like a slot machine reel between positions.
"""

import vanilla
from vanilla import *
import GlyphsApp
from GlyphsApp import Glyphs, GSLayer, GSPath, GSNode
import traceback


class SlotMachineEffect(object):
	def __init__(self):
		windowWidth = 300
		windowHeight = 255
		windowWidthResize = 100
		windowHeightResize = 0
		self.w = vanilla.Window(
			(windowWidth, windowHeight),
			"Create Slot Machine",
			minSize=(windowWidth, windowHeight),
			maxSize=(windowWidth + windowWidthResize, windowHeight + windowHeightResize),
			autosaveName="com.kylewaynebenson.SlotMachine.mainwindow"
		)

		YOffset = 10

		# Top crop dropdown
		self.w.text_topCrop = vanilla.TextBox((15, YOffset, 100, 20), "Top crop:", sizeStyle='regular')
		self.w.topCropPopup = vanilla.PopUpButton((120, YOffset, -15, 20), [
			"x-Height", "Cap Height", "Ascender"
		])
		self.w.topCropPopup.set(1)  # Default to Cap Height

		YOffset += 30

		# Bottom crop dropdown
		self.w.text_bottomCrop = vanilla.TextBox((15, YOffset, 100, 20), "Bottom crop:", sizeStyle='regular')
		self.w.bottomCropPopup = vanilla.PopUpButton((120, YOffset, -15, 20), [
			"Baseline", "Descender"
		])
		self.w.bottomCropPopup.set(0)  # Default to Baseline

		YOffset += 30

		# Y Shift input field
		self.w.text_yShift = vanilla.TextBox((15, YOffset, 100, 20), "Y Shift:", sizeStyle='regular')
		self.w.yShiftInput = vanilla.EditText((120, YOffset, 60, 21), "100", sizeStyle='regular')

		YOffset += 30

		# Gap input field
		self.w.text_gap = vanilla.TextBox((15, YOffset, 100, 20), "Gap:", sizeStyle='regular')
		self.w.gapInput = vanilla.EditText((120, YOffset, 60, 21), "20", sizeStyle='regular')

		YOffset += 35

		# Checkboxes
		self.w.closeAfterRunning = vanilla.CheckBox((15, YOffset, 260, 20), "Close popup after running", value=True)

		YOffset += 25

		self.w.allMasters = vanilla.CheckBox((15, YOffset, 260, 20), "Apply on all masters", value=False)

		# Run button
		self.w.runButton = vanilla.Button((-170, -20 - 15, -15, -15), "Create Slot Machine",
			sizeStyle='regular', callback=self.SlotMachineMain)
		self.w.setDefaultButton(self.w.runButton)

		self.w.open()
		self.w.makeKey()

	def getMetricValue(self, master, metricName):
		"""Get a font metric Y value for a given master."""
		if metricName == "x-Height":
			return master.xHeight
		elif metricName == "Cap Height":
			return master.capHeight
		elif metricName == "Ascender":
			return master.ascender
		elif metricName == "Baseline":
			return 0
		elif metricName == "Descender":
			return master.descender
		return 0

	def clipPaths(self, srcPaths, cutY, keepBelow=True, margin=2000):
		"""
		Clip paths at a horizontal line.
		keepBelow=True keeps everything below cutY, False keeps above.
		Uses a two-step mask approach (union then subtract) to avoid
		leaving the clipping rectangle as a visible artifact.
		"""
		if not srcPaths:
			return []

		tempLayer = GSLayer()
		for p in srcPaths:
			tempLayer.paths.append(p.copy())

		bounds = tempLayer.bounds
		minX = bounds.origin.x - margin
		maxX = bounds.origin.x + bounds.size.width + margin
		minY = bounds.origin.y - margin
		maxY = bounds.origin.y + bounds.size.height + margin

		# Build a mask covering the area to REMOVE
		# Big rectangle covering everything
		bigRect = GSPath()
		bigRect.closed = True
		bigRect.nodes = [
			GSNode((minX, minY)),
			GSNode((maxX, minY)),
			GSNode((maxX, maxY)),
			GSNode((minX, maxY))
		]

		# Keep-area rectangle (reversed to punch a hole in the big rect)
		keepRect = GSPath()
		keepRect.closed = True
		if keepBelow:
			keepRect.nodes = [
				GSNode((minX, minY)),
				GSNode((maxX, minY)),
				GSNode((maxX, cutY)),
				GSNode((minX, cutY))
			]
		else:
			keepRect.nodes = [
				GSNode((minX, cutY)),
				GSNode((maxX, cutY)),
				GSNode((maxX, maxY)),
				GSNode((minX, maxY))
			]
		keepRect.reverse()

		maskLayer = GSLayer()
		maskLayer.paths.append(bigRect)
		maskLayer.paths.append(keepRect)
		maskLayer.removeOverlap()
		maskLayer.correctPathDirection()

		# Step 1: Union the letter paths with the mask
		clipLayer = GSLayer()
		for p in srcPaths:
			clipLayer.paths.append(p.copy())
		for p in maskLayer.paths:
			clipLayer.paths.append(p.copy())
		clipLayer.removeOverlap()

		# Step 2: Subtract the mask, leaving only letter parts in the keep area
		for p in maskLayer.paths:
			cutPath = p.copy()
			cutPath.reverse()
			clipLayer.paths.append(cutPath)
		clipLayer.removeOverlap()
		clipLayer.correctPathDirection()

		return [p.copy() for p in clipLayer.paths]

	def shiftPaths(self, paths, dx, dy):
		"""Shift all nodes in a list of paths by (dx, dy)."""
		for path in paths:
			for node in path.nodes:
				node.position = (node.position.x + dx, node.position.y + dy)

	def SlotMachineMain(self, sender):
		try:
			Font = Glyphs.font
			if not Font:
				Glyphs.showNotification("Slot Machine", "No font open")
				return

			# Read UI parameters
			topCropOptions = ["x-Height", "Cap Height", "Ascender"]
			bottomCropOptions = ["Baseline", "Descender"]
			topCropName = topCropOptions[self.w.topCropPopup.get()]
			bottomCropName = bottomCropOptions[self.w.bottomCropPopup.get()]

			try:
				yShift = float(self.w.yShiftInput.get())
			except ValueError:
				Glyphs.showNotification("Slot Machine", "Invalid Y Shift value")
				return

			try:
				gap = float(self.w.gapInput.get())
			except ValueError:
				Glyphs.showNotification("Slot Machine", "Invalid Gap value")
				return

			allMasters = self.w.allMasters.get()
			closeAfterRunning = self.w.closeAfterRunning.get()

			# Determine which masters to process
			if allMasters:
				masters = Font.masters
			else:
				masters = [Font.selectedFontMaster]

			selectedGlyphs = set([layer.parent for layer in Font.selectedLayers if layer.parent])

			if not selectedGlyphs:
				Glyphs.showNotification("Slot Machine", "No glyphs selected")
				return

			glyphsChanged = []
			Font.disableUpdateInterface()

			for glyph in selectedGlyphs:
				glyph.beginUndo()

				for master in masters:
					srcLayer = glyph.layers[master.id]

					if len(srcLayer.paths) == 0 and len(srcLayer.components) == 0:
						continue

					topCropY = self.getMetricValue(master, topCropName)
					bottomCropY = self.getMetricValue(master, bottomCropName)

					# Prepare clean outlines
					baseLayer = srcLayer.copy()

					if hasattr(baseLayer, 'decomposeCorners'):
						try:
							baseLayer.decomposeCorners()
						except:
							pass

					if baseLayer.components:
						try:
							baseLayer.decomposeComponents()
						except:
							pass

					if hasattr(baseLayer, 'flattenOutlines'):
						try:
							baseLayer.flattenOutlines()
						except:
							pass

					if len(baseLayer.paths) == 0:
						print("Warning: %s has no paths after decomposition, skipping" % glyph.name)
						continue

					baseLayer.removeOverlap()
					baseLayer.correctPathDirection()
					cleanPaths = [p.copy() for p in baseLayer.paths]

					# Shift all paths up by Y Shift amount
					shiftedPaths = [p.copy() for p in cleanPaths]
					self.shiftPaths(shiftedPaths, 0, yShift)

					# Cut with gap: widen the slice at topCropY by the gap amount
					# Upper portion: keep below (topCropY - half the gap)
					# Overflow: keep above (topCropY + half the gap)
					halfGap = gap / 2.0
					upperPaths = self.clipPaths(shiftedPaths, topCropY - halfGap, keepBelow=True)
					overflowPaths = self.clipPaths(shiftedPaths, topCropY + halfGap, keepBelow=False)

					# Shift upper piece up so its top sits at the top crop line
					if upperPaths:
						self.shiftPaths(upperPaths, 0, halfGap)

					# Reposition overflow: shift down so the gap is preserved
					if overflowPaths:
						self.shiftPaths(overflowPaths, 0, -topCropY - halfGap)

					# Build final layer
					finalLayer = GSLayer()
					for p in upperPaths:
						finalLayer.paths.append(p.copy())
					for p in overflowPaths:
						finalLayer.paths.append(p.copy())
					finalLayer.correctPathDirection()

					# Preserve layer attributes
					finalLayer.layerId = srcLayer.layerId
					finalLayer.associatedMasterId = srcLayer.associatedMasterId
					finalLayer.width = srcLayer.width
					for anchor in srcLayer.anchors:
						finalLayer.anchors.append(anchor.copy())

					glyph.layers[master.id] = finalLayer

				glyph.endUndo()
				glyphsChanged.append(glyph.name)

			Font.enableUpdateInterface()

			if glyphsChanged:
				print("Created slot machine effect for: %s" % ", ".join(glyphsChanged))
				Glyphs.showNotification("Slot Machine", "Applied to %d glyph(s)" % len(glyphsChanged))

			if closeAfterRunning:
				self.w.close()

		except Exception as e:
			Glyphs.showMacroWindow()
			print("Slot Machine Error: %s" % e)
			print(traceback.format_exc())


# Run the script
SlotMachineEffect()
