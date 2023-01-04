import numpy as np

from qpic.Mesh import ClementsMesh
from qpic.Device import xy2i, xy2idx

Mesh = ClementsMesh(6)
print(Mesh.devices)

Mesh.plot()
#     print(list(Mesh.Route(ps)[0]))
#     print(list(Mesh.Route(ps)[1]))

def test_idx():
    for a in  Mesh.dev_addr:
        print(a, xy2i(a, 6))

if __name__ == "__main__":
    test_idx()