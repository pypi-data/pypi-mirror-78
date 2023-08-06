**RLCluster**
=============

This is the repository for the *rlcluster* Python package that implements the Rodriguez-Laio 
clustering method [(*Science*, 2014,  **344**, 1492-1495)](http://science.sciencemag.org/content/344/6191/1492)

-------

## Installation

`pip install rlcluster`

---

## Usage

```python
import rlcluster as rlc
# The only required input is a square-form distance matrix:
result = rlc.cluster(D)
# Useful things are attributes of the result object:
a = result.assignments # point i belongs to cluster a[i]
r = result.rhos # point i has RL local density value r[i]
d = result.deltas # point i has RL delta value d[i]
c = result.centres # The list of points that qualify as cluster centres
cutoff = result.cutoff # The cutoff delta value in the decision graph used to select cluster centres
# If you have matplotlib, you can view the decision graph:
import matplotlib pyplot as plt
rlc.decision_graph(result, plt.axes())
```
By default cluster() uses a cutoff distance for the local density calculation that will put an average of 
2% of all the points into each cluster, but this can be changed:
```python
result = rlc.cluster(D, target_fraction=0.01) # aim for clusters of average size 1% of the total
```
By default the cutoff delta value for identifying cluster centres from the decision graph (rho vs. delta) is set at
5 sigma above the mean, but this can also be changed:
```python
result = rlc.cluster(D, sigma=7.0) 
```
Finally the default method for calculating local densities uses a Gaussian kernel rather than the simple hard distance
cutoff method described in the original paper (though the kernel method is used in parts of it). The orignal approach 
can be enforced:
```python
result = rlc.cluster(D, method='classic')
```
#Example

```python
import numpy as np
import scipy.spatial as ss
import rlcluster as rlc
from matplotlib import pyplot as plt
%matplotlib inline
```

**Let's begin with some data.**


```python
points = []
for i in range(600):
    t = np.pi * 0.25 * np.random.normal()
    r = 1.0 + 0.1 * np.random.normal()
    points.append([r * np.sin(t), r * np.cos(t)])
for i in range(1000):
    t = np.pi * 0.25 * np.random.normal()
    r = 2.0 + 0.1 * np.random.normal()
    points.append([r * np.sin(t), r * np.cos(t)])

for i in range(1000):
    x = 3.0 + 0.2 * np.random.normal()
    y = 2.0 + 0.5 * np.random.normal()
    points.append([x,y])

for i in range(100):
    x = -2 + np.random.random() * 6.0
    y = -2 + np.random.random() * 6.0
    points.append([x,y])

points = np.array(points)
```

**Calculate the distance matrix and then cluster**


```python
D = ss.distance.pdist(points)
result = rlc.cluster(ss.distance.squareform(D))
```

**Plot the original data, the clustering, and the decision graph**


```python
fig, axes = plt.subplots(1,3)
fig.set_size_inches((13,4))
axes[0].set_title('Data')
axes[0].plot(points[:,0], points[:,1], 'o')

axes[1].set_title('Clustering')
for cid in np.unique(result.assignments):
    axes[1].plot(points[result.assignments==cid, 0], 
                 points[result.assignments==cid, 1], '.')
axes[1].plot(points[result.centres, 0], 
             points[result.centres, 1], 'om')

axes[2].set_title('Decision Graph')
axes[2].set_xlabel('rho')
axes[2].set_ylabel('delta')
rlc.decision_graph(result, axes[2])
```


![png](doc/example.png)

------
#Author

Charlie Laughton 2018

#License

BSD (2-clause)


