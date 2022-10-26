# from pickletools import read_uint1
import imp
from msilib.schema import Component
import numpy as np
import matplotlib.pyplot as plt

# from discopy.quantum.optics import BBS
import time

from zmq import device
# import pytest
# calibration data struture

cdt = np.dtype([
    ('index', np.uint8),
    ('meta_addr', np.uint8, 2),
    ('clemens_addr', np.uint, 2),
    ('func_para', np.float32),
    ('time', np.datetime64)
])


def fit_func(a,b,c,d):
    return lambda x: a*np.sin(x*b+c)+d

class Circuit:
    """
    Circuit class
    """
    def __init__(self) -> None:
        self.dim = 2
        self._devices = []

    def __repr__(self) -> str:
        return [d.__repr__() for d in self._devices]

    @property
    def width(self):
        """
        Circuit width, maximal y coordinate + 2
        """
        return max([ d.y for d in self._devices ]) + 2
    
    @property
    def depth(self):
        """
        Circuit depth, maximal x coordinate + 1
        """
        return max([ d.x for d in self._devices ]) + 1
        
    @property
    def devices(self):
        self._devices.sort(key = lambda d: d.x)
        return self._devices

    @property
    def dev_addr(self):
        return [d.meta_addr for d in self._devices]

    @devices.setter
    def devices(self, devices):
        self._devices = devices
        
    def add(self, device):
        """
        Add devices into the circiut.
        """
        if isinstance(device , Component):
            assert device not in self._devices
        elif isinstance(device, list):
            assert all(isinstance(d , Component) and (d not in self._devices) for d in device) 
        else:
            raise TypeError
        self._devices.append(device)

    def remove(self, device):
        """
        Remove single device by device obejct.
        To do: by coordinate
        """
        assert device in self._devices
        self._devices.remove(device)

    @property
    def matrix(self):
        """
        Calculate the circuit matrix.
        To do: split the devices by columns
        """
        mat = np.eye(self.width)
        for d in self.devices:
            assert isinstance(d, Component)
            submat = np.eye(self.width)
            submat[d.y:d.y+2,d.y:d.y+2] = d.matrix
            mat = mat@submat
        return mat
    
    def __matmul__(self, other):
        assert isinstance(other, Circuit)
        for d in other.devices:
            d.y += self.depth
        self.devices += other.devices

    def __lshift__(self, circ):
        pass

class Component:
    """
    Parent class of basic components in a mesh.
    """

    def __init__(self, meta_addr) -> None:
        """
        Parameters:
        In
        """
        # assert sum(meta_addr) % 2 == 0
        self.meta_addr = meta_addr
        self.x = self.meta_addr[0]
        self.y = self.meta_addr[1]
        self._matrix = np.eye(2, dtype=np.complex_)
    
    def __repr__(self) -> str:
        return f'Component ({self.meta_addr})'


    def __matmul__(self, other):
        if not isinstance(other, Component):
            raise TypeError
        C = Circuit()
        C.devices = [self, other]
        return C
    
    @property
    def clements_addr(self):
        """
        Neboughoring waveguide numbers used in Clements coding to decompese the SU(N) into the sub SU(2) matrix.
        """
        return (self.y, self.y + 1)

    @property
    def clements_index(self):
        """
        Index using the clements coding, in the diagonal order.
        """
        return int( sum(self.meta_addr)**2*.25 - self.meta_addr[1] )
        
    @property
    def matrix(self):
        return self._matrix
    
    @matrix.setter
    def matrix(self, mat):
        self._matrix = mat

class PhaseShifter(Component):
    """
    Phase shifter
    """
    def __init__(self, meta_addr, angle=0) -> None:
        super().__init__(meta_addr)
        self.angle = angle

        self.pin = None
        self.res = None
        self.offset = None

        self.volts = np.linspace(0,10,100)
        self.intensity = None
        
        self.func = None
        
    @property
    def matrix(self):
        return np.array([
            [np.exp(1j*self.angle), 0],
            [0,1+0j]
        ], dtype=np.complex_)

    # @staticmethod
    def DummyCali(self):
        f = fit_func(1,1,0,0)
        self.intensity = f(self.volts) + np.random.random(100)*.1
        
class BeamSpiliter:
    def __init__(self, bias = 0) -> None:
        self.bias = bias

    @property
    def matrix(self):
        # return np.array()
        pass

class MZI:
    """
    Mach-Zehnder interferometor consisting of 2 biased beam spilitters and 2 phase shifters.
    """
    def __init__(self) -> None:
        self.BSIn = BeamSpiliter(0)
        self.BSOut = BeamSpiliter(0)
        self.ExtPS = PhaseShifter(0)
        self.IntPS = PhaseShifter(0)

    # @property
    # def matrix(self):
        # return np.matmul(self.BSIn.matrix, self.)

class ClementsMesh:

    def __init__(self, N) -> None:
        self.N = N
        # self.metas 

    @property
    def matrix(self):
        pass

    def Route(self, PS):
        """
        Route the output port for a given phaseshifter
        """
        xx = range(PS.x+1, self.N+1) # x coordinate
        # y coordinate going down until edge
        y1 = [ PS.y-i-1 if PS.y-i > 1 else 1 for i in range(0, self.N - PS.x) ] 
        # y coordinate going up until edge
        y2 = [ PS.y+i+1 if PS.y+i < self.N-1 else self.N-1 for i in range(0, self.N - PS.x) ]
        route1, route2 = zip(xx, y1), zip(xx,y2)
        # exclude null phase shifters
        route1 = [ d for d in route1 if sum(d) % 2 == 0 ]
        route2 = [ d for d in route2 if sum(d) % 2 == 0 ]
        return route1, route2

    # def Port(self, )

    # def _load(self, )
    # def
    #  
# class BS
# def CreateDummy():


# if __name__ == "__main__":
#     # print(ps.clements_addr)
#     # print(ps.clements_index)
#     # ps.DummyCali()
#     # print(ps.intensity)

#     ps = PhaseShifter((4,4))
#     Mesh = ClementsMesh(6)
#     print(list(Mesh.Route(ps)[0]))
#     print(list(Mesh.Route(ps)[1]))
    