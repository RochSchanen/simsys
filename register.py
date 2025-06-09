# file: register.py
# content: register
# created: 2025 june 9 Monday
# author: Roch Schanen

'''
    the register device has one or more inputs which concatenation must match
    the and the output width. the number of output bits is defined by the
    parameter "bits". the input value is copied to ouput value on each rising
    edge of the input clock labelled 'clk'.

    an optional inputs can be added to further control the register. the
    register can be cleared at any time by using the asynchronous clear signal
    labelled "clr".

    by convention in this project, the output bits are indexed in the same order
    than the characters in the state string. This means that the bit weights are
    in the reverse order. For a numerical conversion, you should use the following
    expression: int(STRING[::-1], 2) and for a integer value to string conversion,
    you should use the expression f'{NUMBER:0{bits}b}'.
'''

from toolbox import *
from core import logic_device

######################################################################
###                                                           REGISTER
######################################################################

class register(logic_device):

    clr = None
    clk = None

    def __init__(self, bits = 8, name = None, behav = 'U'):
        # call Device class constructor
        logic_device.__init__(self, name)
        # record configuration
        self.configuration = bits
        # instantiate output port
        self.Q = self.add_output_port(bits, "Q", None, None, behav)
        # declare register input list
        self.A = []
        # done
        return

    def add_input(self, port, subset = None):
        self.A.append(self.add_input_port(port, "A", subset))
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
                # done
                return
        # update on rising edge of clock
        if self.clk:
            if self.clk.rising:
                # concatenate input states
                S = NUL.join([a.get() for a in self.A])
                # copy input to ouput
                self.Q.set(S)
                # done
                return
        # done
        return

    def display(self):
        # get name
        name = self.name
        # get configuration
        bits = self.configuration
        # get current values
        input_value = f'Q={NUL.join([a.get() for a in self.A])[::-1]}'
        output_state = f'Q={self.Q.get()[::-1]}'
        # display
        print(f"<register> {name}")
        if self.clk:
            print(f"  clock {self.clk.get()}", end="")
            if self.clk.rising:
                print(", rising", end="")
            print()
        if self.clr:
            print(f"  clear {self.clr.get()}")
        print(f"  bits {bits}")
        print(f"  input {input_value}")
        print(f"  output {output_state}")
        return

######################################################################
#                                                                 TEST
######################################################################

if __name__ == "__main__":

    from core     import logic_system
    from clock    import clock
    from counter  import counter
    from register import register
    from gates    import gate_not

    ls = logic_system()
    clk  = ls.add(clock(name = 'clock'))
    rst  = ls.add(clock(40, 35, 5, 1, name = 'reset'))
    cnt = ls.add(counter(4, name = 'counter'))
    cnt.add_clk(clk.Q)
    cnt.add_clr(rst.Q)
    ntclk = ls.add(gate_not(name = "not_clock"))
    ntclk.add_input(clk.Q)
    reg = ls.add(register(4, name = "register"))
    reg.add_input(cnt.Q)
    reg.add_clk(ntclk.Q)
    reg.add_clr(rst.Q)
    ls.display()
    ls.open("./export.vcd")
    ls.run_until(500)
    ls.close()
