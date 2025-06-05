# file: gates.py
# content: implementation of standard gates
# created: 2025 June 4 Wednesday
# author: Roch Schanen

from toolbox import *
from core import logic_device

######################################################################
###                                                              GATES
######################################################################
# all gates require at least one input
# inputs with multiple bits are allowed like for bus operations:
# this is equivalent to the action of a set of parallele gates.

class gate(logic_device):

    def __init__(self, bits = 1, name = None):
        # call parent class constructor
        logic_device.__init__(self, name)
        # create output of width 'bits'
        self.Q = self.add_output_port(bits, "Q")
        # save configuration
        self.configuration = bits
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
        # immediately update table
        self.make_table(1 << len(self.inputs))
        # done
        return

    def make_table(self, n):
        pass

    def update(self, timeStamp):
        # collect input states
        S = [i.get() for i in self.inputs]
        # update output
        self.Q.set(lut(self.table, *S))
        # done
        return

    def display(self):
        # get name
        name = self.name
        # get configuration
        bits = self.configuration
        # get current values
        value = f'Q={self.Q.get()[::-1]}'
        # display
        print(f"<gate_{self.gn}> {name}")
        print(f"  bits {bits}")
        print(f"  table {self.table}")
        print(f"  value {value}")
        # done
        return

######################################### AND
# for only one input, this is
# equivalent to a 'COPY' bits
# (this is not a recommanded usage)

class gate_and(gate):

    gn = "AND"

    def make_table(self, n):
        self.table = LOW*(n-1) + HGH*1
        return

######################################### NAND (not AND)
# for only one input, this is
# equivalent to an 'INVERSE' bits
# (this is not a recommanded usage)

class gate_nand(gate):

    gn = "NAND"

    def make_table(self, n):
        self.table = HGH*(n-1) + LOW*1
        return

######################################### OR
# for only one input, this is
# equivalent to a 'COPY' bits
# (this is not a recommanded usage)

class gate_or(gate):

    gn = "OR"

    def make_table(self, n):
        self.table = LOW*1 + HGH*(n-1)
        return

######################################### NOR (not OR)
# for only one input, this is
# equivalent to an 'INVERSE' bits
# (this is not a recommanded usage)

class gate_nor(gate):

    gn = "NOR"

    def make_table(self, n):
        self.table = HGH*1 + LOW*(n-1)
        return

######################################### EQU (equal)
# for more than two inputs, this is
# equivalent to a 'ALL BITS EQUAL'
# (this is not a recommanded usage)

class gate_equ(gate):

    gn = "EQU"

    def make_table(self, n):
        self.table = HGH*1 + LOW*(n-2) + HGH*1
        return

######################################### EOR (exclusive OR)
# for more than two inputs, this is
# equivalent to a 'NOT ALL BITS EQUAL'
# (this is not a recommanded usage)

class gate_eor(gate):

    gn = "EOR"

    def make_table(self, n):
        self.table = LOW*1 + HGH*(n-2) + LOW*1
        return

######################################### NOT
# no more than one input is allowed

class gate_not(gate):

    gn = "NOT"

    def make_table(self, n):
        self.table = HGH*1 + LOW*1
        return

######################################################################
#                                                                 TEST
######################################################################

if __name__ == "__main__":

    TESTS = [
        'AND', 
        # 'NAND',
        # 'OR'  ,
        # 'NOR' ,
        # 'EQU' ,
        # 'EOR' ,
        # 'NOT' ,
        ]

    if TESTS:

        from core import logic_system
        from counter import counter
        from clock import clock

        ls = logic_system()
        rst = ls.add(clock(10, 5, 5, 1, name = "reset"))
        clk = ls.add(clock(100, 00, 50, name = "clock"))
        cnt = ls.add(counter(2, name = "counter"))
        cnt.add_clk(clk.Q)
        cnt.add_clr(rst.Q)

        if 'AND' in TESTS:
            g1 = ls.add(gate_and(name = 'AND'))
            g1.add_input(cnt.Q, [0]) # use bit 0 of counter ouput port Q
            g1.add_input(cnt.Q, [1]) # use bit 1 of counter ouput port Q
        
        if 'NAND' in TESTS:
            g2 = ls.add(gate_nand(name = 'NAND'))
            g2.add_input(cnt.Q, [0]) # use bit 0 of counter ouput port Q
            g2.add_input(cnt.Q, [1]) # use bit 1 of counter ouput port Q
        
        if 'OR' in TESTS:
            g3 = ls.add(gate_or(name = 'OR'))
            g3.add_input(cnt.Q, [0]) # use bit 0 of counter ouput port Q
            g3.add_input(cnt.Q, [1]) # use bit 1 of counter ouput port Q
        
        if 'NOR' in TESTS:
            g4 = ls.add(gate_nor(name = 'NOR'))
            g4.add_input(cnt.Q, [0]) # use bit 0 of counter ouput port Q
            g4.add_input(cnt.Q, [1]) # use bit 1 of counter ouput port Q
        
        if 'EQU' in TESTS:
            g5 = ls.add(gate_equ(name = 'EQU'))
            g5.add_input(cnt.Q, [0]) # use bit 0 of counter ouput port Q
            g5.add_input(cnt.Q, [1]) # use bit 1 of counter ouput port Q

        if 'EOR' in TESTS:
            g6 = ls.add(gate_eor(name = 'EOR'))
            g6.add_input(cnt.Q, [0]) # use bit 0 of counter ouput port Q
            g6.add_input(cnt.Q, [1]) # use bit 1 of counter ouput port Q
        
        if 'NOT' in TESTS:
            g7 = ls.add(gate_not(bits = 2, name = 'NOT'))
            g7.add_input(cnt.Q)

        ls.display()
        ls.open("./export.vcd")
        ls.run_until(1000)
        ls.close()
