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


class Node():
    def __init__(self, id=None):
        # Generate a random ID if none is provided
        self.id = id if id is not None else ''.join(
            random.choices(string.ascii_letters + string.digits, k=8))
        self.edges = []

    def add_edge(self, edge):
        self.edges.append(edge)


class Schelling_Node(Node):
    def __init__(self, x: int, y: int, chips: int = 0, id=None, color: Colors = Colors.BLACK):
        super().__init__(id)
        self.chips: int = chips  # Number of chips on the node
        # List of arrows originating from this node
        self.arrows: list[Schelling_Arrow] = []
        self.x: int = x  # X position
        self.y: int = y  # Y position
        self.color: Colors = color  # Color

    def add_arrow(self, to: 'Schelling_Node', linked_nodes: list['Schelling_Node'], color: Colors):
        arrow = Schelling_Arrow(to, linked_nodes, color)
        # Ensure all linked nodes have the same color as the arrow
        for v in linked_nodes:
            assert v.color == color, "All linked nodes must have the same color as the arrow."
        self.arrows.append(arrow)


class Schelling_Arrow():
    def __init__(self, to_node: Schelling_Node, linked_nodes: list[Schelling_Node], color: Colors = Colors.BLACK):
        self.neighbor: Schelling_Node = to_node  # The neighboring node
        # The linked nodes connected by this arrow
        self.out_edge_nodes: list[Schelling_Node] = linked_nodes
        # Color of the arrow
        self.color: Colors = color
