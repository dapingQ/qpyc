from qpyc.Device import Component

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import datetime, time
from qpyc.Mesh import ClementsMesh

# calibration data structure
cdt = np.dtype([
    ('pin', np.uint8),
    ('func_paras', np.float32,), # parameters of electrical power vs. optical phase fitting function
    ('time', np.datetime64) # calibration operated time
])

def new_calidata(N):
    calidata = np.zeros((N,N), dtype=cdt)
    calidata['pin'] = np.array([np.nan]*N**2).reshape(N,N)
    calidata['time'] = np.datetime64()
    return calidata

def fit_func(x, a, b, c, d):
    return a*np.sin( x*b + c ) + d

class RealPhaseShifter(Component):
    """
    Phase shifter to test in practise
    """
    def __init__(self, addr, rising_time=0.01, calidata=None, pin=None):
        super().__init__(addr)
        self.addr = addr
        self.rising_time = rising_time
        self.pin = pin
        self.paras = None
        if calidata is not None:
            self.paras = calidata[addr]['func_paras']
            self.pin = calidata[addr]['pin']
            if pin is not None:
                print('Overwrite Pin number') 
            
        # self.volts = np.linspace(0,10,100)
        # self.intensity = None        
        # self.func = None
        
    def __repr__(self) -> str:
        return f'Phase Shifter {self.addr} Pin {self.pin}'
    
    def SweepIV(self, ps, v_max=10, v_min=0, num=10):
        vv = np.linspace(v_min, v_max, num)
        ii = np.zeros_like(vv)
        for i, v in enumerate(vv):
            ps.v[self.pin] = v
            ii[i] = ps.i[self.pin] 
        return [vv, ii]
    
    def SweepVoltPhase(self, ps, opm_read, v_max=10, v_min=0, num=30):
        volts = np.sqrt(np.linspace(v_min**2, v_max**2, num))
        op = np.zeros_like(volts)
        for i, v in enumerate(volts):
            ps.v[self.pin] = v
            op[i] = opm_read()
        return volts, op
    
    def SweepCurrPhase(self, ps, opm_read, i_max=10, i_min=0, num=30):
        currs = np.sqrt(np.linspace(i_min**2, i_max**2, num))
        op = np.zeros_like(currs)
        for i, c in enumerate(currs):
            ps.i[self.pin] = c
            op[i] = opm_read()
        return currs, op
    
    def SweepFitPhaseDummy(self, i_max=10, i_min=0, num=30, plot=False):
        currs = np.sqrt(np.linspace(i_min**2, i_max**2, num))
        volts = currs*0.1
        pp = currs*volts

        paras = np.random.normal([1, 1, 0.1, 1], [.1, .1, .01, .1])
        rms = paras[0]*0.01
        op = fit_func(pp, *paras) + np.random.normal(0, rms, size=30)

        popt, pcov = curve_fit(fit_func, pp, op)
        self.paras = popt
        if plot is True:
            plt.plot(pp, op, 'r*')
            plt.plot(pp, fit_func(pp, *popt))
            plt.show()
        return popt
    
    def SweepFitPhase(self, ps, opm, i_max=10, i_min=0, num=30):
        currs = np.sqrt(np.linspace(i_min**2, i_max**2, num))
        volts = np.zeros_like(currs)
        op = np.zeros_like(currs)
        for i, c in enumerate(currs):
            ps.i[self.pin] = c
            volts[i] = ps.v[self.pin]
            time.sleep(self.rising_time)
            op[i] = opm.read()
        pp = currs*volts
        popt, pcov = curve_fit(fit_func, pp, op)
        self.paras = popt
        return popt
    
    def UpdateCali(self, calidata):
        calidata[self.addr]['func_paras'] = self.paras
        calidata[self.addr]['time'] = np.datetime64()

class ClementsCali(ClementsMesh):
    def __init__(self, dimension, calidata) -> None:
        super().__init__(dimension)

        phaseshitfers = []
        for i in range(dimension):
            for j in range(dimension):
                phaseshitfers.append( RealPhaseShifter(addr=(i,j), calidata=calidata) )
                # phaseshitfers.append( (i,j) )
        self.phaseshitfers = phaseshitfers

    def __getitem__(self, addr):
        # return super().__getitem__(item)
        return self.phaseshitfers[addr[0]*self.dimension+addr[1]]

if __name__ == '__main__':
    calidata_int = new_calidata(6)
    calidata_int['pin'] = [[-1, 15, -1, 14, -1, 26], 
                        [-1, 13, 12, 25, 24, -1],
                        [10, 9, 11, 8, 23, 22],
                        [-1, 7, 6, 21, 20, -1],
                        [4, 3, 5, 2, 19, 18],
                        [-1, 1, 0, 17, 16, -1]]

    mesh = ClementsCali(6, calidata_int)

    ps1 = RealPhaseShifter(addr=(0,0), calidata=calidata_int)
    print('a')
    # print(ps1.SweepFitPhaseDummy(plot=True))
    
    