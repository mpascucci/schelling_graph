# Schelling Graph
Simulation and visualization for a [Schelling's segregation model](https://en.wikipedia.org/wiki/Schelling%27s_model_of_segregation)

## Installation
```bash
pip install -i https://test.pypi.org/simple/ schelling-graph
```

## Usage
The file `graph_definition.py` contains the definition of the graph `g` used in the examples below.


```python
from graph_definition import g

print(g)
```

    Schelling_Graph with 10 nodes.
    


```python
g.plot(); # show the graph structure
```


    
![png](docs/images/README_2_0.png)
    



```python
# assign chips
n = len(g.nodes)

g.init_chips_uniform(min=0, max=10)
# or equivalently:
# from random import randint
# chips = [randint(0, 10) for _ in range(n)]
# g.set_chips(chips, randomize=True)


g_pre = g.copy() # save pre-move state

g.plot_chips();
```


    
![png](docs/images/README_3_0.png)
    



```python
# Run simulation
logs = g.run_rounds(stop_when=g.is_segregated, max_rounds=5000)
fig, ax = g.plot_chips()
```


    
![png](docs/images/README_4_0.png)
    



```python

```
