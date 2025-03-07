#MenuTitle: Make Node First
#Created by Kyle Wayne Benson
#Created this script so that I could assign a keyboard shortcut to this right-click function
# -*- coding: utf-8 -*-
sel = Layer.selection
if len(sel) == 1 and type(sel[0]) == GSNode:
	sel[0].makeNodeFirst()
