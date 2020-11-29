#!/usr/bin/python3
# file: development.py
# content: development code
# created: 2020 November 14 Saturday
# modified:
# modification:
# author: roch schanen
# comment: system architecture simulator

from sys import version as pythonVersion

print("file: development.py")
print("content: system simulator development")
print("created: 2020 November 14 Saturday")
print("author: roch schanen")
print("comment:")
print("run Python3:" + pythonVersion);

# to fix end of line OS dependence
from os  import linesep as _EOL
_EOLN = -len(_EOL) 

# to compute address size
from numpy import log as ln
from math import ceil

# exit on error
from sys import exit

# import core classes
from core import system, inPort, outPort, Device, randbit
from library import clock, counter

# RAM ################################################################

# ----------->
            # the RAM device is defined by a binary "table" and a "width". the
            # input ports form a binary address that must match the table size.
            # for n inputs, a 2^n values table must be defined. if the table does
            # not match the size, the table will be extended with 'U' bits. the
            # address "zero" points to the left most character in the binary table
            # string. the least significant bit of the address is defined by the
            # first input port registered. the RAM output is updated as soon as
            # the input address is modified.

class ram(Device):

    genericName = 'ram'

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
        table += randbit((2**size-words)*width)
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

    def addInput(self, port, subset = None):
        # instantiate input port
        newport = inPort(port, f"D{len(self.inports)}", subset)
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
        # get alignment
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
        # build address string
        s = ""
        for p in self.inports:
            s += p.get()
        # convert string to integer
        a = int(s[::-1], 2)
        # update output value
        self.Q.set(table[a*width:(a+1)*width])
        # done
        return

# instantiate system
S = system("version 0.00")

# instantiate a clock
cl = S.add(clock(name = 'Clock'))

# instantiate reset from counter
rs = S.add(clock(100, 35, 65, count = 1, name = 'Reset'))

# instantiate counter
cn = S.add(counter(name = 'Counter'))
cn.addTrigger(cl.Q)
cn.addClear(rs.Q)

# instantiate ram
nd = S.add(ram('111011', 2)) 
nd.addAddress(cn.Q, [0, 1])

# show all devices defined
S.displayDevices()

# open export file
S.openFile()

# run simulator 
S.runUntil(500) # 150ns

# close export file
S.closeFile()

