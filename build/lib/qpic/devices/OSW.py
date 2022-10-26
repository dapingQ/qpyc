'''
Controller
2x6, 1550nm, 1m PM fiber with FC/PC connectors
Firmware version: v1.1
'''

import time
import serial, re
import argparse

class OSW:

    def __init__(self, port = None): # set port number
        self.port = port
        self.serial = serial.Serial(self.port,
            timeout = 1,
            baudrate=9600
            )
        self.serial.flushInput()
        self.serial.flushOutput()
        time.sleep(1)

    def query(self):
        self.serial.write(f'<OSW_OUT_?>'.encode('ascii'))
        rcv = self.serial.readline().decode('ascii')
        return [ int(i) for i in re.findall('\d{2}', rcv)]

    def set(self, cha, chb):
        assert 0 <= cha <= 6
        assert 0 <= chb <= 6
        self.serial.write(f'<OSW_OUT_{cha:02d}_{chb:02d}>'.encode('ascii'))
        if self.serial.readline() == b'<OSW_OUT_OK>':
            # self.chn = [cha, chb]
            return f'Set to {cha}, {chb}'
        else:
            return 'Error. Please Set Again.'

    # @property
    # def cha(self):
    #     chn = self.query()
    #     self.cha = chn[0]
    
    # @property
    # def chb(self):
    #     chn = self.query()
    #     self.chb = chn[1]

    # @cha.setter
    # def cha(self, ch):
    #     self.set(ch, self.chb)
    
    # @chb.setter
    # def chb(self, ch):
    #     self.set(self.cha, ch)
    

if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Channel')
    # parser.add_argument('cha', 
    #     type=int)
    # parser.add_argument('chb', 
    #     type=int)
    # args = parser.parse_args()
    ops = OSW('COM10')
    print(ops.query())
    ops.set(1,2)
    print(ops.query())
    ops.set(0,0)
    