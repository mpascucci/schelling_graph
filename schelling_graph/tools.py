
import numpy as np
from schelling_graph.structures import Schelling_Node, Colors


def get_nodes_by_color(vertices: list[Schelling_Node]) -> dict[Colors, list[Schelling_Node]]:
    vertices_by_color = {
        color: [v for v in vertices if v.color == color]
        for color in Colors
    }
    return vertices_by_color


def get_vertex_at_position(x: int, y: int, vertices: list[Schelling_Node]) -> Schelling_Node | None:
    for vertex in vertices:
        if vertex.x == x and vertex.y == y:
            return vertex
    return None


def create_vertex_matrix(vertices: list[Schelling_Node]) -> np.ndarray[Schelling_Node]:
    dim = 4
    # Create a matrix to hold the vertices based on their (x, y) positions
    m = np.zeros((dim, dim), dtype=Schelling_Node)
    for vertex in vertices:
        # Ensure no two vertices occupy the same position
        assert not m[vertex.x,
                     vertex.y], f"Two vertices cannot occupy the same position {(vertex.x, vertex.y)}."
        m[vertex.x, vertex.y] = vertex
    return m  # type: ignore
