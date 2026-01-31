# MenuTitle: Reorder Axis Location Parameter
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Reorders the Axis Location custom parameter in all instances to match the font-level axis order.
This fixes instances that have outdated axis ordering after changing the font-level axis order.
"""

try:
	from Foundation import NSMutableArray
except ImportError:
	NSMutableArray = None

from GlyphsApp import Glyphs, GSProjectDocument


def getFontAxisOrder():
	"""Get the current font-level axis order as a list."""
	font = Glyphs.font
	if not font or not font.axes:
		return None
	return [axis.name for axis in font.axes]


def getInstances():
	"""Get instances from project or font."""
	try:
		frontmostDoc = Glyphs.orderedDocuments()[0]
		if isinstance(frontmostDoc, GSProjectDocument):
			return frontmostDoc.instances()
		elif Glyphs.font:
			return Glyphs.font.instances
	except:
		pass
	return None


def getAxisLocationParameter(instance):
	"""Get the Axis Location parameter from an instance."""
	return instance.customParameters["Axis Location"]


def reorderAxisLocation(axisLocation, fontAxisOrder):
	"""
	Reorder the axis location array to match the font axis order.
	
	Args:
		axisLocation: The current Axis Location parameter (array of dicts)
		fontAxisOrder: List of axis names in the desired order
	
	Returns:
		Reordered axis location array
	"""
	if not axisLocation or not fontAxisOrder:
		return axisLocation
	
	# Convert to list if it's not already
	if hasattr(axisLocation, "__iter__"):
		axisLocationList = list(axisLocation)
	else:
		return axisLocation
	
	# Create a dictionary mapping axis names to their location data
	axisDict = {}
	for item in axisLocationList:
		if isinstance(item, dict) or str(type(item)).find('Dictionary') != -1:
			if 'Axis' in item:
				axisDict[item['Axis']] = item
	
	# Rebuild the array in the correct order
	reorderedLocation = []
	for axisName in fontAxisOrder:
		if axisName in axisDict:
			reorderedLocation.append(axisDict[axisName])
	
	# Add any axes that weren't in the font order (shouldn't happen, but just in case)
	for item in axisLocationList:
		if isinstance(item, dict) or str(type(item)).find('Dictionary') != -1:
			if 'Axis' in item and item['Axis'] not in fontAxisOrder:
				reorderedLocation.append(item)
	
	return reorderedLocation


def main():
	"""Main function to reorder Axis Location parameters."""
	try:
		# Check if we have a font open
		font = Glyphs.font
		if not font:
			print("❌ No font open")
			return
		
		if not font.axes:
			print("❌ No axes defined in font")
			return
		
		# Get font axis order and instances
		fontAxisOrder = getFontAxisOrder()
		instances = getInstances()
		
		if not instances:
			print("❌ No instances found")
			return
		
		print("=== Reordering Axis Location Parameters ===")
		print(f"Font axis order: {' → '.join(fontAxisOrder)}")
		print()
		
		changesCount = 0
		
		# Process all instances (including inactive ones)
		for instance in instances:
			axisLocation = getAxisLocationParameter(instance)
			if axisLocation:
				# Get current order for comparison
				currentOrder = []
				for item in axisLocation:
					if isinstance(item, dict) or str(type(item)).find('Dictionary') != -1:
						if 'Axis' in item:
							currentOrder.append(item['Axis'])
				
				# Only reorder if needed
				if currentOrder != fontAxisOrder:
					reorderedLocation = reorderAxisLocation(axisLocation, fontAxisOrder)
					
					# Update the instance parameter
					if NSMutableArray:
						# Use NSMutableArray if available for better compatibility
						instance.customParameters["Axis Location"] = NSMutableArray.arrayWithArray_(reorderedLocation)
					else:
						# Fallback to regular list
						instance.customParameters["Axis Location"] = reorderedLocation
					
					print(f"✓ {instance.name}: reordered from [{' → '.join(currentOrder)}] to [{' → '.join(fontAxisOrder)}]")
					changesCount += 1
				else:
					print(f"- {instance.name}: already in correct order")
			else:
				print(f"- {instance.name}: no Axis Location parameter")
		
		print()
		if changesCount > 0:
			print(f"🎉 Successfully reordered {changesCount} instance(s)")
		else:
			print("✅ No changes needed - all instances already match the font axis order")

	except Exception as e:
		Glyphs.showMacroWindow()
		print(f"❌ Reorder Axis Location Parameter Error: {e}")
		import traceback
		print(traceback.format_exc())


# Run the script
if __name__ == "__main__":
	main()