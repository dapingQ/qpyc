import numpy as np
from qpyc.Cali import ClementsCali, PinPhaseShifter, new_calidata

# from pycomo.Cali import sixmode_internal_pins, sixmode_external_pins

def test_calidata():
    # Start a Calibration
    # create a empty calibration data structure
    calidata_int = new_calidata(6)
    # this is 2-D structured np array
    print(calidata_int.shape)
    # the datatype is cdt in Cali
    print(calidata_int.dtype)
    # check one addr
    calidata_int[0,1]['pin']

    # define pinout of the chip, in a two dimensional way, -1 here is nc 
    pins = [[-1, 15, -1, 14, -1, 26], 
            [-1, 13, 12, 25, 24, -1],
            [10, 9, 11, 8, 23, 22],
            [-1, 7, 6, 21, 20, -1],
            [4, 3, 5, 2, 19, 18],
            [-1, 1, 0, 17, 16, -1]]
    pin_ma = np.ma.masked_not_equal(pins, -1).mask
    calidata_int['pin'] = pins

if __name__ == "__main__":
    test_calidata()