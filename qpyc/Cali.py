from qpyc.Device import Component

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

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


class RealPhaseShifter(Component):
    """
    Phase shifter
    """
    def __init__(self, addr, pin, rising_time=0.01):
        super().__init__(meta_addr)
        # self.angle = angle
        self.addr = addr
        self.pin = pin
        self.res = None
        self.offset = None

        # self.volts = np.linspace(0,10,100)
        # self.intensity = None        
        # self.func = None
        
    def SweepIV(self, ps, v_max=10, v_min=0, num=10):
        vv = np.linspace(v_min, v_max, num)
        ii = np.zeros_like(vv)
        for i, v in enumerate(vv):
            ps.v[self.pin] = v
            ii[i] = ps.i[self.pin] 
        return [vv, ii]
    
    def SweepVoltPhase(self, ps, opm, v_max=10, v_min=0, num=30):
        volts = np.sqrt(np.linspace(v_min**2, v_max**2, num))
        op = np.zeros_like(volts)
        for i, v in enumerate(volts):
            ps.v[self.pin] = v
            op[i] = opm.read()
        return [volts, op]
    
    def SweepCurrPhase(self, ps, opm, i_max=10, i_min=0, num=30):
        currs = np.sqrt(np.linspace(i_min**2, i_max**2, num))
        op = np.zeros_like(currs)
        for i, c in enumerate(currs):
            ps.i[self.pin] = c
            op[i] = opm.read()
        return [currs, op]
        
    def SweepFit(self, ps, opm, i_max=10, i_min=0, num=30):
        currs = np.sqrt(np.linspace(i_min**2, i_max**2, num))
        volts = np.zeros_like(currs)
        op = np.zeros_like(currs)
        for i, c in enumerate(currs):
            ps.i[self.pin] = c
            volts[i] = ps.v[self.pin]
            op[i] = opm.read()
        pp = currs*volts
        popt, pcov = curve_fit(fit_func, pp, op)
        return popt
    

    