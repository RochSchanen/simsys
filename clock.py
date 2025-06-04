# file: clock.py
# content: clock
# created: 2021 March 14 Sunday
# modified: 2025 May 31 Saturday
# modification: update to match the core.py update
# author: Roch Schanen

'''
    the clock device has one single output and no input. the output
    value depends only on the time elapse since the start of the
    simulation. 

    the clock behaviour is defined by the following parameters: 
    - the "period" in ns is the inverse of the frequency)
    - the phase "shift" in ns is the delay before the clock rise
    - the "width" in ns is the pulse length before the clock fall
    - the "count" value defines the total number of pulses to
    generate.

    a zero shift means that the rising edge of the pulse starts at
    the beginning of the period. the width value plus the shift value
    should not exceed a full period. Also, a 'None' value for the
    'count' parameter means that the number of pulses in unlimited.
    the clock signal is defined at 0 ns and has its level set on
    creation before the start of the simulation.
'''

from toolbox import *
from core import logic_device

######################################################################
###                                                              CLOCK
######################################################################

class clock(logic_device):

    def __init__(
            self,
            period = 20,    # clock period: 20 ns, 50 MHz
            shift  = 10,    # phase shift : 10 ns, half period
            width  = 10,    # pulse width : 10 ns, symmetrical
            count  = None,  # number of pulses: None is unlimited
            name   = None,  # device name : None is use generic
            ):
        # call parent class constructor
        logic_device.__init__(self, name)
        # record configuration
        self.configuration = period, width, shift, count
        # instantiate output ports
        self.Q = self.add_output_port(1, "Q")
        # compute clock phase
        phase = (0 - shift) % period
        # set output ports value
        self.Q.set(['0','1'][phase < width])
        # done
        return

    def update(self, timeStamp):
        # get configuration
        period, width, shift, count = self.configuration
        # compute phase
        phase = (timeStamp - shift) % period
        # unlimited pulse train
        if count == None:
            # update outputs values
            self.Q.set(['0','1'][phase < width])
            return
        # pulse train completed
        if count*period > timeStamp:
            # update outputs values
            self.Q.set(['0','1'][phase < width])
            return
        # done
        return

    def display(self):
        # get name
        name = self.name
        # get configuration
        period, width, shift, count = self.configuration
        # get current values
        value = f"Q={self.Q.get()}"
        # display
        print(f"<clock> {name}")
        print(f"  period: {period}")
        print(f"  width : {width}")
        print(f"  shift : {shift}")
        print(f"  count : {count}")
        print(f"  value : {value}")
        return

######################################################################
#                                                                 TEST
######################################################################

if __name__ == "__main__":

    from core import logic_system

    ls = logic_system()
    ls.add(clock(name = 'clock'))
    ls.display()
    ls.open("./export.vcd")
    ls.run_until(200)
    ls.close()
