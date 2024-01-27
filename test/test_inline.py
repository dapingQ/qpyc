#%%
import numpy as np
from qpyc.Mesh import ClementsMesh
#%%
from dev import pm, pin_i, pin_v, switch, q

switch(0)
print(pm())
#%%

# Start a Calibration

from qpyc.Cali import ClementsCali, PinPhaseShifter, new_calidata
# from pycomo.Cali import sixmode_internal_pins, sixmode_external_pins

# create a empty calibration data structure
calidata_int = new_calidata(6)

# define pinout of the chip, in a two dimensional way, -1 here is nc
calidata_int['pin'] = [[-1, 15, -1, 14, -1, 26], 
                       [-1, 13, 12, 25, 24, -1],
                       [10, 9, 11, 8, 23, 22],
                       [-1, 7, 6, 21, 20, -1],
                       [4, 3, 5, 2, 19, 18],
                       [-1, 1, 0, 17, 16, -1]]
# this is 2-D structured np array
print(calidata_int.shape)
# the datatype is cdt in Cali
print(calidata_int.dtype)
# check one addr
calidata_int[0,1]['pin']

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
    

