# file: rom.py
# content: ROM
# created: 2021 March 15 Monday
# modified: 2025 June 01 Sunday
# modification: update to match the core.py update
# author: Roch Schanen

''' 
    the ROM device has one set of inputs ports, the address,
    and one output port, the data.

    the ROM data are defined by a character string of '0' and
    '1' or other valid bit representation. the data bits are
    indexed in the same order than characters in a string:
    bit 0 is the first character in the string.

    the string is split into words which length is given by
    the 'bits' parameter. This corresponds to the number of
    output bits.

    for an inputs address of length n. the table must contain
    2^n values. That is a table of total length bits*2^n.

    in case the table length does not match the required length,
    the rest of the table is automatically extended. The values
    of the addtional data depends on the parameter "filling".
    the value of the filling parameter can be '0', '1', 'U', or
    'R': the same as for startup_bits().

    the address zero always points to the left most character
    of the string that forms the table.

    the least significant bit of the address is defined by the
    first input port that is instantiated. The most significant
    bit of the address is defined by the last input port that
    is instantiated.

    the ROM output is updated as soon as the input address is
    updated.
    
    if the address contains a single 'U', the all of the output
    bits are set to 'U'.

    The startup bit values are always 'U'.

    to load a table from a file, use the load_table() function
    from the toolbox module. 
'''

from toolbox import *
from core import logic_device
from numpy import log as ln
from math import ceil

_DISPLAY_MAX = 80 # maximum characters per lines for table display

######################################################################
###                                                                ROM
######################################################################
# the default used is the NAND table with two bit inputs
# another more relevant default table could be used instead.

class rom(logic_device):

    def __init__(self,
            table   = '1110', # the table is always stored as a binary string
            bits    =     1 , # the table is subdivided in words of length 'bits'
            name    =  None , # None means no export
            filling =    'U', # filling mode for data padding
            ):
        # call parent class constructor
        logic_device.__init__(self, name)
        # find number of words
        words = ceil(len(table)/bits)
        # express the nn in powers of 2
        nn = ceil(ln(words)/ln(2))
        # compute expansion length
        n = (2**nn-words)*bits
        # expand the table up to 2^nn                
        table += startup_bits(n, filling)
        # record configuration
        self.configuration = nn, bits, table
        # instantiate output port (startup is always 'U')
        self.Q = self.add_output_port(bits, "Q", None, None, 'U')
        # done
        return

    def add_address(self, port, subset = None):
        newport = self.add_input_port(port, f"A", subset)
        # done
        return

    def update(self, timeStamp):
        # get configuration
        bits, bits, table = self.configuration
        # build address string from input ports
        address_string = NUL.join([p.get() for p in self.inputs])
        # check for un-intialised levels
        if 'U' in address_string:
            self.Q.set(UKN*bits)
            return
        # convert string to integer
        address_value = int(address_string[::-1], 2)
        # update output value
        self.Q.set(table[address_value*bits:(address_value+1)*bits])
        # done
        return

    def display(self):
        # get name
        name = self.name
        # get configuration
        nn, bits, table = self.configuration
        # get current value
        value = f"Q={self.Q.get()[::-1]}"
        # display
        print(f"<read only memory> {name}")
        print(f"  length {2**nn}x{bits}")
        print(f"  value {value}")
        s =   f"  table "
        # alignment
        align = len(s)
        # scan through table
        for i in range(2**nn):
            # build up display string
            s += f"{table[i*bits:(i+1)*bits][::-1]}{SPC}"
            # limit lines up to '_DISPLAY_MAX' characters
            if len(s) > _DISPLAY_MAX:
                print(f"{s}")
                s = SPC*align
        # print last table line, less than '_DISPLAY_MAX'
        if len(s) > align: print(f"{s}")
        # build address string from input ports
        address_string = NUL.join([p.get() for p in self.inputs])
        # detect length mismatch
        if not nn == len(address_string):
            print(f"  adress length mismatch warning:")
            print(f"    {nn} bit(s) expected,")
            print(f"    {len(address_string)} bit(s) found.")
        # done
        return

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
    mem = ls.add(rom(name = 'mem'))
    mem.add_address(cnt.Q)
    ls.display()
    ls.open("./export.vcd")
    ls.run_until(150)
    ls.close()
