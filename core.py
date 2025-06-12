# file: core.py
# content: core
# created: 2025 May 28 Wednesday
# author: Roch Schanen

from toolbox import *

######################################################################
###                                                               PORT
######################################################################

class logic_port():

    # signal counter for making signal names
    signal_counter = 0

    # constructor
    def __init__(self, parent, name = None, bits = None, port = None, subset = None, behav = 'U'):
        # record parent
        self.parent = parent
        # make signal name
        self.signal = f"W{self.signal_counter}"
        # increment signal counter
        logic_port.signal_counter += 1
        # record port name
        self.name = name
        # declare port state
        self.state = None
        # set port state
        if bits: self.set(startup_bits(bits, behav))
        # get target port size
        n = port.size() if port else None
        # make port subset
        if port:
            self.subset = subset
            if self.subset is None:
                self.subset = list(range(n))
        # record target
        self.port = port
        # initialise state
        if port: self.update()
        # done
        return

    def size(self):
        return len(self.state)

    def set(self, new_state):
        self.up_to_date = (self.state == new_state)
        self.state = new_state
        return

    def get(self, subset = None):
        if subset is None: return self.state
        return NUL.join([self.state[index] for index in subset])

    def update(self):
        # get output port state
        new_state = self.port.get(self.subset)
        # code for wire delay here
        # ...
        # single bit case
        if len(new_state) == 1:
            self.rising  = (self.state, new_state) == (LOW, HGH)
            self.falling = (self.state, new_state) == (HGH, LOW)
        # update input port state
        self.set(new_state)
        # done
        return

    def export(self):
        # unnamed
        if self.name is None: return NUL
        # check 'up-to-date' flag
        if self.up_to_date: return NUL
        # set 'up-to-date' flag
        self.up_to_date = True
        # make multiple bits case
        if self.size() > 1:
            return f"b{self.state[::-1]} {self.signal}{SPC}"
        # make single bit case
        return f"{self.state}{self.signal}{SPC}"

######################################################################
###                                                             DEVICE
######################################################################

class logic_device():

    # constructor
    def __init__(self, name = None):
        # declare device contents
        self.inputs  = [] # input ports
        self.outputs = [] # output ports
        self.devices = [] # devices
        # record name
        self.name = name
        # call user start
        self.start()
        # done
        return

    # device specific
    def start(self):
        pass        

    def add_input_port(self, port, name = None, subset = None):
        name = name_duplicate(self.inputs, name)
        new_port = logic_port(self, name, None, port, subset)
        self.inputs.append(new_port)
        return new_port

    def add_output_port(self, bits, name = None, port = None, subset = None, behav = 'U'):
        name = name_duplicate(self.outputs, name)
        new_port = logic_port(self, name, bits, port, subset, behav)
        self.outputs.append(new_port)
        return new_port

    def add(self, device):
        device.name = name_duplicate(self.devices, device.name)
        self.devices.append(device)
        return device

    def update_output_ports(self, timeStamp):
        # update sub-devices first
        for d in self.devices:
            self.devices.update_outputs(timeStamp)
        # update 'linked' output ports
        for o in self.outputs:
            if o.port is None: continue
            o.update()
        # update 'unlinked' output ports
        self.update(timeStamp)
        # done
        return

    # device specific
    def update(self, timeStamp):
        pass

    def update_input_ports(self):
        # update inputs ports first
        for i in self.inputs: i.update()
        # update sub-devices
        for d in self.devices: d.update_input_ports()
        # done
        return

    def export(self):
        # unnamed
        if self.name is None: return NUL
        # build export string
        export_string = NUL
        # go through all device contents
        for i in self.inputs:  export_string += i.export()
        for d in self.devices: export_string += d.export()
        for o in self.outputs: export_string += o.export()
        # done
        return export_string

    # device specific
    def display(self):
        pass

######################################################################
###                                                             SYSTEM
######################################################################

class logic_system(logic_device):

    def start(self):
        # setup date and time
        from time import strftime
        self.date = strftime("%A, %d %b %Y at %H:%M:%S")
        self.time = 0 # [ns]
        # done
        return

    def open(self, fp):
        fh = open(fp, 'w')       
        # register file handle
        self.fh = fh
        # write header
        self.fh.write(f"$version 'SimSys 0.0' $end{EOL}")
        self.fh.write(f"$date {self.date} $end{EOL}")
        self.fh.write(f"$timescale 1ns $end{EOL}")
        self.fh.write(f"$scope module SYSTEM $end{EOL}")
        for d in self.devices: self.add_module(d, 1)
        self.fh.write(f"$upscope $end{EOL}")
        self.fh.write(f"$enddefinitions $end{EOL}")
        # done
        return

    def add_module(self, device, t = 0):
        # setup alignment
        align = TAB*t
        # skip unnamed port
        if device.name is None: return NUL
        # open scope
        self.fh.write(f"{align}$scope module {device.name} $end{EOL}")
        # make signals
        for o in device.outputs: self.add_signal(device, o, t+1)
        for i in device.inputs:  self.add_signal(device, i, t+1)
        # add sub-modules
        for d in device.devices: self.add_module(d, t+1)
        # close scope
        self.fh.write(f"{align}$upscope $end{EOL}")
        # done
        return

    def add_signal(self, device, port, t = 0):
        # setup alignment
        align = TAB*t
        # skip unnamed port
        if port.name is None: return NUL
        # make label
        label = f"{device.name}_{port.name}"
        # get signal identifier and size
        signal, bits = port.signal, port.size()
        # check for multiple bits
        if bits > 1: label += f"[{bits-1}:0]"
        # add signal
        self.fh.write(f"{align}$var wire {bits} {signal} {label} $end{EOL}")
        # done
        return

    def run_until(self, time):
        while self.time < time: self.run_step()
        # done
        return

    def run_step(self):
        self.export()
        self.time += 1
        for d in self.devices: d.update_output_ports(self.time)
        for d in self.devices: d.update_input_ports()        
        # done
        return

    def export(self):
        # recursively build the export string
        export_string = NUL
        # make export string from all device
        for d in self.devices:
            export_string += d.export()
        # skip if empty string
        if export_string is NUL: return
        # export string to file
        self.fh.write(f"#{self.time:04}")
        self.fh.write(f"{SPC}{export_string}{EOL}")
        # done
        return

    def close(self):
        self.export()
        self.fh.close()
        # done
        return

    def display(self):
        for d in self.devices: d.display()
        # done
        return

######################################################################
#                                                    FIXED VALUE PORTS
######################################################################

# VCC = logic_port('VCC', 1, None, None, HGH)
# GND = logic_port('GND', 1, None, None, LOW)

######################################################################
#                                                                 TEST
######################################################################

if __name__ == "__main__":

    from clock import clock

    ls = logic_system()
    ls.add(clock(name = "clk"))
    ls.display()
    ls.open(f"./export.vcd")
    ls.run_until(100)
    ls.close()
