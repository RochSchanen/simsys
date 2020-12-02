#!/usr/bin/python3
# file: library.py
# content: system simulator library
# created: 2020 November 14 Saturday
# modified:
# modification:
# author: roch schanen
# comment: device library

# import core classes
from core import Device, inPort, outPort, randbit

# used to determine the minimum number of bits from an integer value 
from numpy import log as ln
from math import ceil

# to fix end of line OS dependence
from os import linesep as _EOL
_EOLN = -len(_EOL) 

# CLOCK ##############################################################

# a clock device has no input and one output
# the outputs value depends only on time
# the clock behaviour is definied by the following parameters: 
# - "period" is the period (1/frequency) in ns.
# - "shift" is the delay of the clock pulse in ns.
# - "width" is the pulse length of the clock signal in ns.
# a zero shift means that the rising edge of the pulse starts at the
# beginning of the period. the width value plus the shift value should
# not exceed a full period. the clock signal is defined from time 0ns
# and has its level set at start up.

class clock(Device):

    genericName = 'clk'

    def __init__(
            self,
            period = 20,    # clock period: 20ns, 50MHz
            shift  = 10,    # phase shift : 0ns, in-phase
            width  = 10,    # pulse width : 10ns, symmetrical
            count  = None,  # number of pulses: None is continuous
            name   = None): # device name : None, use generic

        # call Device class constructor
        Device.__init__(self, name)
        # record configuration
        self.configuration = period, width, shift
        # instantiate output ports
        self.Q = outPort(1, "Q")
        # register port
        self.outports.append(self.Q)
        # setup counter
        self.count = count
        # clock phase state
        self.phase = (0 - shift) % period
        # set default output ports value
        self.Q.set(['0','1'][self.phase < width])

        # done
        return

    def display(self):
        # get name
        name = self.name
        # get configuration
        period, width, phase = self.configuration
        # get current values
        value = f"Q={self.Q.get()}"
        # display
        print(f"<clock> {name}")
        print(f"  period: {period}")
        print(f"  width : {width}")
        print(f"  phase : {phase}")
        print(f"  count : {self.count}")
        print(f"  value : {value}")
        return

    def updateOutputPorts(self, timeStamp):
        # save current Q state for edge detection
        state = self.Q.get()
        # get configuration
        period, width, shift = self.configuration
        # pulse train completed
        if self.count == 0: return
        # compute period phase
        self.phase = (timeStamp - shift) % period
        # update ouputs values
        self.Q.set(['0','1'][self.phase < width])
        # continuous pulse train
        if self.count == None: return
        # catch rising event
        rising = (state, self.Q.get()) == ('0','1')
        # count down
        if rising: self.count -= 1
        # done
        return

# COUNTER ############################################################

# a counter device has a binary output value.
# the number of bits is define by the value of size.
# n bits means counting from 0 to 2^n-1.
# asynchronous reset: counter is clear whenever 'clr' is low
# synchronous counting: increment at the rising edge of 'trg'
# the counter value is coerced to modulo 2^n by clearing bits with a
# weight larger than 2^n-1.  the counter output is defined from 0ns
# and has a random value

class counter(Device):

    genericName = 'cnt'

    clr = None # clear
    trg = None # trigger

    def __init__(
            self,
            size = 4,     # counter width: 4bits, 0 to 15
            name = None): # device name: None, use generic

        # call Device class constructor
        Device.__init__(self, name)
        # record configuration
        self.configuration = size
        # instantiate output port
        self.Q = outPort(size, "Q")
        # register port
        self.outports.append(self.Q)
        # set output port initial value
        self.Q.set(randbit(size))

        # done
        return

    def addTrigger(self, port):
        # instantiate input port
        self.trg = inPort(port, "trg")
        # register port
        self.inports.append(self.trg)
        return

    def addClear(self, port):
        # instantiate input port
        self.clr = inPort(port, "clr")
        # register port
        self.inports.append(self.clr)
        return

    def display(self):
        # get name
        name = self.name
        # get configuration
        size = self.configuration
        # get current values
        value = f'Q={self.Q.get()[::-1]}'
        # display
        print(f"<counter> {name}")
        print(f"  size  : {size}")
        print(f"  value : {value}")
        return

    def updateOutputPorts(self, timeStamp):
        # get configuration
        size = self.configuration
        # asynchronous clear on active low
        if self.clr:
            if self.clr.state == '0':
                # clear output
                self.Q.set(f'{0:0{size}b}')
                return
        # update on rising edge of trigger
        if self.trg:
            if self.trg.rising:
                # get incremented state
                n = int(self.Q.get()[::-1], 2) + 1 
                # make n string, LSB(size) only
                newvalue = f'{n:0{size}b}'[-size:]
                # update output value
                self.Q.set(newvalue[::-1])
                return
        # done
        return

# ROM ################################################################

# the look up table logic allows to built arbitrary gate logic. the
# number of input must match the table size: for n inputs, a 2^n
# values table must be defined. an input combinaison defines an adress
# that points to the table. Adress zero points to the left most
# character in the table string. the least significant bit of the
# address is defined by the first registered input. the most
# significant bit of the address is defined by the last input
# registered.

class rom(Device):

    genericName = 'rom'

    # the default values makes the rom equivalent to a lut 2-NAND
    def __init__(
            self,
            table = '1110', # NAND table, two bit address expected
            width = 1,      # data bus width, one bit output
            name  = None):  # device name: None, use generic

        # call parent class constructor
        Device.__init__(self, name)
        # find number of words
        words = ceil(len(table)/width)
        # size in power of 2
        size = ceil(ln(words)/ln(2))
        # complete table up to 2^size
        table += 'U'*(2**size-words)*width
        # record configuration
        self.configuration = size, width, table
        # instantiate output port
        self.Q = outPort(width, "Q")
        # register port
        self.outports.append(self.Q)
        # set default output port value
        self.Q.set(table[0:width])

        # done
        return

    def addAddress(self, port, subset = None):
        # instantiate input port
        newport = inPort(port, f"A{len(self.inports)}", subset)
        # register port
        self.inports.append(newport)
        return

    def display(self):
        # get name
        name = self.name
        # get configuration
        size, width, table = self.configuration
        # get current value
        value = f"Q={self.Q.get()[::-1]}"
        # display
        print(f"<read only memory> {name}")
        print(f"  size  : {2**size}x{width}")
        print(f"  value : {value}")
        s =   f"  table : "
        # get alignement
        n = len(s)
        # scan through table
        for i in range(2**size):
            # build up display string
            s += f"{table[i*width:(i+1)*width][::-1]} "
            # end of line above 40 characters
            if len(s) > 40: print(f"{s}"); s = n*" "
        # print remain of the table
        if len(s) > n: print(f"{s}")
        # build address string
        s = ""
        for p in self.inports:
            s += p.get()
        # detect size mismatch error
        if not size == len(s):
            print(f"  Size mismatch.")
            print(f"    {size} input(s) expected.")
            print(f"    {len(s)} input(s) found.")
            print(f"  Exiting...")
            exit()
        return

    def updateOutputPorts(self, timeStamp):
        # get configuration
        size, width, table = self.configuration
        # get table input address
        s, a, w = "", 0, 1
        for p in self.inports:
            s += p.get()
        for c in list(s):
            a += w*['0','1'].index(c)
            w <<= 1
        # update output value
        self.Q.set(table[a*width:(a+1)*width])
        # done
        return

# GET ROM DATA FROM FILE #############################################

def GetRomFromFile(filename):
    # read file and collect data
    rom, b, n = '', None, 0
    fh = open(filename,'r')
    l = fh.readline()
    while l:
        s = l.rstrip('\r\n')
        l = fh.readline()
        n += 1
        # skip empty line        
        if not s: continue
        # skip commented line
        if s[0] == '#': continue
        # select numeric representation
        print(s)
        if s[0] == '%':
            if s[1:].strip() == 'BINARY': b = 2; continue
            if s[1:].strip() == 'DECIMAL': b = 10; continue
            if s[1:].strip() == 'HEXADECIMAL': b = 16; continue
            print(f'unknown command "{s[1:].strip()}", current line is {n}')
            exit()
        # set default to hexadecimal
        if not b: b = 16
        # append data to the table
        for w in s.split():
            rom += f'{int(w, b):08b}'[::-1]
    return rom

######################################################################

if __name__ == "__main__":

    from sys import version as pythonVersion

    print("file: library.py")
    print("content: system simulator library")
    print("created: 2020 November 14 Saturday")
    print("author: roch schanen")
    print("comment: device library")
    print("run Python3:" + pythonVersion)

    from core import system

    # instantiate a simulator system
    S = system("version 0.00")
    
    # instantiate a clock
    cl = S.add(clock(name = 'Clock'))

    # instantiate a reset from counter
    rs = S.add(clock(100, 35, 65, count = 1, name = 'Reset'))

    # instantiate a counter
    cn = S.add(counter(name = 'Counter'))
    cn.addTrigger(cl.Q)
    cn.addClear(rs.Q)

    # instantiate rom 4x1 bits: NAND gate
    nd = S.add(rom('1110', name = 'NAND')) 
    nd.addAddress(cn.Q, [0, 1])

    # instantiate rom 16x8 bits
    rm = S.add(rom(GetRomFromFile('rom.txt'), 8, name = 'ROM')) 
    rm.addAddress(cn.Q)

    # show all devices defined
    S.displayDevices()

    # open export file
    S.openFile()

    # run simulator 
    S.runUntil(500) # 150ns
    
    # close export file
    S.closeFile()
