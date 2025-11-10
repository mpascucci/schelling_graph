import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from schelling_graph import Schelling_Node
from schelling_graph.tools import create_vertex_matrix
from mpl_toolkits.mplot3d import Axes3D

def _draw_graph(nodes: list[Schelling_Node], ax):
    for node in nodes:
        ax.scatter(node.x, node.y, s=1000, c=node.color.value)
        ax.scatter(node.x, node.y, s=300, c='white')
        
        count_n = 0
        count_s = 0
        count_e = 0
        count_w = 0

        for i, arrow in enumerate(node.arrows):
            nx = arrow.neighbor.x
            ny = arrow.neighbor.y
            x = node.x
            y = node.y
            
            orientation = (nx - x, ny - y)
            n = orientation[1] > 0
            s = orientation[1] < 0
            e = orientation[0] > 0
            w = orientation[0] < 0

            scale = 0.075

            dx = 0
            dy = 0
            
            if n:
                dx = count_n//2 * scale if count_n%2==0 else -count_n//2 * scale
                y=y+0.3
                ny=ny-0.3
            elif s:
                dx = - (count_s//2 * scale if count_s%2==0 else -count_s//2 * scale)
                y=y-0.3
                ny=ny+0.3
            elif e:
                dy = count_e//2 * scale if count_e%2==0 else -count_e//2 * scale
                x=x+0.3
                nx=nx-0.3
            elif w:
                dy = - (count_w//2 * scale if count_w%2==0 else -count_w//2 * scale)
                x=x-0.3
                nx=nx+0.3


            x += dx
            y += dy
            nx += dx
            ny += dy
            # print(f"Drawing arrow {i} ({arrow.color}) from ({x},{y}) to ({nx},{ny})")
            ax.annotate('',
                        xytext=(x, y),
                        xy=(nx, ny),
                        arrowprops=dict(arrowstyle="->", color=arrow.color.value, lw=2),
                        )
            
            count_n += n
            count_s += s
            count_e += e
            count_w += w


        ax.text(node.x, node.y, str(node.chips), color='black', fontsize=12, ha='center', va='center')

    rows = max(v.x for v in nodes) + 1
    cols = max(v.y for v in nodes) + 1
    ax.set_xticks(np.arange(0, cols , 1))
    ax.set_yticks(np.arange(0, rows, 1))
    ax.set_xlim(-0.5, cols - 0.5)
    ax.set_ylim(-0.5, rows - 0.5)

def draw_graph(vertices: list[Schelling_Node]):
    fig, ax = plt.subplots()
    _draw_graph(vertices, ax=ax)
    plt.show()
    return fig, ax

def _draw_matrix(matrix_or_vertices, ax):
    """Draws the given matrix of Schelling_Vertex objects using matplotlib."""
    if isinstance(matrix_or_vertices, list):
        matrix = create_vertex_matrix(matrix_or_vertices)
    else:
        matrix = matrix_or_vertices

    matrix = np.flip(matrix, axis=1)  # Flip the matrix horizontally for correct display

    max_chips = max(
        node.chips for node in matrix.flatten() if isinstance(node, Schelling_Node))

    rows, cols = matrix.shape
    for i in range(rows):
        for j in range(cols):
            vertex = matrix[i, j]
            if vertex:
                intensity = vertex.chips / max_chips if max_chips > 0 else 0
                facecolor = plt.cm.get_cmap('Greens')(intensity)
                textcolor = 'white' if intensity > 0.5 else 'black'
                ax.add_patch(

                    plt.Rectangle((i, j), 1, 1, # type: ignore
                                  facecolor=facecolor,
                                  edgecolor='white',
                                  linewidth=1))

                ax.text(i + 0.5, j + 0.5, str(vertex.chips), color=textcolor, fontsize=12, ha='center', va='center')
            else:
                ax.add_patch(plt.Rectangle((i, j), 1, 1, color='lightgray', fill=False)) # type: ignore
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_aspect('equal')
    ax.invert_yaxis()

    ax.set_xticks(np.arange(0.5, cols + 0.5, 1))
    ax.set_xticklabels(np.arange(0, cols))
    ax.set_yticks(np.arange(0.5, rows + 0.5, 1))
    ax.set_yticklabels(np.arange(0, rows )[::-1])


def draw_matrix_3D(matrix_or_vertices: list[Schelling_Node] | np.ndarray):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    if isinstance(matrix_or_vertices, list):
        matrix = create_vertex_matrix(matrix_or_vertices)
    else:
        matrix = matrix_or_vertices

    matrix = np.flip(matrix, axis=1)  # Flip the matrix horizontally for correct display

    max_chips = max(
        node.chips for node in matrix.flatten() if isinstance(node, Schelling_Node))
    
    
    rows, cols = matrix.shape

    idxs = np.indices((rows, cols)).reshape(2, -1).T.tolist()
    idxs.sort(key=lambda idx: idx[0]**2 + idx[1]**2)  # Sort by distance from origin

    for i,j in idxs:
        vertex = matrix[i, j]
        if vertex:
            intensity = vertex.chips / max_chips if max_chips > 0 else 0
            facecolor = plt.cm.get_cmap('Greens')(intensity)
            ax.bar3d(i, j, 0, 1, 1, vertex.chips, color=facecolor, edgecolor=None)

    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_zlim(0, max_chips)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Chips')

    ax.set_xticks(np.arange(0.5, cols + 0.5, 1))
    ax.set_xticklabels(np.arange(0, cols))
    ax.set_yticks(np.arange(0.5, rows + 0.5, 1))
    ax.set_yticklabels(np.arange(0, rows )[::-1])
    
    ax.view_init(elev=30, azim=-60) # Changes the elevation and azimuth
    return fig, ax


def draw_matrix(matrix_or_vertices: list[Schelling_Node] | np.ndarray):
    fig, ax = plt.subplots()
    _draw_matrix(matrix_or_vertices, ax=ax)
    plt.show()
    return fig, ax