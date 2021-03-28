#!/usr/bin/python3
# file: clock.py
# content: clock device
# created: 2021 March 14 Sunday
# modified:
# modification:
# author: Roch Schanen
# comment:

# import core classes
from core import Device, outPort

''' CLOCK ############################################################

the clock device has no input and one single output. the output value
depends only on the time from the start of the simulation 

the clock behaviour is defined by the following parameters: 
- the "period" in ns which is the inverse of the frequency)
- the phase "shift" in ns which is the delay before the clock pulse
- the "width" in ns which is the pulse length
- the "count" value which define the number of pulses.

a zero shift means that the rising edge of the pulse starts at the
beginning of the period. the width value plus the shift value should
not exceed a full period. Also, a 'None' value for the 'count'
parameter means that the number of pulses in unlimited. the clock
signal is defined at 0 ns and has its level set on creation before the
start of the simulation.

'''

class clock(Device):

    genericName = 'clk'

    def __init__(
            self,
            period = 20,    # clock period: 20 ns, 50 MHz
            shift  = 10,    # phase shift : 10 ns, half period
            width  = 10,    # pulse width : 10 ns, symmetrical
            count  = None,  # number of pulses: None is unlimited
            name   = None): # device name : None is use generic

        # call Device class constructor
        Device.__init__(self, name)
        # record configuration
        self.configuration = period, width, shift, count
        # instantiate output ports
        self.Q = outPort(1, "Q")
        # register port
        self.outports.append(self.Q)
        # compute clock phase
        phase = (0 - shift) % period
        # set output ports value
        self.Q.set(['0','1'][phase < width])
        # done
        return

    def display(self):
        # get name
        name = self.name
        # get configuration
        period, width, shift, count = self.configuration
        # get current values
        value = f"Q={self.Q.get()}"
        # display
        print(f"<clock> {name}")
        print(f"  period: {period}")
        print(f"  width : {width}")
        print(f"  shift : {shift}")
        print(f"  count : {count}")
        print(f"  value : {value}")
        return

    def updateOutputPorts(self, timeStamp):
        # get configuration
        period, width, shift, count = self.configuration
        # compute phase
        phase = (timeStamp - shift) % period
        # unlimited pulse train
        if count == None:
            # update outputs values
            self.Q.set(['0','1'][phase < width])
            return
        # pulse train completed
        if count*period > timeStamp:
            # update outputs values
            self.Q.set(['0','1'][phase < width])
            return
        # done
        return

# EXAMPLE ############################################################

if __name__ == "__main__":

    from sys import version as pythonVersion

    print("file: clock.py")
    print("content: clock device")
    print("created: 2021 March 14 Sunday")
    print("author: Roch Schanen")
    print("comment:")
    print("run python3:" + pythonVersion)

    from core import system

    # build system
    S = system("version 0.00")
    
    S.add(clock())                          # clk 0
    S.add(clock(shift = 11, count = 3))     # clk 1
    S.add(clock(shift = 9,  count = 3))     # clk 2
    S.add(clock(55, 10, 30, None))          # clk 3
    S.add(clock(55, 10, 30, 2))             # clk 4
    S.add(clock(width = 9, shift = 10, count = 3))

    # simulate
    S.displayDevices()
    S.openFile()
    S.runUntil(200)
    S.closeFile()
