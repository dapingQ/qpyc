from operator import mod
import numpy as np
from pyvisa import ResourceManager

class MultiPowerMeter:
    def __init__(self, port='TCPIP0::10.42.0.107::5000::SOCKET'):
        rm = ResourceManager()
        self.instr = rm.open_resource(port)
        del rm
        self.instr.write_termination = '\r\n'
        self.instr.read_termination = '\r\n' 
    
    def GetIDN(self):
        """
        Description
            Identification Query
        
        Syntax
            *IDN?
        
        Response
            SANTEC,MPM-210H,zzzzzzzz,Ver. x.y
        zzzzzzzz is serial number of main frame, and Ver. x.y is firmware version.
        """
        return self.instr.query('*IDN?')

    def GetError(self):
        """
        Description
            Check Error information.
        
        Syntax
            ERR?
        
        Response
            <value>,<string>
        <value>: Error Code
        <string>: Summary of content for Error
        Please refer to “5.5.5 ERR?”
        
        Example
            ERR?
        
        Response: 0, “No Error”
            """
        return self.instr.query('ERR?')

    def GetModStatus(self):
        """
        Description
            Check recognition of MM (Module) for MPM-210H.
        
        Syntax
            IDIS?
        
        Response
            <value0>, <value1>, <value2>, <value3>, <value4>
        value0: Module0
        value1: Module1
        value2: Module2
        value3: Moduel3
        value4: Module4
        0: Module is not recognized.
        1: Module is recognized.
        
        Example
            IDIS?
        
        Response: 1,1,1,1,1
            """
        return self.instr.query('IDIS?')

    def GetModVer(self, mod):
        """
        Description
            Identification query of a module type
        
        Syntax
            MMVER?<wsp><module>
        
        Parameters
        <module >: 0,1,2,3,4
        
        Response
            <value0>,<value1>,<value2>,<Value3>
        value0: Company (Santec)
        value1: Product code (MPM-211,MPM-212,MPM-
        213,MPM-215)
        value2: Serial number
        value3: Firmware version
        
        Example
            MMVER? 0
        
        Response : Santec,MPM-211,00000000M211,Ver1.11
            """
        self.instr.query(f'MMVER? {mod}')

    def SetGPIBAddr(self, addr=16):
        """
        Description
            Set up GPIB Address
        
        Syntax
            ADDR<wsp><value>
        
        Parameters
        <value>: 1 ~ 31
        
        Default
            16
        
        Example
            ADDR 16
        """
        self.instr.write(f'ADDR {addr}')

    def GetGPIBAddr(self):
        """
        Description
            Check GPIB Address.
        
        Syntax
            ADDR?
        
        Response
            <value>
        
        Example
            ADDR?
        
        Response: 16
            """
        return self.instr.query('ADDR?')

    def SetGateway(self, gateway):
        """
        Description
            Set up Gate way Address.
        
        Syntax
            GW<wsp><www.xxx,yyy,zzz>
        
        Parameters
        <www.xxx,yyy,zzz>: 0 ~ 255
        
        Default
            192.168.1.254
        
        Example
            GW 192.168.1.254
        """
        self.instr.write(f'GR {gateway}')

    def GetGateway(self):
        """
        Description
            Check Gate way Address.
        
        Syntax
            GW?
        
        Response
            <www.xxx,yyy,zzz>
        
        Example
            GW?
        
        Response: 192.168.1.254
            """
        return self.instr.query('GR?')

    def SetSubnetMask(self, subnet):
        """
        Description
            Set up Subnet Mask.
        
        Syntax
            SUBNET<wsp><www.xxx,yyy,zzz>
        
        Parameters
        <www.xxx,yyy,zzz>: 0 ~ 255
        
        Default
            255. 255. 255.0
        
        Example
            SUBNET 255. 255. 255.0
        """
        self.instr.write(f'GR {subnet}')

    def GetSubnetMask(self):
        """
        Description
            Check Subnet Mask
        
        Syntax
            SUBNET?
        
        Response
            <www.xxx,yyy,zzz>
        
        Example
            SUBNET?
        
        Response: 255. 255. 255.0
            """
        return self.instr.query('SUBNET?')

    def SetIP(self, ip):
        """
        Description
            Set up IP Address.
        
        Syntax
            IP<wsp><www.xxx,yyy,zzz>
        
        Parameters
        <www.xxx,yyy,zzz>: 0 ~ 255
        
        Default
            192.168.1.161
        
        Example
            IP 192.168.1.161
        """
        self.instr.write(f'IP {ip}')

    def GetIP(self):
        """
        Description
            Check IP Address.
        
        Syntax
            IP?
        
        Response
            <www.xxx,yyy,zzz>
        
        Example
            IP?
        
        Response: 192.168.1.161
            """
        return self.instr.query('IP?')

    def SetTrigger(self, trig=1):
        """
        Description
            If measuring mode is 'CONSTx', it checks for measuring
        trigger.
        
        Syntax
            TRIG<wsp><value>
        
        Parameters
        <value>
        0 : Internal trigger
        1 : External trigger
        If it is internal trigger, it generates trigger every 10ms.
        
        Default
            1
        
        Example
            TRIG 1
        """
        assert trig in [0,1]
        self.instr.write(f'TRIG {trig}')

    def GetTrigger(self):
        """
        Description
            If measuring mode is 'CONSTx', it checks for measuring trigger.
        
        Syntax
            TRIG?
        
        Response
            <value>
        0 : Internal trigger
        1 : External trigger
        
        Example
            TRIG? 1
        
        Response: 1
            """
        return self.instr.query('TRIG?')
        
    def SetMeasureMode(self, mode):
        """
        
        Description
            Set measurement mode.
        The MPM-215 supports only “CONST2” and “SWEEP2”.
        
        Syntax
            WMOD<wsp><value>
        
        Parameters
        <value>
        “CONST1” => Constant Wavelength, No Auto Gain, SME
        mode
        “SWEEP1” => Sweep Wavelength, No Auto Gain, SME
        mode
        “CONST2” => Constant Wavelength, Auto Gain, SME
        mode
        “SWEEP2” => Sweep Wavelength, Auto Gain, SME mode
        “FREERUN” => Constant Wavelength, No Auto Gain, First
        Hardware Trigger Start (CEM mode)
        Refer to the 5.6.1 WMOD.
        
        Default
            CONST1
        
        Example
            WMOD CONST1
        """
        assert mode in [
            'CONST1',
            'CONST2',
            'SWEEP1',
            'SWEEP2',
            'FREERUN'
            ]
        self.instr.write(f'VMOD {mode}')
    
    def GetMeasureMode(self):
        """
        Description
            Check measurement mode.
        The MPM-215 supports only “CONST2” and “SWEEP2”.
        
        Syntax
            WMOD?
        
        Response
            “CONST1” => Constant Wavelength, No Auto Gain, SME
        mode
        “SWEEP1” => Sweep Wavelength, No Auto Gain, SME
        mode
        “CONST2” => Constant Wavelength, Auto Gain, SME
        mode
        “SWEEP2” => Sweep Wavelength, Auto Gain, SME mode
        “FREERUN” => Constant Wavelength, No Auto Gain, First
        Hardware Trigger Start (CEM mode)
        Refer to the 5.6.1 WMOD.
        
        Example
            WMOD?
        
        Response: CONST1
            """

        return self.instr.query('WMOD?')

    def SetWavelength(self, wavelength):
        """
        Description
            Set up for using wavelength of Constant wavelength
        Measurement Mode (CONST1, CONST2, READ).
        
        Syntax
            WAV<wsp><value>
        
        Parameters
        <value>
        1250.000 ~ 1630.000 Real number
        Unit: nm
        
        Default
            1550
        
        Example
            WAV 1550
        """
        self.instr.write(f'WAV {wavelength:4.3f}')

    def GetWavelength(self):
        """
        Description
            Check
        using
        wavelength
        of
        Constant
        wavelength
        Measurement Mode (CONST1, CONST2, READ).
        
        Syntax
            WAV?
        
        Response
            <value>
        1250.000 ~ 1630.000 Real number
        Unit: nm
        
        Example
            WAV?
        
        Response: 1550
            """
        return self.instr.query('WAV?')

    def SetChannelWavelength(self, module, channel, wavelength):
        """
        Description
            Set up for using wavelength of Constant wavelength
        Measurement Mode (CONST1, CONST2, READ) for each
        channel.
        
        Syntax
            DWAV<wsp><value1>,<value2>,<value3>
        
        Parameters
        <value1>: Module 0, 1, 2, 3, 4, 5
        When setting the <value 1> to 5, all channels and
        module is set to the same wavelength.
        <value2>: Channel 1, 2, 3, 4
        <value3>: 1250.000 ~ 1630.000 Real number
        Unit: nm
        
        Default
            1550
        
        Example
            DWAV 0,1,1550
        """
        assert module in range(6)
        assert channel in range(1,5)
        self.instr.write(f'DWAV {module},{channel},{wavelength:4.3f}')

    def GetChannelWavelength(self, module, channel):
        """
        Description
            Check using wavelength of Constant wavelength
        Measurement Mode (CONST1, CONST2, READ) for each
        channel.
        
        Syntax
            DWAV? <wsp><value1>,<value2>
        
        Parameters
        <value1>: Module 0,1, 2, 3, 4
        <value2>: Channel 1, 2, 3, 4
        
        Response
            <value>
        1250.000 ~ 1630.000 Real number
        Unit: nm
        
        Example
            DWAV? 0,1
        
        Response: 1550
            """

        assert module in range(6)
        assert channel in range(1,5)
        return self.instr.write(f'DWAV? {module},{channel}')

    def SetSweep(self, start=1520, stop=1570, step=0.05):
        """
        Description
            Set up for using wavelength of Sweep Wavelength
        Measurement Mode (SWEEP1, SWEEP2).
        The data points is calculated from the condition that is set
        by the “WSET” command and it is possible to check the
        data points by the “LOGN?” command. Please refer to
        “5.6.3. Measurement data point setting (LOGN)”.
        
        Syntax
            WSET<wsp><value1>,<value2>,<value3>
        
        Parameters
        <value1>: Start wavelength : 1250 ~ 1630
        <value2>: Stop wavelength : 1250 ~ 1630
        <value3>: Step wavelength : 0.001 ~ 10
        Unit: nm
        Note) Stop wavelength = Start wavelength + step
        wavelength
        
        Default
            value1: 1250, value2: 1630, value3: 0.005
        
        Example
            WSET 1520,1570,0.05
        """
        assert 1250 < start < stop < 1630
        assert 1e-3 < step < 1e1
        self.instr.write(f'WSET {start:4.0f},{stop:4.0f},{step:>.3f}')
        
    def GetSweep(self):
        """
        Description
            Check
        using
        wavelength
        of
        Sweep
        Wavelength
        Measurement Mode (SWEEP1, SWEEP2).
        
        Syntax
            WSET?
        
        Response
            <value1>,<value2>,<value3>
        <value1>: Start wavelength : 1250 ~ 1630
        <value2>: Stop wavelength : 1250 ~ 1630
        <value3>: Step wavelength : 0.001 ~ 10
        Unit: nm
        
        Example
            WSET?
        
        Response: 1520,1570,0.05
            """
        return self.instr.query('WSET?')
    
    def SetSpeed(self, speed):
        """
        Description
            Set up Wavelength Sweep Speed (Sweep Wavelength
        Measurement Mode (SWEEP1, SWEEP2)). The averaging
        time is automatically set by the measurement speed and
        measurement step of WSET.
        
        Syntax
            SPE<wsp><value>
        
        Parameters
        <value>: Sweep speed : 0.001 ~ 200
        Unit: nm/sec
        
        Default
            value: 1
        
        Example
            SPE 1
        """
        assert 1e-3 < speed < 200
        self.instr.write(f'SPE {speed}')

    def GetSpeed(self):
        """
        Description
            Check Wavelength Sweep Speed (Sweep Wavelength
        Measurement Mode (SWEEP1, SWEEP2)).
        
        Syntax
            SPE?
        
        Response
            <value>
        Sweep speed : 0.001 ~ 200
        Unit: nm/sec
        
        Example
            SPE?
        
        Response: 1
            """
        return self.instr.query('SPE?')

    def SetLevel(self, level):
        """
        Description
            Set up TIA Gain for CONST1, SWEEP1, FREERUN, AUTO1
        measuring mode.
        Refer to the 5.5.7 for the relation between the gain setting
        and the input power.
        This command is not available for the MPM-215.
        
        Syntax
            LEV<wsp><value>
        
        Parameters
        <value>: 1, 2, 3, 4, 5
        In case of the MPM-213 (current meter), the available
        range is 1 to 4.
        
        Default
            value: 5
        
        Example
            LEV 5
        """
        assert level in range(1,6)
        self.instr.write(f'LEV {level}')

    def GetLevel(self):
        """
        Description
            Check TIA Gain of CONST1, SWEEP1, FREERUN, AUTO1
        measuring mode.
        Refer to the 5.5.7 for the relation between the gain setting
        and the input power.
        This command is not available for the MPM-215.
        
        Syntax
            LEV?
        
        Response
            <value>
        value: 1, 2, 3, 4, 5
        
        Example
            LEV?
        
        Response: 5
            """
        return self.instr.query('LEV?')

    def SetChannelLevel(self, module, channel, level):
        """
        Description
            Set up TIA Gain for CONST1, SWEEP1, FREERUN, AUTO1

        measuring mode for each channel.
        Refer to the 5.5.7 for the relation between the gain setting
        and the input power.
        This command is not available for the MPM-215.
        
        Syntax
            DLEV<wsp><value1>,<value2>,<value3>
        
        Parameters
        <value1>: Module 0, 1, 2, 3, 4, 5
        When setting the <value 1> to 5, all channels and
        module is set to the same wavelength.
        <value2>: Channel 1, 2, 3, 4
        <value3>: Gain 1, 2, 3, 4, 5
        In case of the MPM-213 (current meter), the available
        range is 1 to 4.
        
        Default
            value3: 5
        
        Example
            DLEV 0,1,5
        """
        assert module in range(6)
        assert channel in range(1,5)
        assert level in range(1,6)
        self.instr.write(f'DLEV {module},{channel},{level}')

    def GetChannelLevel(self, module, channel):
        """
        Check TIA Gain of CONST1, SWEEP1, FREERUN, AUTO1
        measuring mode for each channel.
        Refer to the 5.5.7 for the relation between the gain setting
        and the input power.
        When using the “READ?” command, the manual mode
        (AUTO1) of the range mode is only available.
        This command is not available for the MPM-215.
        
        Syntax
            DLEV? <wsp><value1>,<value2>
        
        Parameters
        <value1>: Module 0, 1, 2, 3, 4
        <value2>: Channel 1, 2, 3, 4
        
        Response
            <value>
        value: 1, 2, 3, 4, 5
        
        Example
            DLEV? 0,1
        
        Response: 5
            """
        assert module in range(6)
        assert channel in range(1,5)
        self.instr.write(f'DLEV? {module},{channel}')
    
    def SetAverage(self, avg_time=5):
        """
        Description
            Set up Average Time.
        
        Syntax
            AVG<wsp><value>
        
        Parameters
        <value>: 0.01 ~ 10000.00

        Unit: ms
        Resolution: 0.01(10us)
        
        Default
            value: 5
        
        Example
            AVG 5
        """
        assert 1e-2 < avg_time < 1e4
        self.instr.write(f'AVG {avg_time}')

    def GetAverage(self):
        """
        
        Description
            Check Average time.
        
        Syntax
            AVG?
        
        Response
            <value>
        value: 0.01 ~ 10000.00
        Unit: ms
        resolution: 0.01(10us)
        
        Example
            AVG?
        
        Response: 5
            """
        return self.instr.query('AVG?')

    def SetUnit(self, unit):
        """
        Description
            Set measuring unit of optical power or electrical current.
        
        Syntax
            UNIT<wsp><value>
        
        Parameters
        <value>
        0 - dBm, dBmA
        1 - mW, mA
        
        Default
            value: 0
        
        Example
            UNIT 0
        """
        self.instr.write(f'UNIT {unit}')

    def GetUnit(self):
        """
        Description
            Check measuring unit of optical power or electrical current.
        
        Syntax
            UNIT?
        
        Response
            <value>
        0 - dBm, dBmA
        1 - mW,mA
        
        Example
            UNIT?
        
        Response: 0
            """
        unit_list = ['dBm, dBmA', 'mW,mA']
        return unit_list[int(self.instr.query('UNIT?'))]

    def SetAutoRange(self, auto=True):
        """
        Description
            Set the power range (Auto or Manual).
        It is available for the “READ?” command.
        
        Syntax
            AUTO<wsp><value>
        
        Parameters
        <value>
        0 - Manual range
        1 - Auto range
        
        Default
            value: 1
        
        Example
            AUTO 1
        """
        self.instr.write(f'AUTO {auto:d}')

    def GetAutoRange(self):
        """
        
        Description
            Check the power range (Auto or Manual).
        It is available for the “READ?” command.
        
        Syntax
            AUTO?
        
        Response
            0 - Manual range
        1 - Auto range

        
        Example
            AUTO?
        
        Response: 1
            """
        return bool(self.instr.query('AUTO?'))

    def SetModAutoRange(self, module, auto=True):
        """
        Description
            Set the power range (Auto or Manual) for each channels.
        It is available for the “READ?” command.
        
        Syntax
            DAUTO<wsp><value1>,<value2>
        
        Parameters
        <value1>: Module 0,1, 2, 3, 4, 5
        When setting the <value 1> to 5, all channels and
        module is set to the same wavelength.
        <value2>: Range mode
        0 - Manual range
        1 - Auto range
        
        Default
            value2: 1
        
        Example
            DAUTO 0,1
        """
        assert module in range(6)
        assert auto in [True, False]
        self.instr.write(f'DAUTO {module},{auto:d}')

    def GetModAutoRange(self, module):
        """
        Description
            Check the power range (Auto or Manual) for each
        channels.
        It is available for the “READ?” command.
        
        Syntax
            DAUTO?<wsp><value>
        
        Response
            <value>: Range mode
        0 - Manual range
        1 - Auto range
        
        Example
            DAUTO? 0
        
        Response : 1
            """
        assert module in range(6)
        return self.instr.query(f'DAUTO {module}')
    
    def ReadMod(self, module):
        """
        Description
            Execute optical power or electrical current measurement
        and check the result. If sending the “READ” command
        during logging mode, logging mode stops.
        
        Syntax
            READ?<wsp><module>
        Parameter
        <module>
        Module Number: 0,1,2,3,4
        
        Response
            <value1>,<value2>, <value3>,<value4>
        value1; Optical power of port 1
        value2; Optical power of port 2
        value3; Optical power of port 3
        value4; Optical power of port 4
        
        Example
            READ?
        
        Response: -20.123,-20.454,-20.764,-20.644
            """
        assert module in range(6)
        readout = self.instr.query(f'READ? {module}')
        return np.array([float(i) for i in readout.split(',')])

    def CheckWavelength(self, module, index):
        """
        Description
            Check the wavelength that should be calibrated.
        Unit: nm
        Refer to the 5.5.6 for the method of wavelength
        compensation.
        
        Syntax
            CWAV?<wsp><module>,<index>
        Parameter
        <module>
        Module Number: 0,1,2,3,4
        <index>
        Index : Wavelength set order that would be applied -
        Integer 1,2,3~ 18,19,20
        
        Response
            <value>
        Wavelength
        Unit: nm
        
        Example
            CWAV? 0,1
        
        Response: 1250
            """
        assert module in range(6)
        assert index in range(1,21)
        return self.instr.query('CWAV {module},{index}')

    def CheckWavelengthPO(self, module, channel, index):
        """
        Description
            Power calibration value of the wavelength of “CWAV?”
        command Index.
        Unit: dB
        Refer to the 5.5.6 for the method of wavelength
        compensation.
        
        Syntax
            CWAVPO?<wsp><module>,<ch>,<index>
        Parameter
        <module>
        Module Number: 0,1,2,3,4 - Integer
        <ch>
        Port number: 1,2,3,4 - Integer
        <index>
        Index : Wavelength set order that would be applied -
        Integer 1,2,3~ 18,19
        
        Response
            <optical power offset> - float
        
        Example
            CWAVPO? 0,1,1
        
        Response: 0.904640
            """
        assert module in range(6)
        assert channel in range(1,5)
        assert index in range(20)
        return self.instr.query(f'CWAVPO {module},{channel},{index}')

    def StartMeas(self):
        """
        Description
            Command to start measuring.
        
        Syntax
            MEAS
        
        Example
            MEAS
        """
        self.instr.write('MEAS')

    def StopMeas(self):
        """
        Description
            Command to stop measuring.
        
        Syntax
            STOP
        
        Example
            STOP
        """
        self.instr.write('STOP')

    def Status(self):
        """
        Description
            Check measuring status.
        
        Syntax
            STAT?
        
        Response
            <value1>,<value2>
        <value1>: Status
        0 - Measuring is still in process.
        1 - Measurement completed.
        -1 - The measurement is forcibly stopped.
        <value2>: Measured logging point
        
        Example
            STAT?
        
        Response: 1,100
            """
        return self.instr.query('STAT?')
    
    def SetLogPt(self, point:int):
        """
        Description
            Set
        up
        measurement
        data
        point
        in
        CONST1/CONST2/FREERUN measuring mode.
        Refer to the 5.6.3 Measurement data setting (LOGN).
        
        Syntax
            LOGN<wsp><value>
        
        Parameters
        <value>: 1 ~ 1,000,000
        
        Default
            value: 1
        """
        assert 1 < point < 1e6
        self.instr.write(f'LOGN {point}')

    def GetLogPt(self):
        """Description
            Check measurement data point.
        Refer to the 5.6.3 Measurement data setting (LOGN).
        
        Syntax
            LOGN?
        
        Response
            <value>: 1 ~ 1,000,000
        
        Example
            LOGN?
        
        Response: 100
            """
        return self.instr.query('LOGN?')

    def ReadLogData(self, module, port):
        """
        Description
            Read out the logging data.
        This command is not available for RS-232 communication.
        
        Syntax
            LOGG? <wsp><value1>,<value2>
        <value1>: module number
        <value2>: port number
        
        Response
            Please refer to '5.6.4 LOGG?' for detail information.
        
        Example
            LOGG?
        
        Response: Please refer to '5.6.4 LOGG?' for detail
            information.
        """
        assert module in range(6)
        assert port in range(1,5)
        readout = self.instr.query('LOGG?')
        return np.array(readout.split(','))

    def Zero(self):
        """
        Description
            Before measuring optical power, run Zeroing to delete
        electrical DC offset. Please be careful with incidence light
        into Optic Port. When using the current meter module,
        the MPM-213, please remove the BNC cable from the
        MPM-213. This command action takes about 3 sec so
        please run other commands at least 3 sec later.
        
        Syntax
            ZERO
        
        Example
            ZERO
        """
        self.instr.write('ZERO')

class mpm(MultiPowerMeter):
    def __init__(self, port='TCPIP0::10.42.0.107::5000::SOCKET'):
        super().__init__(port)
        self.SetUnit = 1
        self.chn = 4*sum([int(i) for i in list(self.GetModStatus().split(','))])
        
    def read(self):
        return np.concatenate([self.ReadMod(i) for i in range(self.chn // 4)])

if __name__ == "__main__":
    m = mpm()
    print(m.read())
    # print(mpm.GetIP())