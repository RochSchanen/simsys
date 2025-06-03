# file: rom.py
# content: ROM
# created: 2021 March 15 Monday
# modified: 2025 June 01 Sunday
# modification: update to match the core.py update
# author: Roch Schanen

''' 
    the ROM device has one set of inputs ports, the address, and one set
    of output ports, the data.

    the ROM data are defined by a character string of '0' and '1'.
    the data bits are indexed in the same order than the characters:
    bit 0 is the first character in the string.

    the string is split into groups which size is given by the 'width'
    parameter. This corresponds to the number of output bits.

    for an inputs address of size n. the table must contain 2^n values.
    That is a table of total binary length 2^n*width.

    in the case the binary table length does not match the required
    length, the rest of the table is automatically extended with 'U'
    values. This allows for some flexibility during project development.

    the address zero always points to the left most character of the
    table string.

    the least significant bit of the address is defined by the first input
    port that is instantiated. The most significant bit of the address is
    defined by the last input port that is instantiated.

    the ROM output is updated as soon as the input address is updated.

    simple two inputs gates or more complex look-up tables can be easily
    created using the ROM device.

    if the table string is replaced with a valid file path, the data
    contained in the file will be used as the table. see the 'rom.txt'
    file for example.
'''

from toolbox import *
from core import logic_device

from numpy import log as ln
from math import ceil

######################################################################
###                                                            SYMBOLS
######################################################################
# move symbols to the tools.py module

EOL, SPC, NUL, TAB = f"\n", f" ", f"", f"\t"

######################################################################
###                                                                ROM
######################################################################
# the default used is the NAND table with two bit inputs
# another more relevant default table could be used instead.

class rom(logic_device):

    def __init__(self,
            table  = '1110', # the table is always stored as a binary string
            width  =      1, # the table is subdivided in words of size 'width'
            expand =    '0', # use '0', '1', 'U' for un-intialised, 'R' for random
            name   =   None,
            ):
        # call parent class constructor
        logic_device.__init__(self, name)
        # find number of words
        words = ceil(len(table)/width)
        # express the size in powers of 2
        size = ceil(ln(words)/ln(2))
        # compute expansion size
        n = (2**size-words)*width
        # expand the table up to 2^size                
        table += {
            '0': '0'*n,
            '1': '1'*n,
            'U': 'U'*n,
            'R': random_bits(n),
            }[expand]
        # record configuration
        self.configuration = size, width, table
        # instantiate output port
        self.Q = self.add_output_port(width, "Q")
        # set default output port value
        self.Q.set(table[0:width])
        # done
        return

    def add_address(self, port, subset = None):
        newport = self.add_input_port(port, f"A", subset)
        # done
        return

    def display(self):
        
        # get name
        name = self.name
        
        # get configuration
        size, width, table = self.configuration
        
        # get current value
        value = f"Q={self.Q.get()[::-1]}"
        
        # display
        print(f"<read only memory> {name}")
        print(f"  size {2**size}x{width}")
        print(f"  value {value}")
        s =   f"  table "
        
        # alignment
        align = len(s)
        
        # scan through table
        for i in range(2**size):
        
            # build up display string
            s += f"{table[i*width:(i+1)*width][::-1]}{SPC}"
        
            # limit lines up to 40 characters
            if len(s) > 80:
                print(f"{s}")
                s = SPC*align
        
        # print remaining data
        if len(s) > align:
            print(f"{s}")
        
        # build address string from input ports
        s = ""
        for p in self.inputs:
            s += p.get()
        
        # detect size mismatch error
        if not size == len(s):
            print(f"  Size mismatch.")
            print(f"    {size} input(s) expected.")
            print(f"    {len(s)} input(s) found.")
            print(f"  Exiting...")
            exit()
        return

    def update(self, timeStamp):

        # get configuration
        size, width, table = self.configuration

        # build address string from input ports
        s = ""
        for p in self.inputs:
            s += p.get()

        # convert string to integer
        a = int(s[::-1], 2)

        # update output value
        self.Q.set(table[a*width:(a+1)*width])

        # done
        return

######################################################################
#                                                              EXAMPLE
######################################################################

if __name__ == "__main__":

    from core import logic_system
    from counter import counter
    from clock import clock

    # build system
    ls = logic_system()
    
    # create clocks
    clk = ls.add(clock(name = "clock"))
    rst = ls.add(clock(20, 15, 5, 1, name = "reset"))

    # create two bits counter (0-3)
    cnt = ls.add(counter(3, name = "counter"))
    cnt.add_clk(clk.Q)
    cnt.add_clr(rst.Q)

    # add gate ROM
    gate = ls.add(rom(
            table = "000001010011100",
            width = 3,
            name = 'gate',
            ))
    gate.add_address(cnt.Q)

    # add ROM from file
    # mem = ls.add(rom('./rom.txt', 8, 'memory'))
    # mem.add_address(cnt.Q)    

    # check setup
    ls.display()

    # simulate
    ls.open("./export.vcd")
    ls.run_until(150)
    ls.close()
 