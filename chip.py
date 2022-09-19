# from pickletools import read_uint1
import numpy as np
import matplotlib.pyplot as plt
import time
import pytest
# calibration data struture

cdt = np.dtype([
    ('index', np.uint8),
    ('meta_addr', np.uint8, 2),
    ('clemens_addr', np.uint, 2),
    ('func_para', np.float32, sweep_volts),
    ('time', np.datetime64)
])


def fit_func(a,b,c,d):
    return lambda x: a*np.sin(x*b+c)+d

class PhaseShifter:

    def __init__(self, meta_addr) -> None:
        assert sum(meta_addr) % 2 == 0

        self.meta_addr = meta_addr

        self.pin = None
        self.res = None
        self.offset = None
        self.volts = np.linspace(0,10,100)
        self.intensity = None
    
    @property
    def clements_addr(self):
        """
        Neboughoring waveguide numbers used in Clements coding to decompese the SU(N) into the sub SU(2) matrix.
        """
        return (self.meta_addr[1], self.meta_addr[1] + 1)

    @property
    def clements_index(self):
        """
        Index using the clements coding, in the diagonal order.
        """
        return int( sum(self.meta_addr)**2*.25 - self.meta_addr[1] )
        
    # @staticmethod
    def DummyCali(self):
        f = fit_func(1,1,0,0)
        self.intensity = f(self.volts) + np.random.random(100)*.1
    
    def 

    # def _load(self, )
    # def
    #  
# class BS
# def CreateDummy():


if __name__ == "__main__":
    ps = PhaseShifter((1,3))
    print(ps.clements_addr)
    print(ps.clements_index)
    ps.DummyCali()
    print(ps.intensity)
    