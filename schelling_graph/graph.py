
from typing import Callable, MutableSequence, Type
import numpy as np
import random
from matplotlib import pyplot as plt
from schelling_graph.visualization import _draw_graph, _draw_matrix, animate_chips_matrices
from schelling_graph.structures import Schelling_Node
from schelling_graph.tools import create_vertex_matrix, get_nodes_by_color, node_matrix_2_int_matrix
from .structures import Colors
import termcolor as tc


class Schelling_Graph:
    def __init__(self, nodes: list[Schelling_Node]):
        self.nodes = nodes
        self.matrix: np.ndarray[Schelling_Node] = create_vertex_matrix(  # type: ignore
            nodes)  # type: ignore

        self.nbc = get_nodes_by_color(nodes)
        self._animation_frames = []

    @property
    def chips_matrix(self) -> np.ndarray:
        return node_matrix_2_int_matrix(self.matrix)

    @property
    def nodes_with_chips(self) -> list[Schelling_Node]:
        return [n for n in self.nodes if n.chips > 0]

    @property
    def chips(self) -> list[int]:
        return [n.chips for n in self.nodes]

    def add_arrow(self, from_node: Schelling_Node, to_vertex: Schelling_Node, color: Colors):
        c = Colors(color)
        linked_vertices = self.nbc[c]
        from_node.add_arrow(
            to=to_vertex, linked_nodes=linked_vertices, color=color)

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

    def __getitem__(self, idx) -> Schelling_Node:
        x, y = idx
        return self.matrix[x][y]  # type: ignore

    def plot_all(self, show=True):
        fig, ax = plt.subplots(1, 2, figsize=(10, 5))
        _draw_graph(self.nodes, ax=ax[0])
        _draw_matrix(self.chips_matrix, ax=ax[1])
        ax[0].set_title("Graph Representation")
        ax[1].set_title("Chips")
        if show:
            plt.show()
        return fig, ax

    def plot_chips(self, show=True, ax=None):
        fig = None
        if ax is None:
            fig, ax = plt.subplots(figsize=(5, 5))
        _draw_matrix(self.chips_matrix, ax=ax)
        if show:
            plt.show()
        return fig, ax

    def plot(self, show=True, ax=None):
        fig = None
        if ax is None:
            fig, ax = plt.subplots(figsize=(5, 5))
        _draw_graph(self.nodes, ax=ax)
        if show:
            plt.show()
        return fig, ax

    def run_one_round(self):
        run_round(self)

    def run_rounds(self, stop_when: Callable = lambda: False, max_rounds: int = 1000):
        idlecount = 0
        round_count = 0
        logs = []
        self._animation_frames = []
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
                self._animation_frames.append(self.chips_matrix.copy())

        return logs + [f"Condition satisfied, stopping simulation after {round_count} rounds."]

    def animate(self, interval=200, repeat_delay=1000):
        ani = animate_chips_matrices(
            self._animation_frames, interval, repeat_delay)
        return ani

    def init_chips_uniform(self, min=0, max=5):
        """Initialize chips uniformly between a and b (inclusive)."""
        chips = []
        for n in self.nodes:
            n.chips = random.randint(min, max)
            chips.append(n.chips)

    def init_chips_multinomial(self, pvals: list[float] | np.ndarray):
        """Initialize chips using a multinomial distribution with given probabilities.
        The length of pvals must be equal to the number of nodes.
        The sum of pvals must be 1.
        """

        assert len(pvals) == len(
            self.nodes), f"The length of pvals ({len(pvals)}) must be equal to the number of nodes ({len(self.nodes)})."
        assert abs(
            sum(pvals) - 1.0) < 1e-8, f"The sum of pvals must be 1 (with precision > 1e-8), got {sum(pvals):.8f}."

        total_number_of_chips = 100  # You can adjust this value as needed

        chips = np.random.multinomial(n=total_number_of_chips, pvals=pvals)

        for i, n in enumerate(self.nodes):
            n.chips = chips[i]

    def set_chips(self, chips: MutableSequence[int], randomize: bool = False):
        """Initialize chips assigning values from the given list.
        The values are assigned uniformly at random from the list.  
        The length of samples must be equal to the number of nodes.

        If randomize is False, the values are assigned in the order of the nodes list of this graph.
        """
        assert len(chips) == len(
            self.nodes), "The length of samples must be equal to the number of nodes"

        if randomize:
            random.shuffle(chips)

        for i, n in enumerate(self.nodes):
            n.chips = chips[i]

    def is_segregated(self) -> bool:
        """Check if the graph is segregated.
        A graph is segregated if chips are only on boundary nodes (0,n) or (n,0).
        """
        for n in self.nodes_with_chips:
            if n.x != 0 and n.y != 0:
                return False
        return True

    def __repr__(self) -> str:
        return f"Schelling_Graph with {len(self.nodes)} nodes."

    def copy(self):
        """Create a deep copy of the graph."""
        node_map = {}
        new_nodes = []
        for node in self.nodes:
            new_node = Schelling_Node(x=node.x, y=node.y, color=node.color)
            new_node.chips = node.chips
            node_map[node] = new_node
            new_nodes.append(new_node)

        new_graph = Schelling_Graph(new_nodes)

        for node in self.nodes:
            new_node = node_map[node]
            for arrow in node.arrows:
                neighbor = node_map[arrow.neighbor]
                linked_nodes = [
                    node_map[n] for n in arrow.out_edge_nodes]
                new_node.add_arrow(
                    to=neighbor, linked_nodes=linked_nodes, color=arrow.color)

        return new_graph


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
