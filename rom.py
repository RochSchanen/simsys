#!/usr/bin/python3
# file: rom.py
# content: rom device
# created: 20201 March 15 Monday
# modified:
# modification: 2021 March 20 Saturday
# author: roch schanen
# comment:

# import core classes
from core import Device, inPort, outPort

# used to determine the minimum number
# of bits to code for a given integer value 
from numpy import log as ln
from math import ceil

''' ROM ##############################################################

the rom device has one set of inputs ports which codes for the address
to access and one set of output ports which is the output data. the
rom data is defined by a binary string starting from bit 0. the string
is split into groups which size is given by the 'width'  parameter,
which is also the number of output bits. for an n inputs address,
a 2^n values table must be defined. That is a binary table of length
equal to 2^n * width. if the table length does not match the required
size, the rest of the table will be extended with 'U' bits values. the
address zero points to the left most character of the string. the
least significant bit of the address is defined by the first input
port instanciated. The most significant bit of the address is defined
by the last input port instanciated. the rom output is updated as soon
as the input address is updated. simple two inputs gates or more
complex look-up tables can be easely created using the rom device.
if the table string is replaced with a valid file path, the data
contained in the file will be used as the table. see the 'rom.txt'
file for an example.

'''

class rom(Device):

    genericName = 'rom'

    # check if table is only composed of proper 'signal' characters
    def tableCheck(self, table):
        n = 0
        for c in table:
            if c in '01U':
                    n += 1
        return n == len(table)

    def tableImport(self, filename):
        # read file and collect data
        rom, b, n = '', None, 0
        fh = open(filename,'r')
        l = fh.readline()
        while l:
            # strip current line
            s = l.rstrip('\r\n')
            # load next line
            l = fh.readline()
            # update line number
            n += 1
            # skip empty line     
            if not s: continue
            # strip heading spaces
            s = s.lstrip(' ')
            # skip commented line
            if s[0] == '#': continue
            # select numeric representation (before data)
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

    def __init__(
            self,
            table = '1110', # NAND table, two bit address expected
            width = 1,      # data bus width, one bit output
            name  = None):  # device name: None, use generic
        # check if table is a path to the table data
        if not self.tableCheck(table):
            # if table is a path, import table
            table = self.tableImport(table)
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

    def ilk_a(self, port, subset = None):
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
        print(f"  size {2**size}x{width}")
        print(f"  value {value}")
        s =   f"  table "
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

# GET ROM DATA FROM FILE #############################################


if __name__ == "__main__":

    from sys import version as pythonVersion

    print("file: clock.py")
    print("content: rom device")
    print("created: 2021 March 15 Monday")
    print("author: Roch Schanen")
    print("comment:")
    print("run python3:" + pythonVersion)

    from core import system
    from clock import clock
    from counter import counter

    # build system
    S = system("version 0.00")
    
    # create devices
    clk0 = S.add(clock())
    clk1 = S.add(clock(10, 5, 5, 1))
    cnt0 = S.add(counter(2))
    rom0 = S.add(rom('00110011', 2))

    # create links
    cnt0.ilk_clk(clk0.Q)
    cnt0.ilk_clr(clk1.Q)
    rom0.ilk_a(cnt0.Q)

    # check setup
    S.displayDevices()

    # simulate
    S.openFile()
    S.runUntil(200)
    S.closeFile()
