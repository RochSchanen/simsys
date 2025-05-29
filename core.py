# file: core.py
# content: core
# created: 2025 Mai 28 Wednesday
# author: roch schanen

### SYMBOLS
EOL, SPC, NUL, TAB = "\n", " ", "", "\t"

### BLOCK
def filterBlock(fh, Block, tab):
    b = ""
    for l in Block[len(EOL):].split(EOL):
        b += TAB + l.lstrip() + EOL
    return b

### PORTS
class logic_port():

    # signal count for signal names
    sn = 0

    # constructor
    def __init__(self, n = None, bw = None, lp = None, ss = None):
        # record signal name
        self.sg = f"W{self.sn}"
        # increment global signal count
        logic_port.sn += 1
        # record port name
        self.n = n
        # declare port state
        self.ps = None
        # set port state
        if bw: self.set('U'*bw)
        # get target port size
        n = lp.size() if lp else None
        # build port subset list
        if lp: self.ss = list(range(n)) if ss is None else ss
        # record target
        self.lp = lp
        # init state
        if lp: self.update()
        # done
        return

    def size(self):
        return len(self.ps)

    def set(self, ns):
        self.utd = (self.ps == ns)
        self.ps = ns
        return

    def get(self, ss = None):
        # return full port state
        if ss is None: return self.ps
        # return subset of port state
        return "".join([self.ps[i] for i in ss])

    def update(self):
        # get output port state
        ns = self.lp.get(self.ss)
        # (to do: insert wire delay here...)
        # single bit case
        if len(ns) == 1:
            self.rising  = (self.ps, ns) == ('0','1')
            self.falling = (self.ps, ns) == ('1','0')
        # update input port state
        self.set(ns)
        # done
        return

    def export(self):
        # un-exported
        if self.n is None: return f""
        # check for update
        if self.utd: return f""
        # set flag
        self.utd = True
        # multiple bits case
        if self.size() > 1:
            return f"b{self.ps[::-1]} {self.sg}{SPC}"
        # single bit case
        return f"{self.ps}{self.sg}{SPC}"

    def declare(self, tb, pn = ""):
        if self.n is None: return f""
        label = f"{pn}_{self.n}"
        if self.size() > 1:
            label += f"[{self.size()-1}:0]"
        return f"{'\t'*tb}$var wire {port.size()} {port.sg} {label} $end{EOL}"

### DEVICES
class logic_device():

    gn = "D"

    # constructor
    def __init__(self, n = None):
        # declare device contents
        self.i = [] # inputs
        self.o = [] # outputs
        self.d = [] # sub-devices
        # record name
        self.n = n
        # sub class init
        self.start()
        #done
        return

    def export(self):
        # un-exported
        if self.n is None: return f""
        # build export string
        expstr = ""
        # go through all device contents
        for i in self.i: expstr += i.export()
        for d in self.d: expstr += d.export()
        for o in self.o: expstr += o.export()
        return expstr

    # def declare(self, tb, pn):
    #     # write header
    #     s = f"{'\t'*tb}\t$scope module {self.n} $end{EOL}"
    #     # write variables (inputs)
    #     for p in self.inports:
    #         self.writeVar(f, tab, p)
    #     # write variables (outputs)
    #     for p in self.outports:
    #         self.writeVar(f, tab, p)
    #     # write tail
    #     f.write(f"{tab}$upscope $end{EOL}")
    #     # done
    #     return

    def update_input_ports(self):
        # update inputs ports first
        for i in self.i: i.update()
        # update sub devices
        for d in self.d: d.update_input_ports()
        # done
        return

    # this is a template to be over-written
    def update_output_ports(self, timeStamp):
        # update sub-devices ouput ports first
        for d in self.d: self.d.update_outputs(timeStamp)
        # sub class update
        self.update(timeStamp)
        # done
        return

    def name_duplicate(L, name):
        # bypass no name
        if name is None: return f""
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
        o = logic_port(n, bw = width, lp = lport)
        self.o.append(o)
        return o

    def add_sub_device(self, name = None):
        n = self.name_duplicate(self.d, name)
        d = logic_device(n)
        self.d.append(d)
        return d

    ### sub class methods ###

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

### SYSTEM
class logic_system(logic_device):

    def start(self):

        # setup date 
        from time import strftime
        date = strftime("%A, %d %b %Y at %H:%M:%S")
        print(f"record date: {date}\n")

        # setup time (time units are in ns)
        print(f"reset time")
        self.time = 0
        
        print(f"open file")
        fp = "./export.vcd"

        # create new file
        fh = open(fp, 'w')       
        # start file header
        fh.write(f"$version generated by simsys.py $end{EOL}")
        fh.write(f"$date {date} $end{EOL}")
        fh.write(f"$timescale 1ns $end{EOL}")
        # make system module
        fh.write(f"$scope module SYSTEM $end{EOL}")
        # recursively build the sub devices tree and signals
        for d in self.d: self.makeModule(d)
        # end system module
        fh.write(f"$upscope $end{EOL}")
        # end file header
        fh.write(f"$enddefinitions $end{EOL}")

        # done
        return
