import numpy as np
from qpic.Device import Component, Waveguide, PhaseShifter, BeamSpiliter, MZI


def test_comp():
    W1 = Waveguide(dom=1)
    W2 = Waveguide(dom=2)
    P1 = PhaseShifter(phase=.25)
    TBS = BeamSpiliter(.01)
    BS = BeamSpiliter()
    # MZI = P1 @ W1 >> BS
    MZI1 = MZI(0,0)
    print(MZI1.matrix)


def test_circuit():
    A = Component([0,0])
    B = Component([0,2])
    A.matrix =  np.array([
        [1,2],
        [3,4]
    ])
    B.matrix =  np.array([
        [1,2],
        [3,4]
    ])
    C = Circuit()
    C.add(A)
    C.add(B)
    
    print(C.matrix)

# C = Circuit()
# C.devices = [Component((4,0)), Component((0,2)), Component((1,1))]
# print(C.devices)

if __name__ == "__main__":
    # test_circuit()
    test_comp()