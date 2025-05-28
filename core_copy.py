#!/usr/bin/python3
# file: core.py
# content: system simulator core
# created: 2020 November 14 Saturday
# modified:
# modification:
# author: roch schanen
# comment:

from sys import exit
def exitProcess():
    return exit()

# CHARACTERS SYMBOLS (system dependent?)

EOL, SPC, NUL = "\n", " ", ""   

class VCDfile():

    def __init__(self, sh, fp = "./export.vcd"):
        # create file handle if path is given
        fh = self.create(fp) if fp else None
        # record conficguration
        self.config = sh, fh, 0
        # done
        return

    def create(self, dev, fp):
        # load configuration
        sh, fh, N = self.config
        # close handle if active
        if fh: fh.close()
        # create file (new file)
        fh = open(fp, 'w')
        # make header
        fh.write(f"$version SimSys 0.0 $end{EOL}")
        fh.write(f"$date {sh.date} $end{EOL}")
        fh.write(f"$timescale 1ns $end{EOL}")
        # make modules and signals
        fh.write(f"$scope module SYSTEM $end{EOL}")
        # recursively build the list of devices in the system
        for d in sh.devicelist.values(): d.makeModule()        # !!!!!!!!!!!
        fh.write(f"$upscope $end{EOL}")
        # close header
        fh.write(f"$enddefinitions $end{EOL}")
        # done
        return fh

    def export(self):
        # load configuration
        sh, fh, N = self.config
        # recursively build the export string
        expstr = ""
        for d in sh.devicelist.values(): expstr += d.export()
        # check for empty string
        if expstr is NUL: return
        # export the string
        fh.write(f"#{sh.time:04}")
        fh.write(f"{SPC}{expstr}{EOL}")
        # done
        return

    def close(self):
        # export current state
        self.export()
        # close file
        fh.close()
        # save configuration
        self.config = sh, fh, N
        return

# SYSTEM #############################################################

# the system class collects devices, runs the engine and exports the results

class system():

    def __init__(self, name):
        # devicelist contains all the devices to simulate
        self.devicelist = {}
        # name is the system name
        # usually just the version number
        self.name = name
        # time is the current simulation time
        # it varies thoughout the simulation execution
        self.time = 0
        # date is the date-time at the start of the simulation 
        from time import strftime
        date = strftime("%A, %d %b %Y at %H:%M:%S")
        print(f"create system {name}\n{date}")
        self.date = date
        # create file
        self.file = VCDfile(self)
        # done
        return

    # to find the next index of a generic name:
    # when no name is explicitely given to a device a generic name
    # with an appended number needs to be generated. this method
    # finds a new index that has not been used yet 
    def getName(self, generic):
        n, k = 0, f"{generic}0"
        while k in self.devicelist.keys():
            n += 1
            k = f"{generic}{n}"
        # found name
        return k

    # to display the state of all the devices in the system:
    def displayDevices(self):
        print(f"System state at {self.time}ns")
        for d in self.devicelist.values(): d.display()            
        return

    # to generate one step in the simulation:
    # the step resolution is 1ns by default
    # this should be later made a parameter
    def runStep(self):
        # export state to file
        self.file.export()
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

    # to generate steps until 'time' is reached:
    # this can be used multiple times, each time with a 'time' value 
    # larger than the previous. this allows for executing extra code
    # at specific moment of the simulation 
    def runUntil(self, time):
        while self.time < time:
            self.runStep()
        return

    # to add a device to the system:
    # you should find ready designed devices in other files
    # or make your own (this is the main purpose of this project)
    def add(self, device):
        # get device given name
        name = device.name
        # check for duplicate
        if name in self.devicelist.keys():
            print(f"system.create({name}): duplicated name.")
            print(f"  name {name} already used.")
            print(f"  exiting...")
            exitProcess()
        # make generic name
        if name == None:
            name = self.getName(device.genericName)
            # record new name
            device.name = name
        # register new device
        self.devicelist[name] = device
        # done
        return self.devicelist[name]


 DEVICE #############################################################

# the 'Device' class is a template class. 'writeVar' is used to format
# the header of the VCD file. 'makeModule' write this device header
# for the VCD file. 

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

    def export(self):
        exportResult = ""
        for p in self.exports:
            exportResult += p.export()
        return exportResult

    def display(self):
        pass

    def updateInputPorts(self):
        for p in self.inports: p.update()
        return

    def updateOutputPorts(self, timeStamp):
        pass

# EXAMPLE ############################################################

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
