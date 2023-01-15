import numpy as np

from qpic.Mesh import ClementsMesh
from qpic.Device import xy2i, xy2idx

Mesh = ClementsMesh(6)
# print(Mesh.devices)

def test_idx():
    for a in  Mesh.dev_addr:
        print(a, xy2i(a, 6))

def test_plot():
    Mesh.remove(Mesh.devices[(1,1)])
    Mesh.plot()

if __name__ == "__main__":
    # test_idx()
    test_plot()
    # pass