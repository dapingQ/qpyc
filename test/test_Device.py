import numpy as np
from qpic.Device import Component, Waveguide, PhaseShifter, BeamSpiliter, MZI
from qpic.Device import Circuit


W1 = Waveguide(dom=1)
W2 = Waveguide(dom=2)
P1 = PhaseShifter(phase=.25)
TBS = BeamSpiliter(.01)
BS = BeamSpiliter()


def test_comp():
    MZI = P1 @ W1 >> BS
    # MZI1 = MZI(0,0)
    print(MZI.matrix)


def test_circuit():
    C = Circuit()
    print(C.depth, C.width)
    C.add(P1@W1)
    # print(C.__repr__())
    # C.add(BS)
    D = C.copy()
    print(C.depth, C.width)
    # print(MZI1.matrix)
    print(C.matrix)
    E = D@C
    print(E.devices)

# C = Circuit()
# C.devices = [Component((4,0)), Component((0,2)), Component((1,1))]
# print(C.devices)

if __name__ == "__main__":
    # import doctest
    test_comp()
    test_circuit()
    