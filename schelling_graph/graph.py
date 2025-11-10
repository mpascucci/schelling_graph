
from typing import Callable
import numpy as np
import random
from matplotlib import pyplot as plt
from schelling_graph.visualization import _draw_graph, _draw_matrix
from schelling_graph.structures import Schelling_Node
from schelling_graph.tools import create_vertex_matrix, get_nodes_by_color
from .structures import Colors
import termcolor as tc



class Schelling_Graph:
    def __init__(self, nodes: list[Schelling_Node]):
        self.nodes = nodes
        self.matrix = create_vertex_matrix(nodes)
        self.nbc = get_nodes_by_color(nodes)

    @property
    def nodes_with_chips(self) -> list[Schelling_Node]:
        return [n for n in self.nodes if n.chips > 0]

    def add_arrow(self, from_vertex: Schelling_Node, to_vertex: Schelling_Node, color: str):
        c = Colors(color)
        linked_vertices = self.nbc[c]
        from_vertex.add_arrow(
            to=to_vertex, linked_vertices=linked_vertices, color=color)

    def is_coherent(self) -> bool:
        max_x = max(v.x for v in self.nodes)
        max_y = max(v.y for v in self.nodes)
        # A graph is coherent for all arrows if
        # for very node n, all the nodes linked to the arrows originating from n
        # have at least one arrow of the same color of n
        # unless the neighbor is at the boundary (x=0, x=max_x, y=0, y=max_y)
        for node in self.nodes:
            for arrow in node.arrows:
                neighbor = arrow.neighbor
                if neighbor.x == max_x or neighbor.y == max_y:
                    continue
                for out_node in arrow.out_edge_nodes:
                    if not any(a.color == node.color for a in out_node.arrows):
                        print(
                            f"Graph is not coherent at node ({node.x},{node.y}) with arrow to ({neighbor.x},{neighbor.y}) of color {arrow.color}")
                        return False

        return True

    def get_node(self, x: int, y: int) -> Schelling_Node:
        return self.matrix[x][y]

    def __getitem__(self, idx):
        x, y = idx
        return self.matrix[x][y]

    def plot(self, show=True):
        fig, ax = plt.subplots(1, 2, figsize=(10, 5))
        _draw_matrix(self.matrix, ax=ax[0])
        _draw_graph(self.nodes, ax=ax[1])
        if show:
            plt.show()
        return fig, ax

    def run_one_round(self):
        run_round(self)

    def run_rounds(self, stop_when: Callable = lambda: False, max_rounds: int = 1000):
        idlecount = 0
        round_count = 0
        logs = []
        while not stop_when() and round_count < max_rounds:
            round_count += 1
            done, s = run_round(self)
            if not done:
                idlecount += 1
            else:
                if idlecount > 0:
                    logs.append(
                        f"Idle ({idlecount} round{'s' if idlecount > 1 else ''}).")
                    idlecount = 0
                logs.append(s)

        return logs + [f"Condition satisfied, stopping simulation after {round_count} rounds."]

    def init_chips_uniform(self, a=0, b=5):
        """Initialize chips uniformly between a and b (inclusive)"""
        for n in self.nodes:
            n.chips = random.randint(a, b)

    def init_chips_with_sample(self, samples: list[int]):
        """Initialize chips assigning values from the given list.
        The values are assigned uniformly at random from the list.
        The length of samples must be equal to the number of nodes.
        """
        assert len(samples) == len(
            self.nodes), "The length of samples must be equal to the number of nodes"

        idxs = list(range(len(samples)))
        for n in self.nodes:
            # pop an item from samples at random
            i = random.choice(idxs)
            idxs.remove(i)
            n.chips = samples[i]

    def is_segregated(self) -> bool:
        """Check if the graph is segregated.
        A graph is segregated if chips are only on boundary nodes (0,n) or (n,0).
        """
        for n in self.nodes_with_chips:
            if n.x != 0 and n.y != 0:
                return False
        return True


def move_chips(node, arrow, out_node):
    """Move chips from node to arrow.neighbor and from out_node to out_arrow.neighbor"""
    # move chip of node
    node.chips -= 1
    arrow.neighbor.chips += 1

    # chose an arrow from out_node with the same color as node
    out_arrow = [v for v in out_node.arrows if v.color == node.color]
    if len(out_arrow) == 0:
        # out_node must have exactly one arrow with the same color as node
        return

    out_arrow = out_arrow[0]

    # move chip along the arrow
    out_node.chips -= 1
    out_arrow.neighbor.chips += 1

    s = (f"({node.x},{node.y})" +
         tc.colored(" ---> ", arrow.color) +
         f"({arrow.neighbor.x},{arrow.neighbor.y})" +
         f" & ({out_node.x},{out_node.y}) " +
         tc.colored(f" ---> ", out_arrow.color) +
         f"({out_arrow.neighbor.x},{out_arrow.neighbor.y}).")

    return s


def run_round(schelling_graph: Schelling_Graph):
    # sample a node with uniform distribution, if it has no chips, sample again
    node = random.choice(schelling_graph.nodes_with_chips)

    # choose an arrow with uniform distribution
    # candidate arrows have out_nodes with chips > 0
    candidate_arrows = [a for a in node.arrows if any(
        n.chips > 0 for n in a.out_edge_nodes)]

    # assert len(candidate_arrows) > 0, "No candidate arrows with out_nodes having chips > 0"
    if len(candidate_arrows) == 0:
        return (False, "idle")

    arrow = random.choice(candidate_arrows)

    candidates = [n for n in arrow.out_edge_nodes if n.chips > 0]

    out_node = None
    if len(candidates) > 0:
        out_node = random.choice(candidates)

    # if out_node is the same as node and node has less than 2 chips, re-sample
    if out_node == node and node.chips < 2:
        out_node = None

    if out_node is not None:
        s = move_chips(node, arrow, out_node)
        return (True, s)

    return (False, "idle")
