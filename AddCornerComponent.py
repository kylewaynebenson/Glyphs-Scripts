# MenuTitle: Add Corner Component
# -*- coding: utf-8 -*-
__doc__="""
Adds a selected corner component to the selected node(s) in Glyphs 3.
If multiple nodes are selected, it first applies the "sharpen corner" function.
Option to apply on all compatible masters.
"""

import GlyphsApp
from GlyphsApp import CORNER
from vanilla import *

class AddCornerComponentDialog(object):

    def __init__(self):
        # Get available corner components
        self.corner_components = [g.name for g in Glyphs.font.glyphs if g.name.startswith("_corner.")]
        
        # Set up the dialog
        self.w = FloatingWindow((300, 320), "Add Corner Component")
        self.w.componentList = List((10, 10, -10, -90), self.corner_components, selectionCallback=self.on_selection)
        self.w.allMasters = CheckBox((10, -80, -10, 20), "Apply on all masters", value=True)
        self.w.closeAfter = CheckBox((10, -60, -10, 20), "Close popup after running", value=True)
        self.w.applyButton = Button((10, -30, -10, 20), "Apply", callback=self.apply_corner)
        self.w.center()
        self.w.open()
        
        self.selected_component = None

    def on_selection(self, sender):
        selection = sender.getSelection()
        if selection:
            self.selected_component = self.corner_components[selection[0]]
        else:
            self.selected_component = None

    def get_path_index(self, layer, path):
        for index, p in enumerate(layer.paths):
            if p == path:
                return index
        return -1

    def get_corresponding_nodes(self, glyph, active_layer, selected_nodes):
        corresponding_nodes = {}
        for layer in glyph.layers:
            if layer == active_layer:
                corresponding_nodes[layer.layerId] = selected_nodes
                continue
            
            layer_nodes = []
            for active_node in selected_nodes:
                active_path = active_node.parent
                active_path_index = self.get_path_index(active_layer, active_path)
                active_node_index = active_node.index
                
                if active_path_index != -1 and active_path_index < len(layer.paths):
                    corresponding_path = layer.paths[active_path_index]
                    if active_node_index < len(corresponding_path.nodes):
                        layer_nodes.append(corresponding_path.nodes[active_node_index])
            
            if layer_nodes:
                corresponding_nodes[layer.layerId] = layer_nodes
        
        return corresponding_nodes

    def apply_corner(self, sender):
        if not self.selected_component:
            print("No corner component selected")
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
        selected_nodes = [node for path in active_layer.paths for node in path.nodes if node.selected]

        if not selected_nodes:
            print("No nodes selected")
            return

        all_masters = self.w.allMasters.get()
        
        if all_masters:
            corresponding_nodes = self.get_corresponding_nodes(glyph, active_layer, selected_nodes)
        else:
            corresponding_nodes = {active_layer.layerId: selected_nodes}

        # Apply sharpening first if multiple nodes are selected
        if len(selected_nodes) > 1:
            for layer_id, nodes in corresponding_nodes.items():
                layer = glyph.layers[layer_id]
                layer.parent.beginUndo()
                currentController = Glyphs.font.parent.windowController()
                if currentController:
                    tool = currentController.toolEventHandler()
                    if tool.__class__.__name__ == "GlyphsToolSelectNormal":
                        path = nodes[0].parent  # Get the path of the first selected node
                        startIdx = nodes[0].index  # Get the index of the first selected node
                        endIdx = nodes[-1].index  # Get the index of the last selected node
                        tool._makeCorner_firstNodeIndex_endNodeIndex_(path, startIdx, endIdx)
                    else:
                        print(f"Current tool is not the normal selection tool in layer {layer.name}")
                else:
                    print(f"No current controller found for layer {layer.name}")
                layer.parent.endUndo()

            # Update corresponding_nodes with the sharpened node
            active_sharpened_node = [node for path in active_layer.paths for node in path.nodes if node.selected]
            if active_sharpened_node:
                corresponding_nodes = self.get_corresponding_nodes(glyph, active_layer, active_sharpened_node)
            else:
                print("Warning: No node remained selected after sharpening in the active layer")
                return
        # Add the corner component if there is one node selected per master

        for layer_id, nodes in corresponding_nodes.items():
            layer = glyph.layers[layer_id]
            if len(nodes) == 1:
                for node in nodes:
                    new_corner = GSHint()
                    new_corner.type = CORNER
                    new_corner.name = self.selected_component
                    new_corner.originNode = node
                    layer.hints.append(new_corner)
            else:
                print(f"Warning: sharpen corner failed, sharpen corners manually then try again.")

            print(f"Added corner component '{self.selected_component}' to {len(nodes)} node(s) in layer {layer.name}")

        if self.w.closeAfter.get():
            self.w.close()

AddCornerComponentDialog()