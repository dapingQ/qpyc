'''
Controller
2x6, 1550nm, 1m PM fiber with FC/PC connectors
Firmware version: v1.1
'''

import time
import serial
import argparse

class OSW:

    def __init__(self, port = None): # set port number
        self.port = port
        self.serial = serial.Serial(self.port,
            timeout = 1,
            baudrate=9600
            )
        time.sleep(1)

    def set(self, cha, chb):
        assert 1 < cha <= 6
        assert 1 < chb <= 6
    
        self.serial.write(f'<OSW_OUT_{cha:02d}_{chb:02d}>'.encode('ascii'))
        time.sleep(.1)
        return self.serial.readlines()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Channel')
    parser.add_argument('chan', 
        type=int)
    args = parser.parse_args()
    ops = OSW('COM6')
    print( ops.set(args.chan) )
    