import numpy as np
import doctest
from qpyc.Mesh import ClementsMesh

mesh = ClementsMesh(dimension=10) 

def test_mesh():
    mesh.plot()

def test_route():
    print(mesh.Route([2,4]))

if __name__ == '__main__':
    # test_route()
    test_mesh()