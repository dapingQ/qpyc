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

# Start a Calibration
from qpyc.Cali import ClementsCali, cdt, RealPhaseShifter
from pycomo.Cali import sixmode_internal_pins, sixmode_external_pins

# create a empty calibration data structure
mesh = ClementsCali(6)
calidata_int = np.zeros(len(mesh.addrs), dtype=cdt)
calidata_int['addrs'] = mesh.addrs
calidata_int['pins'] = sixmode_internal_pins
calidata_int['time'] = np.datetime64('nat')

# hardware loading
q = None
osw.read_power = None

for a in mesh.addrs:
    print(f'calibrating {a}')
    ps = RealPhaseShifter(pin=1, addr=(0,0), cal_data=calidata_int)
    # print(ps.SweepFitPhaseDummy(plot=True))
    ps.SweepIV(ps=q)
    popt = ps.SweepFitPhase(ps=q, osw.read_power)
    print(popt)    
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
