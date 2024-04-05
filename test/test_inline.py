#%%
import numpy as np
from qpyc.Mesh import ClementsMesh
#%%
from dev import pm, pin_i, pin_v, switch, q

switch(0)
print(pm())
#%%


#%%
# creata a calibration mesh, equipped with a calibration data object
mesh = ClementsCali(6, calidata_int)

# hardware loading
# osw.read_power = None

for a in mesh.addrs[0:2]:
    print(f'calibrating {a}')
    ps = PinPhaseShifter(addr=a, calidata=calidata_int)

    # print(calidata_int[])
    # print(ps.SweepFitPhaseDummy(plot=True))
    # ps.SweepIV(ps=q)
    # popt = ps.SweepFitPhase(ps=q, osw.read_power)
    # print(popt)    
#%%

ps1 = PinPhaseShifter(pin=1, addr=(0,0), cal_data=calidata)
print(ps1.SweepFitPhaseDummy(plot=True))
    
