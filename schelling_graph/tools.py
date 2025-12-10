import csv
import numpy as np
from schelling_graph.structures import Schelling_Node, VALID_COLORS
from scipy.special import binom


def get_nodes_by_color(vertices: list[Schelling_Node]) -> dict[str, list[Schelling_Node]]:
    vertices_by_color = {
        color: [v for v in vertices if v.color == color]
        for color in VALID_COLORS
    }
    return vertices_by_color


def get_vertex_at_position(x: int, y: int, vertices: list[Schelling_Node]) -> Schelling_Node | None:
    for node in vertices:
        if node.x == x and node.y == y:
            return node
    return None


def is_color_valid(color: str) -> bool:
    return color in VALID_COLORS


def create_vertex_matrix(nodes: list[Schelling_Node]) -> np.ndarray[Schelling_Node]:
    dim = np.ceil(np.sqrt(len(nodes))).astype(int) + 1
    # Create a matrix to hold the vertices based on their (x, y) positions
    m = np.zeros((dim, dim), dtype=Schelling_Node)
    for node in nodes:
        # Ensure no two vertices occupy the same position
        assert not m[node.x,
                     node.y], f"Two vertices cannot occupy the same position {(node.x, node.y)}."
        m[node.x, node.y] = node
    return m  # type: ignore


def node_matrix_2_int_matrix(node_matrix) -> np.ndarray:
    """Converts a matrix of Schelling_Node objects to a matrix of their chips counts."""
    m = np.zeros(node_matrix.shape, dtype=int)
    for i, row in enumerate(node_matrix):
        for j, n in enumerate(row):
            if isinstance(n, Schelling_Node):
                m[i, j] = n.chips
    return m


def load_nodes_from_csv(path: str) -> list[Schelling_Node]:
    nodes = list()
    with open(path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|', )
        cols = [int(x) for x in next(spamreader)[0].split()]

        for row in spamreader:
            cells = row[0].split()
            r = int(cells.pop(0))
            for i, cell in enumerate(cells):
                node = Schelling_Node(x=cols[i], y=r, chips=0, color=cell)
                nodes.append(node)

    return nodes


def multinomial(s, a, b):
    """Calculates the multinomial coefficient for given s, a, b."""
    return binom(s, a)*binom(s-a, b)


def calc_multinomial_pvals(p, q, s):
    """Calculates multinomial probability values for given p, q, s (s=size)."""
    pvals = dict()
    for a in range(s+1):
        for b in range(s+1):
            if (a+b > s):
                continue
            pval = multinomial(s, a, b)*(p**a)*((1-p)**b) * \
                (q**(s-a-b))*((1-q)**(a+b))
            pvals[(a, b)] = pval
    return pvals


# %% ARROWS =====================================================
def auto_arrows(graph, tau, log=False):
    """Automatically creates arrows in the graph based.

    tau: tollerance (tolerant=0 < tau < intollerant=1)
    graph: Schelling_Graph object
    log: if True, prints the created arrows.
    """
    s = graph.matrix.shape[0]-1  # coordinata massima del grafo (dek palazzo)
    τ = tau
    for node in graph.nodes:
        a = node.x
        b = node.y

        # s = b/(a+b) if (a+b)!=0 else 1

        # crea le frecce del colore del node
        for other in graph.nodes:
            c = other.x
            d = other.y

            # c'è sempre una freccia di colore di (0,0)
            r = d/(c+d) if (c+d) != 0 else 1
            w = c/(c+d) if (c+d) != 0 else 1

            # non uscire dal grafo
            if c+d >= s:
                continue

            # freccia giu
            if (b-1 >= 0) and (d+1 <= s) and (b/(a+b) < τ) and (b/(a+b) <= r):
                if log:
                    print(
                        f"a,b({a}, {b}) {node.color} --{other.color}--> a,b-1({a}, {b-1}) {g[a, b-1].color}")
                    print(
                        f"c,d({c}, {d}) {other.color} --{node.color}--> c,d+1({c}, {d+1}) {g[c, d+1].color}")
                    print()

                graph.add_arrow(graph[a, b], graph[a, b-1],
                                out_edge_node=graph[c, d])
                graph.add_arrow(graph[c, d], graph[c, d+1],
                                out_edge_node=graph[a, b])

            # freccia sinistra
            if (a-1 >= 0) and (c+1 <= s) and (a/(a+b) < τ) and (a/(a+b) <= w):
                if log:
                    print(
                        f"a,b({a}, {b}) {node.color} --{other.color}--> a,b-1({a}, {b-1}) {graph[a, b-1].color}")
                    print(
                        f"c,d({c}, {d}) {other.color} --{node.color}--> c,d+1({c}, {d+1}) {graph[c, d+1].color}")
                    print()

                graph.add_arrow(graph[a, b], graph[a-1, b],
                                out_edge_node=graph[c, d])
                graph.add_arrow(graph[c, d], graph[c+1, d],
                                out_edge_node=graph[a, b])
