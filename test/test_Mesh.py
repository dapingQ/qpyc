import numpy as np
import doctest
from qpyc.Mesh import ClementsMesh

mesh = ClementsMesh(dimension=10) 
d1 = mesh[0,2]

def test_plot_address():
    mesh.plot()

def test_plot_phase():
    mesh.plot(label='phase')

def test_route():
    # create a 6x6 Clements 
    mesh = ClementsMesh(dimension=6) 
    mesh.plot()

    # pick a mzi from the mesh
    mzi = mesh.devices[(2,4)]
    print('MZI address is ', mzi.addr)

    # and find the way to route it
    # Route menthod returns 1. a nested tuple, represent the device address of four ports; 2. the port to connect
    # the coordinates not included is the edgem, eg. (1,5) 
    route_path_left_upper, route_path_left_lower, route_path_right_lower, route_path_right_upper, ports_in, ports_out = mesh.Route(mzi.addr)

    print('Route to enter from left upper', route_path_left_upper)
    print('Route to enter from left lower', route_path_left_lower) 
    print('Route to enter from right lower', route_path_right_lower)
    print('Route to enter from right upper', route_path_right_upper)
    print('Ports to enter from', ports_in)
    print('Ports to eixt from',  ports_out)

if __name__ == '__main__':
    test_plot_phase()