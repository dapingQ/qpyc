"""
Python package to communicate with dotfast 64-channel time tagger
Firmware version: 3.59.1
Inspired by Philipp Jenke Logic16 timetagger wrapper
select correct env before running
"""

import os, sys, time
from pathlib import Path
import numpy as np

import Pyro5.server
import Pyro5.core

class TimeTagger64ch():
    """
    This class controls the communication with the Time Tagger of UQ Devices
    it requires the 'pythonnet' package, install it via: pip install pythonnet
    for further documentation see: UQ Devices manual, https://uqdevices.com/documentation/
    """

    def __init__(self):
        # dynamic packages
        self.clr = None                             # clr from pythonnet package
        self.tita = None                            # TimeTag package from the .ddl file

        # device properties
        self.tagger = None                          # time tagger device
        self.unit_int = 5e-9                        # internal unit (s)
        self.time_tagger_name = 'timetagger64ch'     # name of the time tagger
        self.version = None                         # FPGA version of the device
        self.timebase = None                        # timing resolution of the device
        self.num_input = None                       # number of inputs installed on the device

        # bin file properties
        self.n_header_bytes = 0                     # number of header bytes in bin file
        self.n_tag_bytes = 8                        # number of time tag bytes in bin file
        self.n_channel_bytes = 1                    # number of channel bytes in bin file
        self.byte_order = 'little'                  # byte order: 'big' or 'little'
        self.order_reverse = True                   # False: TimeTag;Channel, True: Channel;TimeTag

        # logic and reader option, actually classes by them own
        self.logic = None                           # logic object
        self.reader = None                          # reader object

        # connect to time tagger
        self.get_lib()
        # self.initialize(dev_num=dev_num)

    # basic custom functions
    def get_lib(self):
        """
        Imports the used packages for the time tagger and reads the .dll file.
        """
        self.clr = __import__('clr')
        print('Initialization of the time tagger')
        # folder_dll = Path(Path(__file__).parents[2], 'bib', 'dll', 'dotfast')
        dll_name = 'ttInterface_3_59_01.dll'
        # sys.path.append(str(folder_dll))
        self.clr.AddReference(dll_name[:-4])
        self.tita = __import__('TimeTag')
        self.tagger = self.tita.TTInterface()

    def initialize(self, dev_num=1):
        """
        Initializes the time tagger.

        :param dev_num: number of device, only >1 for more connected devices
        :type dev_num: int
        """
        # self.get_lib()
        self.open(dev_num)
        self.get_logic()
        self.get_reader()
        self.get_info(show=True)

    def get_info(self, show=False):
        """
        Gets basic information about the time tagger.

        :param show: set for print information
        :type show: bool
        """
        self.version = self.get_fpga_version()
        self.timebase = self.get_resolution()
        self.num_input = self.get_no_inputs()
        if show:
            print( f'\nFPGA version: {self.version}' )
            print( f'Timing resolution: {self.timebase}s' )
            print( f'Number of channels installed: {self.num_input}' )

    ### Start of all the wrappper functions ###
    
    # Basic functions

    def open(self, dev_num):
        """
        This function connects to the device. It has to be called before any other function is called.

        :param dev_num: >=1, The parameter is used only when more than one units are connected at the same time.
                        If only one unit is used, this value must be set to 1
        :type dev_num: int
        """
        self.tagger.Open(dev_num)

    def close(self):
        """
        This function should be called before the program terminates.
        """
        self.tagger.Close()

    def calibrate(self):
        """
        This function is optional, because the unit is calibrated automatically.
        """
        self.tagger.Calibrate()

    def get_error_flags(self):
        """
        This function returns the internal error flags.
        Calling this function clears the flags in the device.

        :return: internal error flag
        :rtype: int
        """
        return self.tagger.ReadErrorFlags()

    def get_error_text(self, err=None):
        """
        TThis function translates the error flags to a short text that can be displayed on the user
        interface. The error flags can be obtained by GetErrorFlags() or extracted from the raw data
        stream. Both use the same encoding.

        :param err: error
        :type err: int
        :return: error description
        :rtype: str
        """
        if err is None:
            err = self.get_error_flags()
        return self.tagger.GetErrorText(err)

    def get_no_inputs(self):
        """
        This function returns the number of inputs installed on the device.
        It is used for debugging purposes only.

        :return: number of channels installed
        :rtype: int
        """
        return self.tagger.GetNoInputs()

    def get_resolution(self):
        """
        This function returns the time resolution of the device. 
        It should be used to calculate absolute time values.

        :return: timing resolution (s)
        :rtype: float
        """
        return self.tagger.GetResolution()

    def set_voltage_threshold(self, channel, threshold):
        """
        Sets the voltage threshold for a channel.

        :param channel: channel number from 1 to 64
        :type channel: int
        :param threshold: voltage threshold (V) from -2.0V to 2.0V
        :type threshold: float
        """
        if not 1 <= channel <= self.num_input:
            raise ValueError
        if not -4.0 <= threshold <= 4.0:
            raise ValueError
        self.tagger.SetInputThreshold(int(channel), threshold)

    def set_inversion_mak(self, mask):
        """
        This function is maintained for compatibility only. Please use SetNegEdge().
        """
        self.tagger.SetInversionMask(mask)

    def set_delay(self, channel, delay):
        """
        All input signals can be delayed internally. This is useful to compensate external cable delays.

        :param channel: channel number from 1 to 64
        :type channel: int
        :param delay: 25 bit value, delay in internal units, see get_resolution function
        :type delay: int
        """
        self.tagger.SetDelay(channel, delay)

    def get_fpga_version(self):
        """
        This function returns the current version of the FPGA design. 
        It is used for debugging purposes only.

        :return: FPGA version
        :rtype: int
        """
        return self.tagger.GetFpgaVersion()

    def get_logic(self):
        """
        This function returns the "Logic" object, that contains the Counter / Logic functions
        """
        self.logic = self.tagger.GetLogic()
        
    def freeze_single_counter(self):
        """
        This function stores all the single counters synchronously.
        This function also returns the time between the
        last two calls to FreezeSingleCounter. 
        The time is expressed in 4 ns ticks.

        Note: This function is implemented in software versions above 3.45. 
        Please use Logic object for older versions.
        """
        return self.tagger.FreezeSingleCounter()

    def get_single_count(self, channel):
        """
        This returns the number of input pulses
        in between the last two calls of FreezeSingleCounter.
        This example calculates the frequency of input 4:

        double time = FreezeSingleCounter();
        int pulses = GetSingleCount(4);
        double frequency = pulses / time;

        Note: This function is implemented in software versions above 3.45. 
        Please use Logic object for older versions.

        :param channel: channel number from 1 to 64
        :type channel: int
        :return: number of arrived counts
        :rtype: int
        """
        return self.tagger.GetSingleCount(int(channel))

    def set_led_brightness(self, brightness):
        """
        Sets the brightness of the LED on the front panel.
        Note: This function is implemented in software versions above 3.45 and FPGA Version 1.46.

        :param brightness: brightness of the LED's in percent
        :type brightness: int
        """
        self.tagger.SetLedBrightness(brightness)

    def enable_input(self, channel, enable):
        """
        This can be used to disable inputs. After startup all inputs are enabled.

        :param channel: channel number from 1 to 64
        :type channel: int
        :param enable: enable status
        :type enable: bool

        :return: None
        """
        self.tagger.EnableInput(channel, enable)

    def read_input_status(self, channel):
        """
        This function checks if the input is currently low or high.
        This can be useful while adjusting the input levels.

        :param channel: channel number from 1 to 64
        :type channel: int
        :return: stautus
        :rtype: bool
        """
        return self.tagger.ReadInputStatus(int(channel))

    def set_neg_edge(self, channel, neg):
        """
        After startup, the unit is configured to trigger on the positive edge.
        By calling this function with neg= true, the corresponding input is defined as the negative edge.

        This is an alternative to the function SetInversionMask.
        
        :param channel: channel number from 1 to 64
        :type channel: int
        :param neg: negative edge
        :tyoe neg: bool
        """
        self.tagger.SetNegEdge(channel, neg)

    def load_temporal_walk_correction(self, file):
        """
        When a detector triggers twice within a short time interval,
        the time of the second pulse tends to be off because the detector is not fully recovered yet.
        This can be compensated with this function. Please call factory for details.

        :param file: file name
        :type file: string
        """
        self.tagger.LoadTemporalWalkCorrection(file)

    # Time Tag Readout

    # The current software interface is single-threaded and can support about 200-300 MTags,
    # depending on the computer. At time of this writing, the full data rate can only be saved to disk.
    # If you want to do real-time processing of the data, please contact factory.
    # At an internal FIFO overflow, the DataOverflow flag is set and the error led on the front
    # panel is lit.
    # The following functions are implemented in the class TimetagReader. You get a handle to the
    # TimetagReader by calling TTInterface.GetReader();

    def start_timetags(self):
        """
        This function puts the device into time-tag readout mode.
        The time tags are written into the internal fifo.
        The background thread starts to read the time tags into the RAM of the computer.
        """
        self.reader.StartTimetags()

    def stop_timetags(self):
        """
        The tags are no longer written into internal fifo. The background thread is stopped.
        """
        self.reader.StopTimetags() # not sure in which class

    def tags_present(self):
        """
        This function returns true when tags are ready to read.
        This function is optional.

        :return: state if time tags are ready to read
        :rtype: bool
        """
        return self.tagger.TagsPresent()

    #skip ReadNextTags, as not working for python

    def read_next_tag_value(self):
        """
        This is the very same functionality as ReadNextTag, but optimized for Python.
        It returns either null (= none) or a struct Result.
        """
        return self.reader.ReadNextTagValue()

    def read_tags(self, channels, timetags):
        """
        Return value: size of arrays
        time[n] is the absolute time in internal units. (15.625ps). This value is returned by
        GetResolution().
        Channel [n] is the number of the corresponding input. The first input is number 1.
        The “virtual channel” 117 is used for the overflow tag. The overflow tag is sent whenever a
        data overflow error occurs. The data overflow tag indicates, that some data is missing at this
        point.
        When there are no tags present, this function may wait up to 300 ms before it returns a zero
        result. When you don't want this behavior, use TagsPresent() to check availability first. The
        array is sorted by time. When two tags occur at the same time, then the tag with the smaller
        channel number is transmitted first.
        The array is allocated by the driver software and returned to user code with an out parameter.
        Returning with an out parameter is similar to returning values by a pointer or reference in C /
        C++;
        The arrays can be used until the next call of ReadTags. When the data is needed for a longer
        time it has to be copied to a different array.
        
        :param channels: empty channel list
        :type channels: list
        :param timetags: empty time tags list
        :type timetags: list
        :return: number of time tags, channel list, time tags list
        :rtype: int, list, list
        """
        return self.tagger.ReadTags(channels, timetags)

    # 10 MHz Input

    # The 10 MHz input can be used to increase the long-term stability of the device.
    # It has to be switched on by software to be used.

    def use_10_mhz(self, state):
        """
        When the 10 MHz input is switched on, but no valid signal is connected to the input,
        an error flag is set and the error led on the front panel is lit.

        :param state: state of the 10 MHz input
        :type state: bool
        """
        self.tagger.Use10MHz(state)

    # save to file

    # The software interface offers a high performance interface to save data to disk. The data is
    # saved in a compressed, binary format and can be converted to ASCII offline.

    def get_reader(self):
        """
        Get reader object
        """
        self.reader = self.tagger.GetReader()

    def start_saving(self, filepath):
        """
        Starts saving the time tag data on the local hard drive.

        :param filepath: filepath to a .tt file
        :type filepath: str
        """
        self.reader.StartSaving(filepath)

    def stop_saving(self):
        """
        Stops saving the time tags to the local hard drive.
        """
        self.reader.StopSaving()

    def start_converting(self, input_file, output_file):
        """
        Converts the time tag data file to a binary or txt file, set the format by the set_conversion_binary() function.

        :param input_file: path to the input .tt file
        :type input_file: str
        :param output_file: path to the output .bin or .txt file
        :type output_file: str
        """
        self.reader.StartConverting(input_file, output_file)

    def wait_until_conversion_finished(self):
        """
        Waits until the conversion from the .tt-file to a .bin-file or .txt-file finished.
        """
        self.reader.WaitUntilConversionFinished()

    def set_conversion_binary(self, state=True):
        """"
        The generated file can be either text or binary. Binary mode is selected by default
        self.reader.SetConversionBinary(state)

        :param state: state of conversion mode
        :type state: bool
        """
        self.reader.SetConversionBinary(state)

    # Counter Functions
    # There are two types of counter. Single counter and pattern counter.
    
    # Single counter
    # There are 64 single counter, one for each input. They are working constantly, independent of
    # all other functions. They are present in all devices (TDM800, TDM1600, Logic 64)
    
    # Pattern counter
    # These count special conditions that are interesting in the experiment. This conditions are
    # called pattern and are defined using DefinePattern and DefinePatternNeg functions. For
    # advanced cases SetCompactorBit and SetCompactorCount can also be used.

    # The pattern counter functions are located in the "Logic" object. In .NET It can be obtained by
    # the ttInterface object by the call "GetLogic()". In C++ it can by obtained by the CTimeTag
    # object.

    def switch_logic_mode(self):
        """
        This function is implemented for compatibility with older Logic-16 devices. In current devices
        the counter and time-tag can run simultaneously.
        """
        self.logic.SwitchLogicMode()

    def read_logic(self):
        """
        Please call this function before you read any counters. The calls to ReadLogic defines the
        measurement interval.
        This function takes a snapshot of all counter. All counter keep running in the background, so
        no events are lost during readout. All following functions read these snapshots. This ensures
        that all values correspond to the exact same time interval.
        When you use ReadLogic() please do not call FreezeSingleCounter() because ReadLogic
        also freezes the single counter.

        :return: not needed
        :rtype: int array?
        """
        try:
            self.logic.ReadLogic()
        except self.tita.UsbException:
            pass

    def get_time_counter(self):
        """
        This function returns the time between the last two calls to ReadLogic() in 4ns increments.
        This function is provided for compatibility.

        :return: time between two calls of ReadLogic() (4ns)
        :rtype: int
        """
        return self.logic.GetTimeCounter()

    def get_time(self):
        """
        This function returns the time between the last two calls to ReadLogic() in seconds
        increments.

        :return: time between two calls of ReadLogic() 
        :rtype: float
        """
        return self.logic.GetTime()

    def get_pattern_count(self, pattern_no):
        """
        This function returns the number of times in the corresponding pattern occurred.

        :param pattern_no: pattern number
        :type pattern_no: int
        :return: number of times
        :rtype: int
        """
        return self.logic.GetPatternCount(pattern_no)

    def define_pattern(self, pattern_no, posmask):
        """
        Please note that the index starts at 0. Input 1 is sented by 0, input 2 by bit 1 and so on.
        Example: DefinePattern (27, 3);
        This defines pattern 27 to be the "AND" gate of the first two inputs. Counter 27 will count,
        when input 1 and input 2 both have an active edge within the coincidence window.
        Please Note:
        Defining patterns takes some time. During this time, the pattern counter can be
        showing unexpected results. Please only call this function, when something is
        changed.
        
        :param pattern_no: Number of pattern to define.
        :type pattern_no: int
        :param posMask: 64 bit mask of the inputs that have to be present for the pattern to be active.
        :type posmask: unsigned long
        """
        return self.logic.DefinePattern(pattern_no, posmask)
        
    def define_pattern_neg(self, pattern_no, posmask, negmask):
        """
        Define both positive and negative pattern

        :param pattern_no: Number of pattern to define.
        :type pattern_no: int
        :param posMask: Bitmask of the inputs that have to be active for the pattern to count.
        :type posmask: unsigned long
        :param posMask: Bitmask of the inputs that must not be active for the pattern to count.
        :type posmask: unsigned long
        """
        return self.logic.DefinePatternNeg(pattern_no, posmask, negmask)

    def set_window_width(self, window):
        """
        This sets the width to the coincidence window. The value is given in internal units. (15.625
        ps) The width can be quite large, that is nice for testing and finding right delays. However, the
        window should not be so large that one input has several pulses in the window. In that case
        the count is not accurate and an error flag is raised.

        :param window: coincidence window
        :type window: int
        """
        return self.logic.SetWindowWidth(window)
    
    def set_window_width_ex(self, channel, window):
        """
        This allows different coincidence windows for different inputs. When both window functions
        are called, SetWindowWidth has to be called first because it just sets the width of all inputs.
        
        :param channel: input channel to set different coincidence window
        :type channel: int, 1- 64
        :param window: coincidence window
        :type window: int
        """
        return self.logic.SetWindowWidth(channel, window)
        
    # Bitcount Feature

    # The unit allows arbitrary logic functions for groups of 4 neighboring channels. (1-4, 5-8, 9-
    # 12 ..) This can be used to define pattern in terms of number of photons. For historic reasons,
    # this unit is called "compactor".
    # This is an advanced feature that is not needed for normal operation.
    # Important:
    # The compactor functions have to be called before any call to DefinePattern or
    # DefinePatternNeg.
    # To define the compactor memory you have two options. This is the "photon counting memory"
    # ( I called it "compactor" because it used to reduce the 64 inputs to 32.)

    def set_compactor_count(self, channel, bitcount):
        """
        Bitcount is the number of photons in the group, 1-4
        Bitcount "-1" means don't use counter function, use the input as it is. That's the default value.
        (Corresponding to the "+" symbol in TimeTagExplorer)

        :param channel: channel number
        :type channel: int
        :param bitcount: number of photons in the group, 1-4
        :type bitcount: int
        """
        return self.logic.SetCompactorCount(channel, bitcount)

    def set_compactor_bit(self, channel, index, value):
        """
        Using this function you have full control over the memory. Please contact factory for details.
        
        :param channel: channel number, 1-64
        :type channel: int
        :param index: 0-15 memory address
        :type channel: byte
        :param value: memory bit
        :type value: bit
        """
        return self.logic.SetCompactorBit(channel, index, value)

    ### End of all the wrapper methods ###

    @staticmethod
    def single_channel_to_num_pattern(channel):
        """
        Converts the logic pattern of a single channel into the number representing this event pattern.

        :param channel: channel number from 1 to 64
        :type channel: int
        :return: number representing the event pattern
        :rtype: int
        """
        return 2 ** (channel - 1)

    @staticmethod
    def pattern_to_num_pattern(pattern):
        """
        This functions converts a event pattern into the integer value.

        :param pattern: event pattern with 0 or 1 for each channel
        :type pattern: numpy array with length of 64
        :return: number representing the event pattern
        :rtype: int
        """
        return pattern.dot(1 << np.arange(pattern.size)[::-1])

    @staticmethod
    def num_pattern_to_pattern(num):
        """
        This function converts the number of an event pattern to the event pattern.

        :param num: number representing the event pattern
        :type num: int
        :return: event pattern with 0 or 1 for each channel
        :rtype: numpy array with length of 64
        """
        return np.array([int(char) for char in np.binary_repr(num, width=64)])

    
    @staticmethod
    def remove_eol_char_from_bin_file(input_file, output_file, old_seq=b'\r\n', new_seq=b'0'):
        """
        This function removes the end of line characters of a saved .bin-file.

        :param input_file: path to the input .bin file with eol
        :type input_file: str
        :param output_file: path to the output .bin without eol
        :type output_file: str
        :param old_seq: old byte sequence
        :type old_seq: bytearray
        :param new_seq: new byte sequence
        :type new_seq: bytearray
        """
        input_file_open = open(input_file, "rb")
        output_file_open = open(output_file, "wb")
        chunk = 100_000_000
        old_seq_len = len(old_seq)
        while True:
            data = input_file_open.read(chunk)
            data_size = len(data)
            seek_len = data_size - data.rfind(old_seq) - old_seq_len
            if seek_len > old_seq_len:
                seek_len = old_seq_len
            data = data.replace(old_seq, new_seq)
            output_file_open.write(data)
            input_file_open.seek(-seek_len, 1)
            output_file_open.seek(-seek_len, 1)
            if data_size < chunk:
                break
        input_file_open.close()
        output_file_open.close()

    def converting_temp_time_tag_file_to_bin_file_wo_eol(self, input_file, output_file):
        """
        Converts the temporal .tt-file to a .bin file without end of line characters

        :param input_file: path to the input .tt file
        :type input_file: str
        :param output_file: path to the output .bin file
        :type output_file: str
        """
        self.set_conversion_binary(True)
        self.start_converting(input_file + '.tt', output_file + '.eolbin')
        self.wait_until_conversion_finished()
        self.remove_eol_char_from_bin_file(output_file + '.eolbin', output_file + '.bin')
        os.remove(output_file + '.eolbin')


    def get_countrate(self, channel=1, exp_time=1):
        """
        Performs a countrate measurement.

        :param channel: used channel
        :type channel: int
        :param exp_time: exposure time (s)
        :type exp_time: float
        :return: count rate (Hz)
        :rtype: float
        """
        self.freeze_single_counter()
        time.sleep(exp_time)
        exp_time_meas = self.freeze_single_counter()
        
        counts = self.get_single_count(channel)
        countrate = counts / exp_time_meas
        return countrate

    def set_coincidence(self, pattern_no=1, channels=[1,2], threshold=0.05, window=150):
        """
        Get coincidence couting in a expected integration of time

        :param pattern_no: pattern number of counter
        :type pattern_no: int
        :param channels: list of coincidence channel
        :type channels: list
        :param threshold: voltage threshold (V) from -2.0V to 2.0V
        :type threshold: float
        :param window: coincidence window
        :type window: int
        """
        
        [ self.set_voltage_threshold(channel=ch, threshold=threshold) for ch in channels ]
        self.define_pattern( pattern_no, ch2pos(channels) )
        self.set_window_width( window )

    def get_coincidence(self, pattern_no=1, channels=[1,2], exp_time=1):
        
        self.freeze_single_counter()
        time.sleep(exp_time)
        exp_time_meas = self.freeze_single_counter()

        single_counts = [ self.get_single_count(i) for i in channels]
        cc_counts = self.get_pattern_count(pattern_no=pattern_no)
        return exp_time_meas, single_counts, cc_counts

def record_time_tags():
    """
    Basic example to record time tags
    """
    tt = TimeTagger64ch()
    tt.get_resolution()
    
    file_name = 'test_tags'
    tt.get_reader()
    time.sleep(2)
    tt.start_saving(file_name + '.tt')
    time.sleep(2)
    tt.stop_saving()
    
    tt.set_conversion_binary(False)
    tt.start_converting(file_name + '.tt', file_name + '.txt')
    tt.wait_until_conversion_finished()
    tt.converting_temp_time_tag_file_to_bin_file_wo_eol(file_name, file_name)
    tt.close()

def ch2pos(channels):
    return sum([2**(i-1) for i in channels])

def test_single_countrate(channel, exp_time, threshold=0.05):
    tt = TimeTagger64ch()
    tt.initialize()
    time.sleep(2)
    print(tt.get_error_text())
    tt.set_voltage_threshold(channel=channel, threshold=threshold)
    print('\nChannel {:d}'.format(channel))
    for _ in range(3):
        print('Countrate: {:.2f}Hz'.format(tt.get_countrate(channel=channel, exp_time=exp_time)))
    tt.close()

def test_coincidence( pattern_no=1, channels=[9,13], exp_time=1, threshold=0.05, window=150):
    tt = TimeTagger64ch()
    tt.initialize()
    time.sleep(2)
    print(tt.get_error_text())
    tt.set_coincidence(pattern_no=pattern_no, channels=channels, threshold=threshold, window=window)

    for _ in range(3):
        t, sc, cc = tt.get_coincidence(exp_time=exp_time)
        print(f'In {t} second')
        print(f'Single counting in channel {channels}: {sc}')
        print(f'Coincidence Counting: {cc}')
    
    tt.close()

# def convert_file():
#     input_path = os.path.join(pathlib.Path.home(), 'Nextcloud', 'graphene_lab_data', 
#                                 'data', 'timetag',
#                               'temp', 'time_tags')
#     output_path = os.path.join(pathlib.Path.home(), 'Nextcloud', 'graphene_lab_data',
#                                 'data', 'timetag',
#                                'temp', 'time_tags')
#     TimeTagger64ch.converting_temp_time_tag_file_to_bin_file_wo_eol(input_path, output_path)

def remove_eol():
    tt = TimeTagger64ch()
    input_path = os.path.join(Path.home(), 'Desktop', 'spdc_g2_60s_210504')
    tt.remove_eol_char_from_bin_file(input_path + '.eolbin', input_path + '.bin')

def server():
    """
    Expose timetagger instance using Pyro5
    """
    tt = TimeTagger64ch()
    daemon = Pyro5.server.Daemon()
    ns = Pyro5.core.locate_ns()
    uri = daemon.register(tt)
    print(uri)
    ns.register('tt64', uri)
    daemon.requestLoop()

if __name__ == '__main__':

    # remove_eol()
    # convert_file()
    # print(TimeTagger64ch.pattern_to_num_pattern(np.array([1,0,0,1])))
    # test_single_countrate()
    test_coincidence()
    # server()
   
