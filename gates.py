# file: gates.py
# content: implementation of standard gates
# created: 2025 June 4 Wednesday
# author: Roch Schanen

from toolbox import *
from core import logic_device

######################################################################
###                                                               GATE
######################################################################

class gate(logic_device):

    def __init__(self, bits = 1, name = None):
        # call parent class constructor
        logic_device.__init__(self, name)
        # create output of width 'bits'
        self.Q = self.add_output_port(bits, "Q")
        # done
        return

    def add_input(self, port, subset = None):
        i = self.add_input_port(port, "A", subset)
        # display width mismatch warning
        ni, no = i.size(), self.Q.size() 
        if not ni == no:
            print(f"  width mismatch warning:")
            print(f"    {no} bit(s) expected from output width,")
            print(f"    {ni} bit(s) found for input {i.name}.")
        # update table
        self.make_table()
        # done
        return

    def make_table(self):
        pass

    def update(self, timeStamp):
        # collect input states
        S = [i.get() for i in self.inputs]
        # update output
        self.Q.set(lut(self.table, *S))
        # done
        return

    def make_table(self):
        # compute table length
        n = 1 << len(self.inputs)
        # build AND table
        self.table = 'U'*n
        # done
        return

    # def make_table(self):
    #     # compute table length
    #     n = 1 << len(self.inputs)
    #     # build AND table
    #     self.table = f'{1:0{n}b}'
    #     # done
    #     return

######################################################################
#                                                                 TEST
######################################################################

if __name__ == "__main__":

    from core import logic_system
    from counter import counter
    from clock import clock

    ls = logic_system()
    clk = ls.add(clock(name = "clock"))
    rst = ls.add(clock(20, 15, 5, 1, name = "reset"))
    cnt = ls.add(counter(2, name = "counter"))
    cnt.add_clk(clk.Q)
    cnt.add_clr(rst.Q)
    gte = ls.add(gate(name = 'gate'))
    gte.add_input(cnt.Q, [0])
    gte.add_input(cnt.Q, [1])
    ls.display()
    ls.open("./export.vcd")
    ls.run_until(150)
    ls.close()
