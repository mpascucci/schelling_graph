import random
import string
from enum import Enum

class Colors(Enum):
    ORANGE = "orange"
    BLUE = "blue"
    CYAN = "cyan"
    PURPLE = "purple"
    BLACK = "black"
    RED = "red"
    GREEN = "green"


class Vertex():
    def __init__(self, id=None):
        # Generate a random ID if none is provided
        self.id = id if id is not None else ''.join(
            random.choices(string.ascii_letters + string.digits, k=8))
        self.edges = []

    def add_edge(self, edge):
        self.edges.append(edge)


class Schelling_Node(Vertex):
    def __init__(self, x: int, y: int, chips: int = 0, id=None, color: str = None):
        super().__init__(id)
        self.chips: int = chips  # Number of chips on the vertex
        # List of arrows originating from this vertex
        self.arrows: list[Shelling_Arrow] = []
        self.x: int = x  # X position
        self.y: int = y  # Y position
        self.color: str = color  # Color (just for visualization purposes)

    def add_arrow(self, to: 'Schelling_Node', linked_vertices: list['Schelling_Node'], color: str):
        arrow = Shelling_Arrow(to, linked_vertices, color)
        # Ensure all linked vertices have the same color as the arrow
        for v in linked_vertices:
            assert v.color == color, "All linked vertices must have the same color as the arrow."
        self.arrows.append(arrow)


class Shelling_Arrow():
    def __init__(self, to_node: Schelling_Node, linked_nodes: list[Schelling_Node], color: str):
        self.neighbor: Schelling_Node = to_node  # The neighboring vertex
        # The linked vertices
        self.out_edge_nodes: list[Schelling_Node] = linked_nodes
        # Color of the arrow (for visualization purposes)
        self.color: str = color


