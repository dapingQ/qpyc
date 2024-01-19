#%%
import numpy as np
import doctest
from qpyc.Mesh import ClementsMesh

# create a 6x6 Clements 
mesh = ClementsMesh(dimension=6) 
mesh.plot()

# pick a MZI and route it
# Route returns 1. a nested tuple, represent the device address of four ports; 2. the port to connect
# the coordinates not included is the edgem, eg. (1,5) 
mzi = mesh.devices[(2,4)]
print('MZI address is ', mzi.addr)
route_path_left_upper, route_path_left_lower, route_path_right_lower, route_path_right_upper,  ports_in, ports_out = mesh.Route(mzi.addr)

print('Route to enter from left upper', route_path_left_upper)
print('Route to enter from _left_lower', route_path_left_lower) 
print('Route to enter from _right_lower', route_path_right_lower)
print('Route to enter from _right_upper', route_path_right_upper)
print(ports_in, ports_out)

#%%

from dev import pm, pin_i, pin_v, switch, q

switch(0)
print(pm())
#%%

# Start a Calibration
from qpyc.Cali import ClementsCali, cdt, RealPhaseShifter, new_calidata
from pycomo.Cali import sixmode_internal_pins, sixmode_external_pins

# create a empty calibration data structure
calidata_int = new_calidata(6)

calidata_int['pin'] = [[-1, 15, -1, 14, -1, 26], 
                       [-1, 13, 12, 25, 24, -1],
                       [10, 9, 11, 8, 23, 22],
                       [-1, 7, 6, 21, 20, -1],
                       [4, 3, 5, 2, 19, 18],
                       [-1, 1, 0, 17, 16, -1]]

mesh = ClementsCali(6, calidata_int)

# hardware loading
# osw.read_power = None

for a in mesh.addrs[0:2]:
    print(f'calibrating {a}')
    ps = RealPhaseShifter(addr=a, calidata=calidata_int)
    # print(calidata_int[])
    # print(ps.SweepFitPhaseDummy(plot=True))
    # ps.SweepIV(ps=q)
    # popt = ps.SweepFitPhase(ps=q, osw.read_power)
    # print(popt)    
#%%

ps1 = RealPhaseShifter(pin=1, addr=(0,0), cal_data=calidata)
print(ps1.SweepFitPhaseDummy(plot=True))
    

mesh = CKe


#%%
N = 6
aa = (3,3)

xx = range(N)
# flip = lambda x: 2*N-abs(x) if abs(x) > N

y1 = [ abs(x - aa[0] + aa[1] + 1) - 1 for x in range(N) ]
y2 = [ - abs(x - aa[0] - aa[1] + N - 1) + N - 1 for x in range(N) ]
print(list(zip(xx, y1)))
print(list(zip(xx, y2)))

# %%
