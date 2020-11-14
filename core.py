#!/usr/bin/python3
# file: core.py
# content: system simulator core
# created: 2020 november 14 Saturday
# modified:
# modification:
# author: roch schanen
# comment: core classes

# todo: when declaring bus, create
# individual ports as well... Think!
# todo: make signals
# todo: make bus
# todo: make engine
# todo: make processor
# todo: make memory
# todo: make devices
# todo: make time, records, etc... 
# todo: break point, step-by-step, state display
# todo: add validity check of device setup  
# collect every device in the system run system engine and record data

from time import strftime 
from sys import exit

# FOR COMPATIBILLTY ISSUES

SEP = " "    # SIGNAL SEPARATOR
EOL = "\n"   # END-OF-LINE CODE

# SIGNAL COUNTER
# the signal counter is used for the VCD file wire names. they are all
# given the format 'Wn' where 'W' is the letter W and 'n' is an index
# number. The value of n is given by the
# counter 'N'.

N = 0

# SYSTEM / MODULE #########################################

class system():

    # (generic)
    def __init__(self, name):
        date = strftime("%A, %d %b %Y at %H:%M:%S")
        print(f"create system {name}\n{date}")
        self.devicelist = {}
        self.name = name
        self.date = date
        self.time = 0
        # done
        return

    # (generic)
    # getName returns a device name in the form 'Sn' where the string
    # S is a given generic name and 'n' is an index number. The index
    # is incremented with every new call. This provides an trivial way
    # to create unique device names.
    def getName(self, generic):
        n, k = 0, f"{generic}0"
        while k in self.devicelist.keys():
            n += 1
            k = f"{generic}{n}"
        # found name
        return k

    # (generic)
    def displayDevices(self):
        for d in self.devicelist.values(): d.display()            
        return

    # (generic)
    # create a new VCD file and make the file header. 
    def openFile(self, pathName = "./output.vcd"):
        # create file
        fh = open(pathName, 'w')
        # make header
        fh.write(f"$version Generated by simsys.py $end{EOL}")
        fh.write(f"$date {self.date} $end{EOL}")
        fh.write(f"$timescale 1ns $end{EOL}")
        # make modules and signals
        fh.write(f"$scope module SYSTEM $end{EOL}")
        for d in self.devicelist.values(): d.makeModule(fh, 0)
        fh.write(f"$upscope $end{EOL}")
        # close header
        fh.write(f"$enddefinitions $end{EOL}")
        # done
        self.pathName = pathName
        self.fh = fh
        return

    # (generic)
    def closeFile(self):
        self.fh.close()
        return

    # (generic)
    # this generate a new step in the simulation. the step resolution
    # is 1ns at the moment. it should be made possible to vary this
    # value. 
    def runStep(self):
        # export new state
        exportResult = ""
        for device in self.devicelist.values():
            exportResult += device.export()
        # export
        if exportResult:
            self.fh.write(f"#{self.time}")
            self.fh.write(f"{SEP}{exportResult}{EOL}")
        # increase time by one interval (1ns)
        self.time += 1
        # update device outputs
        for device in self.devicelist.values():
            device.updateOutputPorts(self.time)
        # update device inputs
        for device in self.devicelist.values():
            device.updateInputPorts()        
        # done
        return

    # (generic)
    # repeat steps until end time is reached
    def runUntil(self, time):
        while self.time < time:
            self.runStep()
        return

    # (generic)
    def add(self, device):
        # get device given name
        name = device.name
        # check for duplicate
        if name in self.devicelist.keys():
            print(f"system.create({name}): duplicated name.")
            print(f"  name {name} already used.")
            print(f"  exiting...")
            exit()
        # make generic name
        if name == None:
            name = self.getName(device.genericName)
            # record new name
            device.name = name
        # register new device
        self.devicelist[name] = device
        # done
        return self.devicelist[name]

class portCommon():

    def addSignal(self):
        global N
        self.signal = f"W{N}"
        N += 1
        return self.signal

    def get(self):
        return self.state

    def size(self):
        return len(self.state)

    # export to VCD format
    def export(self):
        if self.signal:
            # no change
            if self.uptodate: return ""
            # set flag
            self.uptodate = True
            # bit string export
            if self.size() > 1:
                return f"b{self.state} {self.signal}{SEP}"
            # single bit export
            return f"{self.state}{self.signal}{SEP}"
        # no signal
        return ""

# OUTPUT PORTS ############################################
# 'set' asserts the value of the port. The method detects if
# the asserted value has changed the value of the port and sets
# the 'uptodate' flag. no change <=> 'uptodate' is true.

class outPort(portCommon):

    def __init__(self, bits = 1, name = None):
        # initialise to undefined value 'U'
        self.state = 'U'*bits
        # register port name
        self.name = name
        # force update at origin
        self.uptodate = False
        # export signal
        self.signal = None
        return

    def set(self, newvalue):
        # check type is string 
        if not isinstance(newvalue, str):
            print(f"port.set: value must be of string type.")
            print(f"  exiting...")
            exit()
        # check size
        if not len(newvalue) == self.size():
            print(f"port.set: value size mismatch:")
            print(f"  value size is {len(value)}.")
            print(f"  expected size is {self.size()}.")
            print(f"  exiting...")
            exit()
        # set flag
        self.uptodate = (self.state == newvalue)
        # update value
        self.state = newvalue
        # done
        return

# INPUT PORTS #############################################

class inPort(portCommon):
# an input port is always linked to an output port.
# !!! create two port constant: vcc and gnd.
# 'update' sets the new value of the input port from
# its linked output port value. It sets the 'uptodate' flag.
# it also detects the 'rising' and 'falling' edge events.

    def __init__(self, port, name = None):
        # linking (adding to the network)
        self.p = port
        # register port name
        self.name = name
        # initial state
        self.state = port.get()
        # force update at origin
        self.uptodate = False
        # export signal
        self.signal = None
        # clear edge events        
        self.rising  = False
        self.falling = False
        return

    def update(self):
        newvalue = self.p.get()
        # update flag
        self.uptodate = (self.state == newvalue)
        # update value
        if self.p.size() > 1:
            self.state = newvalue
            return
        # single bit case        
        self.rising  = False
        self.falling = False
        # detect rising edge
        if (self.state, newvalue) == ('0','1'):
            self.rising = True                 
        # detect falling edge
        if (self.state, newvalue) == ('1','0'):
            self.falling = True
        # update state
        self.state = newvalue                 
        return

# DEVICE #################################################
# the 'Device' class is a template class.
# 'writeVar' helps to format the header of the VCD file.
# 'makeModule' write this device header for the VCD file. 

class Device():

    genericName = "dev"

    def __init__(self, name):
        self.name = name
        self.inports  = []
        self.outports = []
        self.exports  = []
        return

    def writeVar(self,
            f,  # file
            t,  # tab level
            p): # port
        # write port signal
        if p.name:
            # register port in export list
            self.exports.append(p)
            # get size
            size = p.size()
            # get signal name
            label = f"{self.name}_{p.name}"
            if size > 1:
                label += f"[{size-1}:0]"
            # get signal identifier
            signal = p.addSignal()
            f.write(f"{t}\t$var")    # header
            f.write(f" wire {size}") # signal size
            f.write(f" {signal}")    # signal identifier
            f.write(f" {label}")     # signal name
            f.write(f" $end{EOL}")   # tail
        return

    def makeModule(self,
            f,  # file
            t): # tab level
        # get module name
        name = self.name
        # tab alignment
        tab  = '\t'*(t+1)
        # write header
        f.write(f"{tab}$scope module {name} $end{EOL}")
        # write variables (inputs)
        for p in self.inports:
            self.writeVar(f, tab, p)
        # write variables (outputs)
        for p in self.outports:
            self.writeVar(f, tab, p)
        # write tail
        f.write(f"{tab}$upscope $end{EOL}")
        # done
        return

    def updateInputPorts(self):
        for p in self.inports: p.update()
        return

    def export(self):
        exportResult = ""
        for p in self.exports:
            exportResult += p.export()
        return exportResult

    def display(self):
        pass

# EXAMPLE #################################################

if __name__ == "__main__":

    from sys import version as pythonVersion

    print("file: core.py")
    print("content: system simulator core")
    print("created: 2020 july 19 Sunday")
    print("author: roch schanen")
    print("comment: core classes")
    print("run Python3:" + pythonVersion)

    # instantiate simulator
    S = system("version 0.00")    

    # show all devices defined
    S.displayDevices()

    # open export file
    S.openFile()    
    # run simulator    
    S.runUntil(500)
    # close export file
    S.closeFile()
