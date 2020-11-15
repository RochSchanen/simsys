#!/usr/bin/python3
# file: library.py
# content: system simulator library
# created: 2020 November 14 Saturday
# modified:
# modification:
# author: roch schanen
# comment: device library

# import core classes
from core import Device, inPort, outPort

# import random generator for initialising registers bits
from numpy.random import randint as rnd

# used to determine the minimum number of bits from an integer value 
from numpy import log as ln

# RESET ##############################################################

# a reset has no input
# a reset has a single output
# the output value depends only on time
# the reset behaviour is definied by the following parameter 
# - "width" is the pulse length of the reset signal in ns.
# the reset signal occurs only once and starts exactly at the same
# time than the simulation run

class reset(Device):

    genericName = 'rst'

    def __init__(
            self,
            width = 1,     # pulse width: 1ns, one cycle
            name  = None): # device name: None, use generic

        # call Device class constructor
        Device.__init__(self, name)
        # record configuration
        self.configuration = width
        # instantiate output port
        self.P = outPort(1, "P")
        self.Q = outPort(1, "Q")
        # register port
        self.outports.append(self.P)
        self.outports.append(self.Q)
        # set default output ports value
        self.P.set('1')
        self.Q.set('0')
        # done
        return

    def display(self):
        # get name
        name = self.name
        # get configuration
        width = self.configuration
        # get current values
        value = f"{self.Q.get()}"
        # display
        print(f"reset: {name},{width},{value}")
        return

    def updateOutputPorts(self, timeStamp):
        # get configuration
        width = self.configuration
        # compute new state
        m = timeStamp
        # update output value
        self.P.set(['0','1'][m < width])
        self.Q.set(['1','0'][m < width])
        # done
        return

# CLOCK ##############################################################

# a clock has no input
# a clock has a single output
# the output value depends only on time
# the clock behaviour is definied by the following parameters: 
# - "period" is the period (1/frequency) in ns.
# - "width" is the pulse length of the clock signal in ns.
# - "phase" is the delay of the clock pulse in ns.
# a zero phase means that the rising edge of the pulse starts at the
# beginning of the period. the width plus the phase should not exceed
# the period.

class clock(Device):

    genericName = 'clk'

    def __init__(
            self,
            period = 20,    # clock period: 20ns, 50MHz
            width  = 10,    # pulse width : 10ns, symmetrical
            phase  = 0,     # phase shift : 0ns, in-phase
            name   = None): # device name : None, use generic

        # call Device class constructor
        Device.__init__(self, name)
        # record configuration
        self.configuration = period, width, phase
        # instantiate output ports
        self.P = outPort(1, "P")
        self.Q = outPort(1, "Q")
        # register port
        self.outports.append(self.P)
        self.outports.append(self.Q)
        # set default output ports value
        self.P.set('1')
        self.Q.set('0')

        # done
        return

    def display(self):
        # get name
        name = self.name
        # get configuration
        period, width, phase = self.configuration
        # get current values
        value = f"{self.P.get()},{self.Q.get()}"
        # display
        print(f"clock: {name},{period},{width},{phase},{value}")
        return

    def updateOutputPorts(self, timeStamp):
        # get configuration
        period, width, phase = self.configuration
        # compute new state
        m = (timeStamp-phase) % period
        # update ouputs values
        self.P.set(['0','1'][m < width])
        self.Q.set(['1','0'][m < width])
        # done
        return

# COUNTER ############################################################

# size is the number of bits.
# n bits means counting from 0 to 2^n-1.
# asynchronous reset: counter is clear whenever 'clr' is low
# synchronous counting: increment at the rising edge of 'trg'
# the counter value is coerced to modulo 2^n by clearing bits with a
# weight larger than 2^n-1

class counter(Device):

    genericName = 'cnt'

    clr = None # clear
    trg = None # trigger
    wrt = None # write / count
    ena = None # enable
    cse = None # chip select

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
        # set initial output port value
        self.Q.set(f'{rnd(size):0{size}b}')  # random
        # to init with unknown value, use "self.Q.set('U'*size)"
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
        value = self.Q.get()
        # display
        print(f"counter: {name},{size},{value}")
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
                n = int(self.Q.get(), 2) + 1
                # make n string, LSB(size) only
                newvalue = f'{n:0{size}b}'[-size:]
                # update output value
                self.Q.set(newvalue)
                return
        # done
        return

# LUT ################################################################

# the look up table logic allows to built arbitrary gate logic.
# the number of input must match the table size:
# for n inputs, a 2^n values table must be defined.
# an input combinaison defines an adress that points to the table.
# Adress zero points to the left most character in the table string.
# the most significant bit of the address is defined by the first
# registered input. the least significant bit of the address is
# defined by the last input registered.
#
# examples of standard 2 inputs gates:
# _OR2   = "0111"
# _AND2  = "0001"
# _NAND2 = "1110"
# 
# examples of standard 3 inputs gates:
# _OR3   = "01111111"
# _AND3  = "00000001"
# _NAND3 = "11111110"

class lut(Device):

    genericName = 'lut'

    def __init__(
            self,
            table = '1110', # lut table: a 2 inputs NAND gate
            name  = None):  # device name: None, use generic

        # call parent class constructor
        Device.__init__(self, name)
        # compute size
        size = int(ln(len(table))/ln(2))
        # record configuration
        self.configuration = size, table
        # instantiate output port
        self.Q = outPort(1, "Q")
        # register port
        self.outports.append(self.Q)
        # set default output port value (random bits)
        self.Q.set('U')
        return

    def addInput(self, port, subset = None):
        # instantiate input port
        newport = inPort(port, f"I{len(self.inports)}", subset)
        # register port
        self.inports.append(newport)
        return

    def display(self):
        # get name
        name = self.name
        # get configuration
        size, table = self.configuration
        # get current value
        value = self.Q.get()
        # display
        print(f"lut: {name},{size},{table},{value}")
        # detect size mismatch error
        s = ""
        for p in self.inports:
            s += p.get()
        if not size == len(s):
            print(f"  Size mismatch.")
            print(f"    {size} input(s) expected.")
            print(f"    {len(s)} input(s) found.")
            print(f"  Exiting...")
            exit()
        return

    def updateOutputPorts(self, timeStamp):
        # get configuration
        size, table = self.configuration
        # get table input address
        s, a, w = "", 0, 1 << (size-1)
        for p in self.inports:
            s += p.get()
        for c in list(s):
            a += w*['0','1'].index(c)
            w >>= 1
        # update output value
        self.Q.set(table[a])
        # done
        return

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
    
    # instantiate a reset signal
    rst0 = S.add(reset(5))

    # instantiate a clock
    clk0 = S.add(clock())

    # instantiate a counter
    cnt0 = S.add(counter())

    # define counter input network
    cnt0.addTrigger(clk0.Q)
    cnt0.addClear(rst0.Q)

    # instanciate a 4 input lut
    #            I0 = 0101010101010101
    #            I1 = 0011001100110011
    #            I2 = 0000111100001111
    #            I4 = 0000000011111111
    lut0 = S.add(lut('1000100010001000'))

    # define lut input network
    lut0.addInput(cnt0.Q)
    # lut0.addInput(cnt0.Q, [0])
    # lut0.addInput(cnt0.Q, [1])
    # lut0.addInput(cnt0.Q, [2])
    # lut0.addInput(cnt0.Q, [3])

    # show all devices defined
    S.displayDevices()

    # open export file
    S.openFile()

    # run simulator 
    S.runUntil(350) # 150ns
    
    # close export file
    S.closeFile()
