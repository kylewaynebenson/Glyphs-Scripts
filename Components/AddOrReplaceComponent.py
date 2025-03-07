# MenuTitle: Add or Replace with Component
# -*- coding: utf-8 -*-
__doc__="""
Replaces selected path or component with a new component in Glyphs 3.
Options for automatic alignment, applying on all masters, and searching through all available glyphs.
"""

import GlyphsApp
from vanilla import *

class AddReplaceComponentDialog(object):

    def __init__(self):
        # Get all available glyphs
        self.all_glyphs = sorted([g.name for g in Glyphs.font.glyphs])
        
        # Set up the dialog
        self.w = FloatingWindow((300, 400), "Add or Replace with Component")
        self.w.search = SearchBox((10, 10, -10, 20), callback=self.search_callback)
        self.w.componentList = List((10, 40, -10, -90), self.all_glyphs, selectionCallback=self.on_selection)
        self.w.autoAlign = CheckBox((10, -80, -10, 20), "Enable automatic alignment", value=True)
        self.w.allMasters = CheckBox((10, -60, -10, 20), "Apply on all masters", value=True)
        self.w.closeAfter = CheckBox((10, -40, -10, 20), "Close popup after running", value=True)
        self.w.applyButton = Button((10, -30, -10, 20), "Apply", callback=self.apply_component)
        self.w.center()
        self.w.open()
        
        self.selected_component = None

    def search_callback(self, sender):
        search_text = sender.get().strip()
        if search_text.endswith(" "):
            # Exact match if the search ends with a space
            exact_matches = [g for g in self.all_glyphs if g.lower() == search_text.lower().strip()]
            partial_matches = [g for g in self.all_glyphs if g.lower().startswith(search_text.lower().strip()) and g not in exact_matches]
            filtered_glyphs = exact_matches + partial_matches
        else:
            # Prioritize glyphs that start with the search text, then include partial matches
            starts_with = [g for g in self.all_glyphs if g.lower().startswith(search_text.lower())]
            contains = [g for g in self.all_glyphs if search_text.lower() in g.lower() and g not in starts_with]
            filtered_glyphs = starts_with + contains
        self.w.componentList.set(filtered_glyphs)

    def on_selection(self, sender):
        selection = sender.getSelection()
        if selection:
            self.selected_component = sender.get()[selection[0]]
        else:
            self.selected_component = None

    def get_selected_shape_index(self, layer):
        for i, shape in enumerate(layer.shapes):
            if shape.selected:
                return i
        return -1

    def apply_component(self, sender):
        if not self.selected_component:
            print("No component selected")
            return

        font = Glyphs.font
        if not font:
            print("No font open")
            return

        glyph = font.selectedLayers[0].parent
        if not glyph:
            print("No glyph selected")
            return

        active_layer = font.selectedLayers[0]
        selected_shape_index = self.get_selected_shape_index(active_layer)

        if selected_shape_index == -1:
            print("No shape selected")
            return

        all_masters = self.w.allMasters.get()
        auto_align = self.w.autoAlign.get()

        layers_to_process = glyph.layers if all_masters else [active_layer]

        for layer in layers_to_process:
            if selected_shape_index < len(layer.shapes):
                shape_to_replace = layer.shapes[selected_shape_index]
                
                # Get the bounds of the shape to replace
                bounds = shape_to_replace.bounds

                # Remove the shape
                del layer.shapes[selected_shape_index]

                # Add new component
                new_component = GSComponent(self.selected_component)
                layer.shapes.append(new_component)

                if auto_align:
                    new_component.automaticAlignment = True
                else:
                    # Center the new component where the old shape was
                    new_bounds = new_component.bounds
                    new_component.position = (
                        bounds.origin.x + (bounds.size.width - new_bounds.size.width) / 2,
                        bounds.origin.y + (bounds.size.height - new_bounds.size.height) / 2
                    )

                print(f"Replaced shape with component '{self.selected_component}' in layer {layer.name}")
            else:
                print(f"No corresponding shape found in layer {layer.name}")

        if self.w.closeAfter.get():
            self.w.close()

AddReplaceComponentDialog()
