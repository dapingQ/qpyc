import numpy as np
from qpyc.Device import Component, Waveguide, PhaseShifter, BeamSpiliter, MZI
from qpyc.Device import Circuit
import doctest

W1 = Waveguide(dom=1)
W2 = Waveguide(dom=2)
P1 = PhaseShifter(phase=.25)
TBS = BeamSpiliter(.01)
BS = BeamSpiliter()

def test_add():
    C = Circuit()
    print(C.depth, C.width)
    C.add(P1@W1)
    C.add(BS, TBS)

def test_MZI():
    BS =  BeamSpiliter(0) 
    D = PhaseShifter(1/3) @ Waveguide()
    C = BS >> D >> BS
    print(BS.matrix)
    print(D.matrix)
    
def test_circuit():
    C = Circuit()
    # C.add(BS)
    C.add(BeamSpiliter(addr=(0,0)))
    C.add(BeamSpiliter(addr=(1,1)))
    # C.add(BS)
    # C.add(BS)
    C.plot()

if __name__ == "__main__":
    # test_MZI()
    test_circuit()
