#!/usr/bin/python3
# file: counter.py
# content: counter device
# created: 2021 March 14 Sunday
# modified:
# modification:
# author: Roch Schanen
# comment:

# import core classes
from core import Device, inPort, outPort

# random generator
from numpy.random import randint

# random bits
def randbits(size = 1):
    n, s = 0, ""
    while n < size:
        s += f'{randint(256):0{8}b}'
        n += 8
    return s[0:size]

''' COUNTER ##########################################################

the clock device has a least one input and one set of outputs that
codes for a binary value. the number of output bits is define by the
parameter "size". the output value is incremented by one on each
rising edge of the input which serves as a clock. a counter of n bits
is counting from 0 to 2^n-1. the counter value is coerced to values
modulo 2^n. the coercion is applied by clearing bits with a weight
larger than 2^n-1.

additionally, optional inputs can be added to further control the
counter. for example, the counter can be cleared at any time by using
asynchronous "clr" port. 

the output ports of the counter have a well-defined state at the start
of the simulation but they code for an arbitrary random value.

by standard in this project, all the bits are indexed in the same
order than the characters in the string. This means that the bit
weigths are in the reverse order. For a numerical conversion, we use
int(STRING[::-1], 2) and for a string conversion, we use
f'{NUMBER:0{size}b}'.

'''

class counter(Device):

    genericName = 'cnt'

    clr = None
    clk = None

    def __init__(
            self,
            size = 4,     # counter width: 4bits, 0 to 15
            name = None): # device name  : None, use generic

        # call Device class constructor
        Device.__init__(self, name)
        # record configuration
        self.configuration = size
        # instantiate output port
        self.Q = outPort(size, "Q")
        # register port
        self.outports.append(self.Q)
        # set output ports value
        self.Q.set(randbits(size))
        # done
        return

    def ilk_clk(self, port):
        # instantiate input port
        self.clk = inPort(port, "clk")
        # register port
        self.inports.append(self.clk)
        return

    def ilk_clr(self, port):
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
        if self.clk:
            print(f"  trigger {self.clk.get()}", end="")
            if self.clk.rising:
                print(", rising", end="")
            print()
        if self.clr:
            print(f"  clear {self.clr.get()}")
        print(f"  size {size}")
        print(f"  value {value}")
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
        if self.clk:
            if self.clk.rising:
                # get incremented state
                n = int(self.Q.get()[::-1], 2) + 1 
                # make n string, LSB(size) only
                newvalue = f'{n:0{size}b}'[-size:]
                # update output value
                self.Q.set(newvalue[::-1])
                return
        # done
        return

if __name__ == "__main__":

    from sys import version as pythonVersion

    print("file: clock.py")
    print("content: clock device")
    print("created: 2021 March 14 Sunday")
    print("author: Roch Schanen")
    print("comment: clock device")
    print("run python3:" + pythonVersion)

    from core import system
    from clock import clock

    # build system
    S = system("version 0.00")
    
    # create devices
    clk = S.add(clock())
    rst = S.add(clock(30, 25, 5, 1))
    cnt1 = S.add(counter())
    cnt2 = S.add(counter())

    # create links
    cnt1.ilk_clk(clk.Q)
    cnt2.ilk_clk(clk.Q)
    cnt2.ilk_clr(rst.Q)

    # check setup
    S.displayDevices()

    # simulate
    S.openFile()
    S.runUntil(200)
    S.closeFile()
