from qpyc.Device import Component

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import datetime
from qpyc.Mesh import ClementsMesh

# calibration data structure
cdt = np.dtype([
    ('pins', np.uint8),
    ('addrs', np.uint8, 2), # meta
    ('func_paras', np.float32,), # parameters of electrical power vs. optical phase fitting function
    ('time', np.datetime64) # calibration operated time
])


# CaliData = {}
# CaliData['rising_time'] = 0.1 
# CaliData['width'] = 6
# CaliData['depth'] = 6
# CaliData['rising_time'] = 0.1 
# CaliData['phase_func']=np.array([],dtype=(100,cdt))

calidata = np.zeros(30, dtype=cdt)
calidata['addrs'] = ClementsMesh(6).addrs*2
calidata['pins'] = np.arange(30)

def fit_func(x, a, b, c, d):
    return a*np.sin(x*b+c)+d

class RealPhaseShifter(Component):
    """
    Phase shifter
    """
    def __init__(self, addr, pin, rising_time=0.01, cal_data=None):
        super().__init__(addr)
        # self.angle = angle
        self.addr = addr
        self.pin = pin
        # self.res = None
        # self.offset = None
        if cal_data is None:
            self.paras = None
        else:
            self.paras = cal_data[np.where(cal_data['pin']==pin)]

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
        return volts, op
    
    def SweepCurrPhase(self, ps, opm, i_max=10, i_min=0, num=30):
        currs = np.sqrt(np.linspace(i_min**2, i_max**2, num))
        op = np.zeros_like(currs)
        for i, c in enumerate(currs):
            ps.i[self.pin] = c
            op[i] = opm.read()
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
            op[i] = opm.read()
        pp = currs*volts
        popt, pcov = curve_fit(fit_func, pp, op)
        self.paras = popt
        return popt
    
    def SaveCali(self):
        pass
    
if __name__ == '__main__':
    ps1 = RealPhaseShifter(pin=1, addr=(0,0))
    print(ps1.SweepFitPhaseDummy(plot=True))
    ps2 = RealPhaseShifter(pin=2)
    # ps1.SweepCurrPhase
    