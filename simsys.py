#!/usr/bin/python3
# file: simsys.py
# content: system simulator
# created: 2020 july 19 Sunday
# modified:
# modification:
# author: roch schanen
# comment: system architecture simulator

# todo: make signals
# todo: make bus
# todo: make engine
# todo: make processor
# todo: make memory
# todo: make devices
# todo: make time, records, etc... 
# todo: break point, step-by-step, state display

# collect every device in the system
# run system engine and record data

from time import strftime 
from sys import exit

class system():

    def __init__(self, name):
        date = strftime("%A, %d %b %Y at %H:%M:%S")
        print(f"create system {name}\n{date}")
        self.devicelist = {}
        self.name = name
        self.date = date
        self.time = 0
        # done
        return

    # time units are in ns (float) 
    def addClock( 
        self,
        period = 20,    # 20ns, 50MHz
        width  = 10,     # symetrical clock
        phase  = 0,     # 0ns, in phase
        name   = None): # None, generic name

        # get generic clock name
        if not name:
            # find a new name
            n, k = 0, "clk0"
            while k in self.devicelist.keys():
                n += 1
                k = f"clk{n}"
            # found name
            name = k

        # create
        self.devicelist[name] = \
            clock(period, width, phase, name)

        # done
        return

    def displayDevices(self):
        for d in self.devicelist.values(): d.display()            
        return

    def openFile(self, pathName = "./output.vcd"):
        # create file
        fh = open(pathName, 'w')
        # make header
        fh.write(f"$version Generated by simsys.py $end\n")
        fh.write(f"$date {self.date} $end\n")
        # fh.write(f"$timezero 0 $end\n")
        fh.write(f"$timescale 1ns $end\n")
        # make modules and signals
        n = 0
        fh.write(f"$scope module SYSTEM $end\n")
        for d in self.devicelist.values():
            n = d.makeModule(fh, n, 0)
        fh.write(f"$upscope $end\n")
        # close header
        fh.write(f"$enddefinitions $end\n")
        # set initial values at time zero
        fh.write(f"#0\n")
        for d in self.devicelist.values():
            fh.write(d.getState())
        # done
        self.pathName = pathName
        self.fh = fh
        return

    def closeFile(self):
        self.fh.close()
        return

    def updateDevices(self):
        # increase time interval in units of 1ns
        self.time += 1
        # check for a signal change
        change = ""        
        for d in self.devicelist.values():
            change += d.updateState(self.time)
        # export if any change occured
        if change:
            self.fh.write(f"#{self.time}\n")
            self.fh.write(change)
        return

    def runUntil(self, time):
        while self.time < time:
            self.updateDevices()
        return

class port():

    def __init__(self, bits = 1):
        self.value = 'U'*bits
        return

    def get(self):
        return self.value

    def set(self, value):
        if not isinstance(value, str):
            print("port.set: value must be of string type.")
            exit()
        if not len(value) == len(self.value):
            print("port.set: value size mismatch:")
            print(f"  value size is {len(value)}.")
            print(f"  expected size is {len(self.value)}.")
            print(f"  exiting...")
            exit()
        self.value = value
        return

    def size(self):
        return len(self.value)

class clock():

    def __init__(
        self,
        period, # clock period (float time)
        width,  # pulse width  (float time)
        phase,  # phase shift  (float time)
        name):  # clock name
        # record
        self.name = name
        self.configuration = period, width, phase
        self.port = port(1)
        # done
        return

    def makeModule(self, fh, n, t):
        # get data
        name = self.name
        tab  = '\t'*(t+1)
        # write module
        fh.write(f"{tab}$scope module {name} $end\n")
        fh.write(f"{tab}\t$var wire 1 W{n} {name}_CLK $end\n")
        fh.write(f"{tab}$upscope $end\n")
        # record signal reference (VCD)
        self.signal = f"W{n}"
        return n+1

    def getState(self):
        return f"{self.port.get()}{self.signal}\n"

    def display(self):
        # get data
        name = self.name
        period, width, phase = self.configuration
        value = self.port.get()
        # display
        print(f"CLK: {name},{period},{width},{phase},{value}")
        return

    def updateState(self, timeStamp):
        # get configuration
        period, width, phase = self.configuration
        # get new state
        m = (timeStamp-phase) % period
        s = ['0','1'][m < width]
        # continue
        if self.port.get() == s: return ""
        # update
        self.port.set(s)        
        # done
        return self.getState()

if __name__ == "__main__":

    import sys

    print("file: simsys.py")
    print("content: system simulator")
    print("created: 2020 july 19 Sunday")
    print("author: roch schanen")
    print("comment: system architecture simulator")
    print("run Python3:" + sys.version);

    s = system("version 0.00")
    s.addClock()
    s.addClock(phase = 2)
    s.addClock(phase = 4)
    s.displayDevices()
    s.openFile()
    s.runUntil(100)
    s.closeFile()
