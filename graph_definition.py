
#%% IMPORTS
import schelling_graph as sg
import numpy as np
C = sg.Colors

#%% VERTICES =====================================================

vertices = [
    sg.Schelling_Node(x=0, y=3, chips=0, color=C.BLACK),
    sg.Schelling_Node(x=0, y=2, chips=0, color=C.RED),
    sg.Schelling_Node(x=0, y=1, chips=0, color=C.RED),
    sg.Schelling_Node(x=0, y=0, chips=0, color=C.ORANGE),
    sg.Schelling_Node(x=1, y=2, chips=0, color=C.PURPLE),
    sg.Schelling_Node(x=1, y=1, chips=0, color=C.BLUE),
    sg.Schelling_Node(x=1, y=0, chips=0, color=C.CYAN),
    sg.Schelling_Node(x=2, y=1, chips=0, color=C.GREEN),
    sg.Schelling_Node(x=2, y=0, chips=0, color=C.CYAN),
    sg.Schelling_Node(x=3, y=0, chips=0, color=C.BLACK),
]

g = sg.Schelling_Graph(vertices)


#%% GIVE CHIPS =====================================================
# give chips
# for v in vertices:
#     v.chips = random.randint(1, 2)

g[1,2].chips = 1
g[0,0].chips = 1

#%% ARROWS =====================================================
g.add_arrow(g[0,0], g[0,1], color=C.BLUE)
g.add_arrow(g[0,0], g[0,1], color=C.GREEN)
g.add_arrow(g[0,0], g[1,0], color=C.BLUE)
g.add_arrow(g[0,0], g[1,0], color=C.PURPLE)

g.add_arrow(g[0,1], g[0,2], color=C.BLUE)
g.add_arrow(g[0,1], g[0,2], color=C.GREEN)

g.add_arrow(g[0,2], g[0,3], color=C.BLUE)
g.add_arrow(g[0,2], g[0,3], color=C.GREEN)

g.add_arrow(g[1,2], g[0,2], color=C.BLUE)
g.add_arrow(g[1,2], g[0,2], color=C.ORANGE)
g.add_arrow(g[1,2], g[0,2], color=C.CYAN)

g.add_arrow(g[1,1], g[1,2], color=C.BLUE)
g.add_arrow(g[1,1], g[0,1], color=C.BLUE)
g.add_arrow(g[1,1], g[2,1], color=C.BLUE)
g.add_arrow(g[1,1], g[1,0], color=C.BLUE)
g.add_arrow(g[1,1], g[1,1], color=C.BLUE)
g.add_arrow(g[1,1], g[1,0], color=C.RED)
g.add_arrow(g[1,1], g[1,0], color=C.ORANGE)
g.add_arrow(g[1,1], g[1,2], color=C.GREEN)
g.add_arrow(g[1,1], g[0,1], color=C.CYAN)
g.add_arrow(g[1,1], g[0,1], color=C.ORANGE)
g.add_arrow(g[1,1], g[2,1], color=C.PURPLE)

g.add_arrow(g[2,1], g[2,0], color=C.BLUE)
g.add_arrow(g[2,1], g[2,0], color=C.RED)
g.add_arrow(g[2,1], g[2,0], color=C.ORANGE)

g.add_arrow(g[1,0], g[2,0], color=C.BLUE)
g.add_arrow(g[1,0], g[2,0], color=C.PURPLE)

g.add_arrow(g[2,0], g[3,0], color=C.BLUE)
g.add_arrow(g[2,0], g[3,0], color=C.PURPLE)



