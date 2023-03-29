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
    

if __name__ == "__main__":
    # import doctest
    # test_comp()
    # test_circuit()
    C1 = Circuit()
    C1.add(Waveguide(dom=2))
    C = Circuit()
    C1.stack(C)
    print(C.depth, C.width)
    C.add(W1)
    print(C[(1,1)])
    