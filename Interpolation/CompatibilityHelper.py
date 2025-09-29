#MenuTitle: Compatibility Helper
# -*- coding: utf-8 -*-
__doc__="""
Analyzes the current glyph for compatibility issues and reports them in the Macro Panel.
Checks for:
- Masters with different path counts than others
- Masters missing anchors that a majority have
- Intermediate layers with duplicate names
"""

from GlyphsApp import Glyphs

def check_path_counts(glyph):
	"""Check if all masters have the same number of paths."""
	issues = []
	
	# Get path counts for each master layer
	master_path_counts = {}
	for layer in glyph.layers:
		if layer.isMasterLayer or layer.isSpecialLayer:
			master_name = layer.name if layer.name else layer.associatedMasterId
			path_count = len(layer.paths)
			master_path_counts[master_name] = path_count
	
	if not master_path_counts:
		return issues
	
	# Find the most common path count
	path_counts = list(master_path_counts.values())
	most_common_count = max(set(path_counts), key=path_counts.count)
	
	# Report masters that differ
	for master_name, count in master_path_counts.items():
		if count != most_common_count:
			issues.append(f"  ⚠️  Master '{master_name}' has {count} path(s), expected {most_common_count}")
	
	return issues

def check_anchors(glyph):
	"""Check if all masters have the same anchors."""
	issues = []
	
	# Collect anchor names for each master layer
	master_anchors = {}
	for layer in glyph.layers:
		if layer.isMasterLayer or layer.isSpecialLayer:
			master_name = layer.name if layer.name else layer.associatedMasterId
			anchor_names = set([anchor.name for anchor in layer.anchors])
			master_anchors[master_name] = anchor_names
	
	if not master_anchors:
		return issues
	
	# Find all unique anchor names across masters
	all_anchor_names = set()
	for anchor_set in master_anchors.values():
		all_anchor_names.update(anchor_set)
	
	if not all_anchor_names:
		return issues
	
	# For each anchor, check if majority of masters have it
	num_masters = len(master_anchors)
	majority_threshold = num_masters / 2.0
	
	for anchor_name in all_anchor_names:
		masters_with_anchor = [master for master, anchors in master_anchors.items() if anchor_name in anchors]
		masters_without_anchor = [master for master, anchors in master_anchors.items() if anchor_name not in anchors]
		
		# If majority have it but some don't, report the ones missing it
		if len(masters_with_anchor) > majority_threshold and masters_without_anchor:
			for master_name in masters_without_anchor:
				issues.append(f"  ⚠️  Master '{master_name}' is missing anchor '{anchor_name}' (present in {len(masters_with_anchor)}/{num_masters} masters)")
	
	return issues

def check_duplicate_intermediate_names(glyph):
	"""Check for intermediate layers with duplicate names."""
	issues = []
	
	# Collect intermediate layer names
	intermediate_layers = {}
	for layer in glyph.layers:
		# Intermediate layers are neither master nor special layers
		if not layer.isMasterLayer and not layer.isSpecialLayer:
			layer_name = layer.name
			if layer_name:
				if layer_name not in intermediate_layers:
					intermediate_layers[layer_name] = []
				intermediate_layers[layer_name].append(layer)
	
	# Report duplicates
	for layer_name, layers in intermediate_layers.items():
		if len(layers) > 1:
			issues.append(f"  ⚠️  Duplicate intermediate layer name '{layer_name}' found {len(layers)} times")
	
	return issues

def main():
	font = Glyphs.font
	
	if not font:
		print("⛔️ No font open")
		return
	
	# Get current glyph
	current_tab = font.currentTab
	if not current_tab:
		print("⛔️ No tab open")
		return
	
	layers = current_tab.layers
	if not layers:
		print("⛔️ No glyph selected")
		return
	
	glyph = layers[0].parent
	
	print(f"\n{'='*60}")
	print(f"Compatibility Check: {glyph.name}")
	print(f"{'='*60}\n")
	
	# Run all checks
	path_issues = check_path_counts(glyph)
	anchor_issues = check_anchors(glyph)
	duplicate_issues = check_duplicate_intermediate_names(glyph)
	
	# Report results
	has_issues = False
	
	if path_issues:
		has_issues = True
		print("PATH COUNT ISSUES:")
		for issue in path_issues:
			print(issue)
		print()
	
	if anchor_issues:
		has_issues = True
		print("ANCHOR ISSUES:")
		for issue in anchor_issues:
			print(issue)
		print()
	
	if duplicate_issues:
		has_issues = True
		print("DUPLICATE INTERMEDIATE LAYER NAMES:")
		for issue in duplicate_issues:
			print(issue)
		print()
	
	if not has_issues:
		print("✅ No compatibility issues found!")
	else:
		print(f"{'='*60}")
		print(f"Found {len(path_issues) + len(anchor_issues) + len(duplicate_issues)} issue(s)")
		print(f"{'='*60}")
	
	print()

if __name__ == "__main__":
	main()
