# file: gate.py
# content: implementation of standard gates
# created: 2025 June 4 Wednesday
# author: Roch Schanen

from toolbox import *
from core import logic_device

# to do: add table to configuration?

######################################################################
###                                                              GATES
######################################################################
# all gates require at least one input port. inputs with multiple bits
# are allowed and behave like bus operations. this is equivalent to the
# action of a set of parallel gates on each bits of the inputs.

class _gate(logic_device):

    gn = "generic_name"

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

    # this is gate specific
    def make_table(self, n):
        pass

    def update(self, timeStamp):
        # collect input states
        S = [i.get() for i in self.inputs]
        # update output
        self.Q.set(lut(self.table, *S))
        # done
        return

    def display(self, tab):
        # get name
        name = self.name
        # get configuration
        bits = self.configuration
        # get current values
        value = f'Q={self.Q.get()[::-1]}'
        # display
        print(f"<{self.gn}> {name}")
        print(f"  bits {bits}")
        print(f"  table {self.table}")
        print(f"  value {value}")
        # done
        return

######################################### AND
# for only one input, this is equivalent to a 'COPY' bits
# (this is not recommanded since it is not standard)

class gate_and(_gate):

    gn = "gate_AND"

    def make_table(self, n):
        self.table = LOW*(n-1) + HGH*1
        return

######################################### NAND (not AND)
# for only one input, this is equivalent to an 'INVERSE' bits
# (this is not recommanded since it is not standard)

class gate_nand(_gate):

    gn = "gate_NAND"

    def make_table(self, n):
        self.table = HGH*(n-1) + LOW*1
        return

######################################### OR
# for only one input, this is equivalent to a 'COPY' bits
# (this is not recommanded since it is not standard)

class gate_or(_gate):

    gn = "gate_OR"

    def make_table(self, n):
        self.table = LOW*1 + HGH*(n-1)
        return

######################################### NOR (not OR)
# for only one input, this is equivalent to an 'INVERSE' bits
# (this is not recommanded since it is not standard)

class gate_nor(_gate):

    gn = "gate_NOR"

    def make_table(self, n):
        self.table = HGH*1 + LOW*(n-1)
        return

######################################### EQU (equal)
# for only one input, this is equivalent to a set of constant 'HIGH' bits.
# for more than two inputs, this is equivalent to a 'ALL BITS EQUAL'.
# (none of this is recommanded since it is not standard)

class gate_equ(_gate):

    gn = "gate_EQU"

    def make_table(self, n):
        self.table = HGH*1 + LOW*(n-2) + HGH*1
        return

######################################### EOR (exclusive OR)
# for only one input, this is equivalent to a set of constant 'LOW' bits.
# for more than two inputs, this is equivalent to a 'NOT ALL BITS EQUAL'.
# (none of this is recommanded since it is not standard)

class gate_eor(_gate):

    gn = "gate_EOR"

    def make_table(self, n):
        self.table = LOW*1 + HGH*(n-2) + LOW*1
        return

######################################################################
###                                                           GATE_NOT
######################################################################
# for multiple inputs with multiple bits, all the inputs bits are concatenated
# as a single set of parallel bits to be inverted: the number of input bits
# should obviously match the number of output bits.

class gate_not(_gate):

    def __init__(self, bits = 1, name = None):
        # call parent class constructor
        logic_device.__init__(self, name)
        # create output of width 'bits'
        self.Q = self.add_output_port(bits, "Q")
        # save configuration
        self.configuration = bits
        # done
        return

    def start(self):
        self.table = HGH*1 + LOW*1
        # done
        return

    def add_input(self, port, subset = None):
        i = self.add_input_port(port, "A", subset)
        # done
        return

    def update(self, timeStamp):
        # collect input states and concatenate all
        S = NUL.join([i.get() for i in self.inputs])
        # update output
        self.Q.set(lut(self.table, S))
        # done
        return

    def display(self, tab):
        # get name
        name = self.name
        # get configuration
        bits = self.configuration
        # collect input states, concatenate and get input length
        S = NUL.join([i.get() for i in self.inputs])
        ni, no = len(S), self.Q.size()
        if not ni == no:
            print(f"  width mismatch warning:")
            print(f"    {no} bit(s) expected,")
            print(f"    {ni} bit(s) found.")
        # get current values
        value = f'Q={self.Q.get()[::-1]}'
        # display
        print(f"<gate_NOT> {name}")
        print(f"  bits {bits}")
        print(f"  table {self.table}")
        print(f"  value {value}")
        # done
        return

######################################################################
#                                                                 TEST
######################################################################

if __name__ == "__main__":

    TESTS = [
        # 'AND', 
        # 'NAND',
        # 'OR'  ,
        # 'NOR' ,
        # 'EQU' ,
        # 'EOR' ,
        'NOT' ,
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
            g1.add_input(cnt.Q, [0]) # use bit 0 of counter output port Q
            g1.add_input(cnt.Q, [1]) # use bit 1 of counter output port Q
        
        if 'NAND' in TESTS:
            g2 = ls.add(gate_nand(name = 'NAND'))
            g2.add_input(cnt.Q, [0]) # use bit 0 of counter output port Q
            g2.add_input(cnt.Q, [1]) # use bit 1 of counter output port Q
        
        if 'OR' in TESTS:
            g3 = ls.add(gate_or(name = 'OR'))
            g3.add_input(cnt.Q, [0]) # use bit 0 of counter output port Q
            g3.add_input(cnt.Q, [1]) # use bit 1 of counter output port Q
        
        if 'NOR' in TESTS:
            g4 = ls.add(gate_nor(name = 'NOR'))
            g4.add_input(cnt.Q, [0]) # use bit 0 of counter output port Q
            g4.add_input(cnt.Q, [1]) # use bit 1 of counter output port Q
        
        if 'EQU' in TESTS:
            g5 = ls.add(gate_equ(name = 'EQU'))
            g5.add_input(cnt.Q, [0]) # use bit 0 of counter output port Q
            g5.add_input(cnt.Q, [1]) # use bit 1 of counter output port Q

        if 'EOR' in TESTS:
            g6 = ls.add(gate_eor(name = 'EOR'))
            g6.add_input(cnt.Q, [0]) # use bit 0 of counter output port Q
            g6.add_input(cnt.Q, [1]) # use bit 1 of counter output port Q
        
        if 'NOT' in TESTS:
            g7 = ls.add(gate_not(bits = 2, name = 'NOT'))
            g7.add_input(cnt.Q)
            
            g8 = ls.add(gate_not(bits = 2, name = 'NOT1'))
            g8.add_input(cnt.Q, [0])
            g8.add_input(cnt.Q, [1])

        ls.display()
        ls.open("./export.vcd")
        ls.run_until(1000)
        ls.close()
