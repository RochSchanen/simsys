#!/usr/bin/python3
# file: library.py
# content: system simulator library
# created: 2020 november 14 Saturday
# modified:
# modification:
# author: roch schanen
# comment: device library

# import core classes
from core import Device, inPort, outPort

# CLOCK ###################################################

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
            name   = None): # clock name  : None, use generic

        # call parent class constructor
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

    # # (specific)
    # # size is the number of bits.
    # # n bits means counting between 0 and 2^n-1.
    # # default is 4 bits which gives a count between 0 and 15.
    # def createCounter( 
    #     self,
    #     size = 4,     # 4bits, count 0 to 15
    #     name = None): # None, generic name
    #     # check duplicate
    #     if name in self.devicelist.keys():
    #         print(f"system.createCounter: counter name duplicated.")
    #         print(f"  name {name} already used.")
    #         print(f"  exiting...")
    #         exit()
    #     # get generic counter name
    #     if not name: name = self.getName("cnt")
    #     # create
    #     self.devicelist[name] = \
    #         counter(size, name)
    #     # done
    #     return self.devicelist[name]

# # COUNTER #################################################

# # todo: counter options
# # clr on active low, high
# # trg on rising, falling edge
# # wrt on active low, high
# # ena on active low, high
# # cse on active low, high
# # initial value random, zero, maybe undefined
# # maybe parallel, serial load

# class counter(Device):

#     # the following ports are activated only when
#     # an input port is dynamically connected to them  
#     clr = None # clear   (reset)
#     trg = None # trigger (clock)
#     # wrt = None # write   (load) ...to implement
#     # ena = None # enable  (output) ...to implement
#     # cse = None # chip select ...to implement

#     # re-define __init__ to add parameter 'size'
#     def __init__(self,
#             size,   # counter bits width 
#             name):  # counter name
#         # call parent class constructor
#         Device.__init__(self, name)
#         # record configuration
#         self.configuration = size
#         # instantiate output port
#         self.Q = outPort(size, "Q")
#         # register port
#         self.outports.append(self.Q)
#         # set initial output port value
#         # self.Q.set('X'*size)               # undefined values
#         self.Q.set(f'{rnd(size):0{size}b}')  # random values
#         return

#     def addTrigger(self,
#             p): # port
#         # instantiate input port
#         self.trg = inPort(p, "trg")
#         # register port
#         self.inports.append(self.trg)
#         return

#     def addClear(self,
#             p): # port
#         # instantiate input port
#         self.clr = inPort(p, "clr")
#         # register port
#         self.inports.append(self.clr)
#         return

#     def display(self):
#         name = self.name
#         size = self.configuration
#         value = self.Q.get()
#         # display
#         print(f"CNT: {name},{size},{value}")
#         return

#     # here is defined the behaviour of the counter device
#     # asynchronous reset (counter is zero whenever 'clr' is low)
#     # synchronous increment on the rising edge of 'clk'
#     # the counter value is coerced modulo 'size'.
#     def updateOutputPorts(self, timeStamp):
#         # get configuration
#         size = self.configuration
#         # asynchronous clear on active low
#         if self.clr.state == '0':
#             # clear output
#             self.Q.set(f'{0:0{size}b}')
#             return
#         # update on rising edge of trigger
#         if self.trg.rising:
#             # get incremented state
#             n = int(self.Q.get(), 2) + 1
#             # make n string, LSB(size) only
#             newvalue = f'{n:0{size}b}'[-size:]
#             # new output
#             self.Q.set(newvalue)
#             return
#         # done
#         return

    # # (specific)
    # # create a reset signal.
    # # length is the period of the reset signal in ns.
    # # the reset signal occurs once at the start of the run.
    # def createReset( 
    #     self,
    #     length = 1,   # 1, one cycle
    #     name = None): # None, generic name
    #     # check duplicate
    #     if name in self.devicelist.keys():
    #         print(f"system.createReset: reset name duplicated.")
    #         print(f"  name {name} already used.")
    #         print(f"  exiting...")
    #         exit()
    #     # get generic counter name
    #     if not name: name = self.getName("rst")
    #     # create
    #     self.devicelist[name] = \
    #         reset(length, name)
    #     # done
    #     return self.devicelist[name]

# # RESET ###################################################

# class reset(Device):

#     def __init__(self,
#             length, # clear delay length
#             name):  # device name
#         # call parent class constructor
#         Device.__init__(self, name)
#         # record configuration
#         self.configuration = length
#         # instantiate output port
#         self.Q = outPort(1, "Q")
#         # register port
#         self.outports.append(self.Q)
#         # set default output ports value
#         self.Q.set('0')
#         # done
#         return

#     def display(self):
#         name = self.name
#         length = self.configuration
#         value = f"{self.Q.get()}"
#         # display
#         print(f"RST: {name},{length},{value}")
#         return

#     def updateOutputPorts(self, timeStamp):
#         # get configuration
#         length = self.configuration
#         # compute output
#         value = ['1','0'][timeStamp < length]
#         # update output
#         self.Q.set(value)
#         # done
#         return

    # # (specific)
    # # size is the number of bits.
    # # n bits means counting between 0 and 2^n-1.
    # # default is 4 bits which gives a count between 0 and 15.
    # def createLUT( 
    #     self,
    #     table = '1110', # default table is a 2 inputs NAND gate
    #     name = None): # None, generic name
    #     # check duplicate
    #     if name in self.devicelist.keys():
    #         print(f"system.createLUT: LUT name duplicated.")
    #         print(f"  name {name} already used.")
    #         print(f"  exiting...")
    #         exit()
    #     # get generic counter name
    #     if not name: name = self.getName("lut")
    #     # create
    #     self.devicelist[name] = \
    #         lut(table, name)
    #     # done
    #     return self.devicelist[name]

# # LUT #################################################
# # look up table logic: logic element of FPGAs and other
# # types of programmable logic. inputs are ordered with
# # the least significant bit being the first added. 

# class lut(Device):

#     # re-define __init__ to add parameter 'size'
#     def __init__(self,
#             table,  # lut table
#             name):  # counter name
#         # call parent class constructor
#         Device.__init__(self, name)
#         # compute size
#         size = int(ln(len(table))/ln(2))
#         # record configuration
#         self.configuration = size, table
#         # instantiate output port
#         self.Q = outPort(1, "Q")
#         # register port
#         self.outports.append(self.Q)
#         # set default output port value (random bits)
#         self.Q.set('X')
#         return

#     def addInput(self,
#             p): # port
#         # instantiate input port
#         newport = inPort(p, f"I{len(self.inports)}")
#         # register new port
#         self.inports.append(newport)
#         return

#     def display(self):
#         name = self.name
#         size, table = self.configuration
#         value = self.Q.get()
#         # display
#         print(f"LUT: {name},{size},{table},{value}")
#         if not size == len(self.inports):
#             print(f"  Size mismatch.")
#             print(f"    {size} input(s) expected.")
#             print(f"    {len(self.inports)} input(s) found.")
#             print(f"  Exiting...")
#             exit()
#         return

#     # the LUT device returns the table value pointed
#     # by the input address value. 
#     def updateOutputPorts(self, timeStamp):
#         # get configuration
#         size, table = self.configuration
#         # get table address
#         a, w = 0, 1 << (size-1)
#         for i in self.inports:
#             a += w*['0','1'].index(i.get())
#             w >>= 1
#         # set new value
#         self.Q.set(table[a])
#         # done
#         return

# # RAM #################################################
# # Random Access Memory: store words pointed by address.

# class ram(Device):

#     adr = None
#     clk = None    

#     # re-define __init__ to add parameter 'size'
#     def __init__(self,
#             length,  # number of words
#             width,   # size of the words
#             name):   # counter name
#         # call parent class constructor
#         Device.__init__(self, name)
#         # record configuration
#         self.configuration = length, size
#         # instantiate output port
#         self.Q = outPort(size, "Q")
#         # register port
#         self.outports.append(self.Q)
#         # set default output port value (random bits)
#         self.Q.set('X'*size)
#         return

#     def addInput(self,
#             p): # port
#         # instantiate input port
#         newport = inPort(p, f"I{len(self.inports)}")
#         # register new port
#         self.inports.append(newport)
#         return

#     def display(self):
#         name = self.name
#         size, table = self.configuration
#         value = self.Q.get()
#         # display
#         print(f"LUT: {name},{size},{table},{value}")
#         if not size == len(self.inports):
#             print(f"  Size mismatch.")
#             print(f"    {size} input(s) expected.")
#             print(f"    {len(self.inports)} input(s) found.")
#             print(f"  Exiting...")
#             exit()
#         return

#     # the LUT device returns the table value pointed
#     # by the input address value. 
#     def updateOutputPorts(self, timeStamp):
#         # get configuration
#         size, table = self.configuration
#         # get table address
#         a, w = 0, 1 << (size-1)
#         for i in self.inports:
#             a += w*['0','1'].index(i.get())
#             w >>= 1
#         # set new value
#         self.Q.set(table[a])
#         # done
#         return


# EXAMPLE #################################################

if __name__ == "__main__":

    from sys import version as pythonVersion

    print("file: library.py")
    print("content: system simulator library")
    print("created: 2020 november 14 Saturday")
    print("author: roch schanen")
    print("comment: device library")
    print("run Python3:" + pythonVersion)

    from core import system

    # instantiate a simulator system
    S = system("version 0.00")
    
    # instantiate a clock
    S.add(clock())

    # show all devices defined
    S.displayDevices()

    # open export file
    S.openFile()

    # run simulator 
    S.runUntil(150) # 150ns
    
    # close export file
    S.closeFile()
