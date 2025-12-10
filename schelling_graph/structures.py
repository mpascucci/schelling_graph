import random
import string
import matplotlib.colors as mcolors

VALID_COLORS = tuple(mcolors.CSS4_COLORS.keys())


class Node():
    def __init__(self, id=None):
        # Generate a random ID if none is provided
        self.id = id if id is not None else ''.join(
            random.choices(string.ascii_letters + string.digits, k=8))
        self.edges = []

    def add_edge(self, edge):
        self.edges.append(edge)


class Schelling_Node(Node):
    def __init__(self, x: int, y: int, chips: int = 0, id=None, color: str = 'black'):
        super().__init__(id)

        self.chips: int = chips  # Number of chips on the node
        # List of arrows originating from this node
        self.arrows: list[Schelling_Arrow] = []
        self.x: int = x  # X position
        self.y: int = y  # Y position
        self.color: str = color  # Color

    def add_arrow(self, to: 'Schelling_Node', out_edge_node: 'Schelling_Node'):
        arrow = Schelling_Arrow(to, out_edge_node)
        self.arrows.append(arrow)

    def __repr__(self):
        return f"Schelling_Node ({self.x}, {self.y}) {self.color} c={self.chips} "


class Schelling_Arrow():
    def __init__(self, to_node: 'Schelling_Node', out_edge_node: 'Schelling_Node'):
        self.neighbor: 'Schelling_Node' = to_node  # The neighboring node
        # The linked nodes connected by this arrow
        self.out_edge_node: 'Schelling_Node' = out_edge_node

    @property
    def color(self) -> str:
        return self.out_edge_node.color

    def __repr__(self):
        return f"Schelling_Arrow to ({self.neighbor.x} --{self.out_edge_node.color}--> {self.neighbor.y}), out_edge_node: {self.out_edge_node}"
