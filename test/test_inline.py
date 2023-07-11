#%%
import numpy as np
import doctest
from qpyc.Mesh import ClementsMesh

mesh = ClementsMesh(dimension=5) 

# def test_mesh():
#     mesh.plot()

# def test_route():
#     bs = mesh.devices[(2,2)]
#     print(bs.addr)
#     print(mesh.Route(bs))

#%%
N = 6
aa = (3,3)

xx = range(N)
# flip = lambda x: 2*N-abs(x) if abs(x) > N

y1 = [ abs(x - aa[0] + aa[1] + 1) - 1 for x in range(N) ]
y2 = [ - abs(x - aa[0] - aa[1] + N - 1) + N - 1 for x in range(N) ]
print(list(zip(xx, y1)))
print(list(zip(xx, y2)))

# %%
