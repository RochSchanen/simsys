# file: multiplexer.py
# content: multiplexer
# created: 2025 june 9 Monday
# author: Roch Schanen

'''
    the number of output bits is defined by the parameter "bits".

    part of the the input port value is copied to the output port.
    
    the part that is copied depends on the value of the selector value.

    the output is updated as soon as any input is modified.

'''

from toolbox import *
from core import logic_device

######################################################################
###                                                        MULTIPLEXER
######################################################################

class multiplexer(logic_device):

    def __init__(self, bits = 1, name = None, behav = 'U'):
        # call Device class constructor
        logic_device.__init__(self, name)
        # record configuration
        self.configuration = bits
        # instantiate output port
        self.Q = self.add_output_port(bits, "Q", None, None, behav)
        # declare multiplexer data and selector input lists
        self.A, self.S = [], []
        # done
        return

    def add_A(self, port, subset = None):
        self.A.append(self.add_input_port(port, "A", subset))
        # done
        return

    def add_S(self, port, subset = None):
        self.S.append(self.add_input_port(port, "S", subset))
        # done
        return

    def update(self, timeStamp):
        # get configuration
        bits = self.configuration
        # concatenate address inputs
        S = NUL.join([s.get() for s in self.S])
        # check for uninitialized bit(s)
        if UKN in S:
            # set uninitialised output
            self.Q.set(UKN*bits)
            # done
            return
        # compute address pointer
        p = int(S[::-1], 2)*bits
        # buid data inputs table
        A = NUL.join([a.get() for a in self.A])
        # copy selected data to multiplexer output
        self.Q.set(A[p:p+bits])
        # done
        return

    def display(self):
        # get name
        name = self.name
        # get configuration
        bits = self.configuration
        # get current values
        input_address = NUL.join([s.get() for s in self.S])
        input_table = NUL.join([a.get() for a in self.A])
        output_state = self.Q.get()[::-1]
        address_length = len(input_address)
        # display
        print(f"<multiplexer> {name}")

        print(f"  bits {bits}")
        print(f"  input {None}")
        print(f"  output {None}")

        # done
        return

######################################################################
#                                                                 TEST
######################################################################

if __name__ == "__main__":

    from core    import logic_system
    from clock   import clock
    from counter import counter

    ls = logic_system()
    # add clocks
    rst  = ls.add(clock(20, 15, 5, 1, name = 'reset'))
    clk  = ls.add(clock(name = 'clock'))
    # multiplexer with 5 inputs gives 2^5 combination to test
    cnt = ls.add(counter(5, name = 'counter'))
    cnt.add_clk(clk.Q)
    cnt.add_clr(rst.Q)
    # multiplexer with 4 bits input, one bit select, 2 bits output
    mpx = ls.add(multiplexer(2, name = "multiplexer"))
    mpx.add_A(cnt.Q, [1, 2])
    mpx.add_A(cnt.Q, [3, 4])
    mpx.add_S(cnt.Q, [0])
    # run test
    ls.display()
    ls.open("./export.vcd")
    ls.run_until(700)
    ls.close()
