# file: core.py
# content: core
# created: 2025 Mai 28 Wednesday
# author: roch schanen

######################################################################
###                                                            SYMBOLS
######################################################################

EOL, SPC, NUL, TAB = f"\n", f" ", f"", f"\t"

######################################################################
###                                                               PORT
######################################################################

class logic_port():

    # signal counter for making signal names
    sn = 0

    # constructor
    def __init__(self,
            n = None,  # name
            w = None,  # width
            p = None,  # port
            s = None,  # subset
            ):
        # make signal name
        self.sg = f"W{self.sn}"
        # increment signal counter
        logic_port.sn += 1
        # record port name
        self.n = n
        # declare port state
        self.ps = None
        # set port state
        if w: self.set('U'*w)
        # get target port size
        n = p.size() if p else None
        # build port subset list
        if p: self.s = list(range(n)) if s is None else s
        # record target
        self.lp = p
        # inititialise state
        if p: self.update()
        # done
        return

    def size(self):
        return len(self.ps)

    def set(self, ns):
        self.utd = (self.ps == ns)
        self.ps = ns
        return

    def get(self, ss = None):
        if ss is None: return self.ps
        return NUL.join([self.ps[i] for i in ss])

    def update(self):
        # get output port state
        ns = self.lp.get(self.ss)
        # insert wire delay here
        # ...
        # single bit case
        if len(ns) == 1:
            self.rising  = (self.ps, ns) == ('0','1')
            self.falling = (self.ps, ns) == ('1','0')
        # update input port state
        self.set(ns)
        # done
        return

    def export(self):
        # un-named
        if self.n is None: return NUL
        # check 'up-to-date' flag
        if self.utd: return NUL
        # set 'up-to-date' flag
        self.utd = True
        # make multiple bits case
        if self.size() > 1:
            return f"b{self.ps[::-1]} {self.sg}{SPC}"
        # make single bit case
        return f"{self.ps}{self.sg}{SPC}"

######################################################################
###                                                             DEVICE
######################################################################

class logic_device():

    # constructor
    def __init__(self, n = None):
        # declare device contents
        self.i = [] # inputs
        self.o = [] # outputs
        self.d = [] # sub-devices
        # record name
        self.n = n
        # call user start
        self.start()
        # done
        return

    def export(self):
        # un-named
        if self.n is None: return NUL
        # build export string
        expstr = NUL
        # go through all device contents
        for i in self.i: expstr += i.export()
        for d in self.d: expstr += d.export()
        for o in self.o: expstr += o.export()
        # done
        return expstr

    def update_input_ports(self):
        # update inputs ports first
        for i in self.i: i.update()
        # update sub devices
        for d in self.d: d.update_input_ports()
        # done
        return

    def update_output_ports(self, timeStamp):
        # update sub-devices first
        for d in self.d:
            self.d.update_outputs(timeStamp)
        # update 'linked' output ports
        for o in self.o:
            if o.lp is None: continue
            o.update()
        # update 'un-linked' output ports
        self.update(timeStamp)
        # done
        return

    def name_duplicate(self, L, name):
        # bypass no name
        if name is None: return NUL
        # build name list
        N = [l.n for l in L]
        nc, ns = 0, f"{name}"
        while ns in N:
            ns = f"{name}{nc}"
            nc += 1
        return ns

    def add_input_port(self, lport, name = None):
        n = self.name_duplicate(self.i, name)
        i = logic_port(n, lp = lport)
        self.i.append(i)
        return i

    def add_output_port(self, width, name = None, lport = None):
        n = self.name_duplicate(self.o, name)
        o = logic_port(n, w = width, p = lport)
        self.o.append(o)
        return o

    def add_device(self, d):
        d.n = self.name_duplicate(self.d, d.n)
        self.d.append(d)
        return d

    ### device specific ###

    # build up device internal structure
    # during sub class instantiation.
    def start(self):
        pass        

    # display device structure and state
    # whenever.
    def display(self):
        pass

    # device output ports updates:
    # from this inputs, sub-devices outputs, timestamp,
    # or any other internal parameters.
    def update(self, timeStamp):
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

    def add_signal(self, device, port, t = 0):
        # setup alignment
        align = TAB*t
        # skip un-named port
        if port.n is None: return NUL
        # make label
        l = f"{device.n}_{port.n}"
        # get signal identifier and size
        s, n = port.sg, port.size()
        # multiple bits
        if n > 1: l += f"[{n-1}:0]"
        # declare signal
        self.fh.write(f"{align}$var wire {n} {s} {l} $end{EOL}")
        # done
        return

    def add_module(self, d, t = 0):
        # setup alignment
        align = TAB*t
        # skip un-named port
        if d.n is None: return NUL
        # open scope
        self.fh.write(f"{align}$scope module {d.n} $end{EOL}")
        # make signals
        # for i in d.i: self.add_signal(d, i, t+1)
        for o in d.o: self.add_signal(d, o, t+1)
        # add sub-modules here
        # ...
        # close scope
        self.fh.write(f"{align}$upscope $end{EOL}")
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
        for d in self.d: self.add_module(d, 1)
        self.fh.write(f"$upscope $end{EOL}")
        self.fh.write(f"$enddefinitions $end{EOL}")
        # done
        return

    def close(self):
        self.export()
        self.fh.close()
        # done
        return

    def export(self):
        # recursively build the export string
        expstr = NUL
        for d in self.d:
            expstr += d.export()
        # skip empty string
        if expstr is NUL: return
        # export to file
        self.fh.write(f"#{self.time:04}")
        self.fh.write(f"{SPC}{expstr}{EOL}")
        # done
        return

    def run_step(self):
        self.export()
        self.time += 1
        for d in self.d: d.update_output_ports(self.time)
        for d in self.d: d.update_input_ports()        
        # done
        return

    def run_until(self, time):
        while self.time < time: self.run_step()
        # done
        return

    def display(self):
        for d in self.d: d.display()
        # done
        return

######################################################################
#                                                              EXAMPLE
######################################################################

if __name__ == "__main__":

    from clock import clock

    # instantiate logic system
    ls = logic_system()

    # add a clock to the logic system
    ls.add_device(clock(name = "clk"))

    # display system contents
    ls.display()

    # create output file
    ls.open("./export.vcd")

    # run simulation over 100ns
    ls.run_until(100)

    # close file
    ls.close()

    # done
