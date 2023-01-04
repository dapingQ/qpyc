import numpy as np
import matplotlib.pyplot as plt

# calibration data structure
cdt = np.dtype([
    ('index', np.uint8),
    ('meta_addr', np.uint8, 2), # meta
    ('clemens_addr', np.uint, 2), 
    ('func_para', np.float32), # parameters of electrical power vs. optical phase fitting function
    ('time', np.datetime64) # calibration operated time
])

def fit_func(a,b,c,d):
    return lambda x: a*np.sin(x*b+c)+d



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
        

    