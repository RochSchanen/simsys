# file: counter.py
# content: counter
# created: 2021 March 14 Sunday
# modified: 2025 May 31 Saturday
# modification: update to match the core.py update 
# author: Roch Schanen

'''
    the counter device has a least one input and one set of outputs that
    codes for a binary value. the number of output bits is defined by the
    parameter "size". the output value is incremented by one on each
    rising edge of the input which is labelled as 'clk'. a counter of n bits
    is counting from 0 to 2^n-1. the counter value is coerced to values
    modulo 2^n. the coercion is applied by clearing all the bits with weight
    larger than 2^n-1.

    optional inputs can be added to further control the counter. the counter
    can be cleared at any time by using the asynchronous port labelled "clr". 

    the output ports of the counter are in a well-defined state at the
    start of the simulation but they code for an arbitrary random value.

    by standard in this project, the output bits are indexed in the same
    order than the characters in the state string. This means that the bit
    weights are in the reverse order. For a numerical conversion, you can use
    int(STRING[::-1], 2) and for a string conversion, use f'{NUMBER:0{size}b}'.
'''

from core import logic_device

from numpy.random import randint

######################################################################
###                                                              TOOLS
######################################################################
# tools need to be moved to a tool.py module for re-use.

# random bits generator
def random_bits(width = 1):
    n, s = 0, ""
    while n < width:
        s += f'{randint(256):0{8}b}'
        n += 8
    return s[0:width]

######################################################################
###                                                              CLOCK
######################################################################

class counter(logic_device):

    clr = None
    clk = None

    def __init__(self, width = 4, name = None):
        # call Device class constructor
        logic_device.__init__(self, name)
        # record configuration
        self.configuration = width
        # instantiate output port
        self.Q = self.add_output_port(width, "Q")
        # set output ports value
        self.Q.set(random_bits(width))
        # done
        return

    def add_clk(self, port, subset = None):
        self.clk = self.add_input_port(port, "clk", subset)
        # done
        return

    def add_clr(self, port, subset = None):
        self.clr = self.add_input_port(port, "clr", subset)
        # done
        return

    def display(self):
        # get name
        name = self.name
        # get configuration
        size = self.configuration
        # get current values
        value = f'Q={self.Q.get()[::-1]}'
        # display
        print(f"<counter> {name}")
        if self.clk:
            print(f"  trigger {self.clk.get()}", end="")
            if self.clk.rising:
                print(", rising", end="")
            print()
        if self.clr:
            print(f"  clear {self.clr.get()}")
        print(f"  size {size}")
        print(f"  value {value}")
        return

    def update(self, timeStamp):
        # get configuration
        size = self.configuration
        # asynchronous clear on active low
        if self.clr:
            if self.clr.state == '0':
                # clear output
                self.Q.set(f'{0:0{size}b}')
                return
        # update on rising edge of trigger
        if self.clk:
            if self.clk.rising:
                # get incremented state
                n = int(self.Q.get()[::-1], 2) + 1 
                # make n string, cut-off to keep LSB(size) only
                newvalue = f'{n:0{size}b}'[-size:]
                # update output value
                self.Q.set(newvalue[::-1])
                return
        # done
        return

# EXAMPLE ############################################################

if __name__ == "__main__":

    from core import logic_system
    from clock import clock

    # build system
    ls = logic_system()
    # create devices
    clk  = ls.add(clock(name = 'clk'))
    rst  = ls.add(clock(40, 35, 5, 1, name = 'rst'))
    cnt0 = ls.add(counter(name = 'cnt0'))
    cnt1 = ls.add(counter(name = 'cnt1'))
    # create i/o links
    cnt0.add_clk(clk.Q)
    cnt1.add_clk(clk.Q)
    cnt1.add_clr(rst.Q)
    # check setup
    ls.display()
    # simulate
    ls.open("./export.vcd")
    ls.run_until(200)
    ls.close()
