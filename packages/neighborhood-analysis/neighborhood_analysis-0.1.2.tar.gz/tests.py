import numpy as np
import neighborhood_analysis as na
from neighborhood_analysis import CellCombs, get_neighbors, comb_bootstrap

from time import time

types = ['a', 'b', 'c', 'd', 'e']
points = np.random.randint(0, 1000, (10000, 2))
corr_types = np.random.choice(types, 10000)
points = [(x, y) for (x, y) in points]
neighbors = get_neighbors(points, 10.0)

start = time()
cc = CellCombs(types)
cc.bootstrap(corr_types, neighbors, ignore_self=True)
print("order=False:", cc.cell_combs)

cc = CellCombs(types, True)
cc.bootstrap(corr_types, neighbors, ignore_self=True)
print("order=True:", cc.cell_combs)

end = time()
print(f"used {(end-start):.2f}s")

s1 = time()
X = [bool(i) for i in np.random.choice([True, False], 10000)]
Y = [bool(i) for i in np.random.choice([True, False], 10000)]
v = comb_bootstrap(X, Y, neighbors, ignore_self=True)
s2 = time()
print(f"used {(s2-s1):.2f}s")
