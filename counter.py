# file: counter.py
# content: counter
# created: 2021 March 14 Sunday
# modified: 2025 May 31 Saturday
# modification: update to match the core.py update 
# author: Roch Schanen

'''
    the counter device has a least one input and one set of outputs that codes
    for a binary value. the number of output bits is defined by the parameter
    "bits". the output value is incremented by one on each rising edge of the
    input which is labelled as 'clk'. a counter of n bits is counting from 0
    to 2^n-1. the counter value is coerced to values modulo 2^n. the coercion
    is applied by clearing all the bits with weight larger than 2^n-1.

    optional inputs can be added to further control the counter. the counter
    can be cleared at any time by using the asynchronous port labelled "clr". 
'''

from toolbox import *
from core import logic_device

######################################################################
###                                                              CLOCK
######################################################################

class counter(logic_device):

    clr = None
    clk = None

    def __init__(self, bits = 4, name = None, behav = 'U'):
        # call Device class constructor
        logic_device.__init__(self, name)
        # record configuration
        self.configuration = bits
        # instantiate output port
        self.Q = self.add_output_port(bits, "Q", None, None, behav)
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

    def update(self, timeStamp):
        # get configuration
        bits = self.configuration
        # asynchronous clear on active low
        if self.clr:
            if self.clr.state == LOW:
                # clear output
                self.Q.set(f'{0:0{bits}b}')
                return
        # update on rising edge of trigger
        if self.clk:
            if self.clk.rising:
                # get incremented state
                n = int(self.Q.get()[::-1], 2) + 1 
                # make n string, cut-off to keep LSB(bits) only
                newvalue = f'{n:0{bits}b}'[-bits:]
                # update output value
                self.Q.set(newvalue[::-1])
                return
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
        print(f"<counter> {name}")
        if self.clk:
            print(f"  clock {self.clk.get()}", end="")
            if self.clk.rising:
                print(", rising", end="")
            print()
        if self.clr:
            print(f"  clear {self.clr.get()}")
        print(f"  bits {bits}")
        print(f"  value {value}")
        return

######################################################################
#                                                                 TEST
######################################################################

if __name__ == "__main__":

    from core import logic_system
    from clock import clock

    ls = logic_system()
    clk  = ls.add(clock(name = 'clock'))
    rst  = ls.add(clock(40, 35, 5, 1, name = 'reset'))
    cnt = ls.add(counter(name = 'counter'))
    cnt.add_clk(clk.Q)
    cnt.add_clr(rst.Q)
    ls.display()
    ls.open("./export.vcd")
    ls.run_until(200)
    ls.close()
