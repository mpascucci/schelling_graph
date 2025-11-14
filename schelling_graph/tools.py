
import numpy as np
from schelling_graph.structures import Schelling_Node, Colors


def get_nodes_by_color(vertices: list[Schelling_Node]) -> dict[Colors, list[Schelling_Node]]:
    vertices_by_color = {
        color: [v for v in vertices if v.color == color]
        for color in Colors
    }
    return vertices_by_color


def get_vertex_at_position(x: int, y: int, vertices: list[Schelling_Node]) -> Schelling_Node | None:
    for node in vertices:
        if node.x == x and node.y == y:
            return node
    return None


def create_vertex_matrix(vertices: list[Schelling_Node]) -> np.ndarray[Schelling_Node]:
    dim = 4
    # Create a matrix to hold the vertices based on their (x, y) positions
    m = np.zeros((dim, dim), dtype=Schelling_Node)
    for node in vertices:
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
