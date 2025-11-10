# Schelling Graph
Simulation and visualization for a [Schelling's segregation model](https://en.wikipedia.org/wiki/Schelling%27s_model_of_segregation)

## Installation
```bash
pip install schelling-graph
```

## Usage
The file `graph_definition.py` contains the definition of the graph `g` used in the examples below.


```python
from graph_definition import g
from schelling_graph.visualization import draw_matrix_3D
import numpy as np

print(g)
```

    Schelling_Graph with 10 nodes.
    


```python
g.plot(); # show the graph structure
```


    
![png](README_files/README_2_0.png)
    



```python
# assign chips
n = len(g.nodes)
chips = np.random.randint(0, 60, size=n)
g.set_chips(chips)
g_pre = g.copy() # save pre-move state

g.plot_chips();
```


    
![png](README_files/README_3_0.png)
    



```python
# Run simulation
logs = g.run_rounds(stop_when=g.is_segregated, max_rounds=5000)
fig, ax = g.plot_chips()
```
    
![png](README_files/README_4_0.png)
    

