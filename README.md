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

q=0.05
p=0.6
pvals = [1/10]*10
g.init_chips_multinomial(pvals)

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
ani = g.animate(interval=200)
```

<html></html>

see the [animation of the simulation](docs/images/schelling_simulation.html).
