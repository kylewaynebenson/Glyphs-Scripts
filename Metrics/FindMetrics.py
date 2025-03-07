#MenuTitle: Find Metrics
#Description: Find metrics with specific characteristics and open in tab

import vanilla
from GlyphsApp import Glyphs, GSGlyph, GSFont

class FindMetricsDialog:
    def __init__(self):
        # Window dimensions
        self.w = vanilla.FloatingWindow((300, 270), "Find Metrics")
        
        # UI elements
        y = 10
        self.w.smallerThanLabel = vanilla.TextBox((10, y, 120, 20), "Smaller than:")
        self.w.smallerThanValue = vanilla.EditText((130, y, 60, 20), "0")
        self.w.smallerThanButton = vanilla.Button((200, y, 90, 20), "Find", callback=self.findSmallerThan)
        y += 30
        # checkbox to select right side 
        self.w.smallerRightSide = vanilla.CheckBox((130, y, 280, 20), "Right side")
        # checkbox to select left side 
        self.w.smallerLeftSide = vanilla.CheckBox((10, y, 280, 20), "Left side")

        # dividing line
        y += 30
        self.w.dividingLine = vanilla.HorizontalLine((10, y, 280, 1))
        
        y += 10
        self.w.largerThanLabel = vanilla.TextBox((10, y, 120, 20), "Larger than:")
        self.w.largerThanValue = vanilla.EditText((130, y, 60, 20), "0")
        self.w.largerThanButton = vanilla.Button((200, y, 90, 20), "Find", callback=self.findLargerThan)
        y += 30
        # checkbox to select right side
        self.w.largerRightSide = vanilla.CheckBox((130, y, 280, 20), "Right side")
        # checkbox to select left side
        self.w.largerLeftSide = vanilla.CheckBox((10, y, 280, 20), "Left side")
        
        # dividing line
        y += 30
        self.w.dividingLine2 = vanilla.HorizontalLine((10, y, 280, 1))

        y += 10
        self.w.selectedGlyphsOnly = vanilla.CheckBox((10, y, 280, 20), "Selected glyphs only")

        # glyphs made only of components
        y+= 25
        self.w.onlyComponents = vanilla.CheckBox((10, y, 280, 20), "Search composite glyphs too")
        
        y += 35
        self.w.statusText = vanilla.TextBox((10, y, 280, 20), "")
        
        self.w.open()
    
    def getScope(self):
        """Determine which glyphs to check based on checkbox selections"""
        font = Glyphs.font
        selectedOnly = self.w.selectedGlyphsOnly.get()
        includeComponents = self.w.onlyComponents.get()
        
        if selectedOnly:
            glyphs = [layer.parent for layer in font.selectedLayers]
        else:
            glyphs = font.glyphs
        
        # Filter out composite glyphs if checkbox is not checked
        if not includeComponents:
            filtered_glyphs = []
            for glyph in glyphs:
                # Check if any layer has paths (not just components)
                has_paths = False
                for layer in glyph.layers:
                    if len(layer.paths) > 0:
                        has_paths = True
                        break
                
                # Include glyph if it has paths in any layer
                if has_paths:
                    filtered_glyphs.append(glyph)
            glyphs = filtered_glyphs
            
        return font, glyphs
    
    def openInTab(self, glyphNames):
        """Open the given glyph names in a new tab"""
        glyphNames = list(set(glyphNames))  # Remove duplicates
        
        if not glyphNames:
            self.w.statusText.set("No glyphs match the criteria")
            return
        
        font = Glyphs.font
        
        # Sort the glyphs in a logical order
        sorted_names = []
        glyph_data = []
        
        # First, collect data about each glyph for sorting
        for name in glyphNames:
            glyph = font.glyphs[name]
            if glyph:
                # Get the unicode value if available, otherwise use None
                unicode_val = glyph.unicode
                category = glyph.category
                subcategory = glyph.subCategory
                # Store as tuple for sorting
                glyph_data.append((name, unicode_val, category, subcategory))
        
        # Define a sort key function - similar to Glyphs' category order
        def sort_key(item):
            name, unicode_val, category, subcategory = item
            
            # Primary sort: by category (using numeric values to represent category priority)
            category_order = {
                "Letter": 1,
                "Number": 2, 
                "Punctuation": 3,
                "Symbol": 4,
                "Mark": 5,
                None: 99
            }
            
            # Secondary sort: by subcategory
            subcategory_order = {
                "Uppercase": 1,
                "Lowercase": 2,
                "Smallcaps": 3,
                "Decimal Digit": 1,
                None: 99
            }
            
            # If we have Unicode, use it for tertiary sorting
            unicode_sort = int(unicode_val, 16) if unicode_val else 0xFFFFFF
            
            return (
                category_order.get(category, 99),
                subcategory_order.get(subcategory, 99),
                unicode_sort,
                name  # Finally sort by name for consistent ordering
            )
        
        # Sort the glyph data
        glyph_data.sort(key=sort_key)
        
        # Extract the sorted names
        sorted_names = [item[0] for item in glyph_data]
        
        # Create a new tab with sorted glyphs
        newTab = font.newTab()
        formatted_names = [f"/{name}" for name in sorted_names]
        newTab.text = "".join(formatted_names)
        
        self.w.statusText.set(f"Found {len(glyphNames)} glyphs")
    
    def findSmallerThan(self, sender):
        """Find glyphs with metrics smaller than the specified value"""
        try:
            value = int(self.w.smallerThanValue.get())
            font, glyphs = self.getScope()
            
            # Get side selections
            checkLeftSide = self.w.smallerLeftSide.get()
            checkRightSide = self.w.smallerRightSide.get()
            
            # If neither is selected, check both sides (default behavior)
            if not checkLeftSide and not checkRightSide:
                checkLeftSide = True
                checkRightSide = True
            
            matchingGlyphs = []
            
            # Only check the current master
            master = font.selectedFontMaster
            
            for glyph in glyphs:
                layer = glyph.layers[master.id]
                # Only check the selected sides
                if (checkLeftSide and layer.LSB < value) or (checkRightSide and layer.RSB < value):
                    matchingGlyphs.append(glyph.name)
            
            self.openInTab(matchingGlyphs)
            
        except ValueError:
            self.w.statusText.set("Please enter a valid number")

    def findLargerThan(self, sender):
        """Find glyphs with metrics larger than the specified value"""
        try:
            value = int(self.w.largerThanValue.get())
            font, glyphs = self.getScope()
            
            # Get side selections
            checkLeftSide = self.w.largerLeftSide.get()
            checkRightSide = self.w.largerRightSide.get()
            
            # If neither is selected, check both sides (default behavior)
            if not checkLeftSide and not checkRightSide:
                checkLeftSide = True
                checkRightSide = True
            
            matchingGlyphs = []
            
            # Only check the current master
            master = font.selectedFontMaster
            
            for glyph in glyphs:
                layer = glyph.layers[master.id]
                # Only check the selected sides
                if (checkLeftSide and layer.LSB > value) or (checkRightSide and layer.RSB > value):
                    matchingGlyphs.append(glyph.name)
            
            self.openInTab(matchingGlyphs)
            
        except ValueError:
            self.w.statusText.set("Please enter a valid number")


# Run the script
FindMetricsDialog()

