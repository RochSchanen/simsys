# file: toolbox.py
# content: tools
# created: 2025 June 02 Monday
# author: Roch Schanen

from numpy.random import randint

######################################################################
###                                                            SYMBOLS
######################################################################

# general strings
EOL, SPC, NUL, TAB = f'\n', f' ', f'', f'\t'

# bit representation
LOW, HGH, UKN = f'0', f'1', f'U'

# load table parsing symbols (local symbols)
_COM, _SEP = f'#', f'='

######################################################################
###                                                     NAME_DUPLICATE
######################################################################

def name_duplicate(objects, name):
    # bypass when no name
    if name is None: return None
    # build the list of names
    names = [o.name for o in objects]
    # initialise (start counting from one)
    counter, newname = 1, f"{name}"
    # loop until no duplicate
    while newname in names:
        newname = f"{name}{counter}"
        counter += 1
    # done
    return newname

######################################################################
###                                                        RANDOM_BITS
######################################################################

def random_bits(bits = 1, block = 8):
    # initialise
    n, table = 0, NUL
    # build enough random bits
    while n < bits:
        table += f'{randint(1<<block):0{block}b}'
        n += block
    # cut-off excess and return
    return table[:bits]

######################################################################
###                                                       STARTUP_BITS
######################################################################
# allow for a string of behav char to individualise start up behaviour

def startup_bits(bits = 1, behav = 'U'):
    return {
        '0': LOW*bits,
        '1': HGH*bits,
        'U': UKN*bits,
        'R': random_bits(bits),
        }[behav]

######################################################################
###                                                         LOAD_TABLE
######################################################################

def load_table(fp):
    # initialise
    table, base, bits, line_number = NUL, 16, 8, 0
    # open file
    fh = open(fp,'r')
    # read file line by line
    new_line = fh.readline()
    while new_line:
        # strip 'end-of-line' characters
        line = new_line.rstrip('\r\n')
        # load next line already
        new_line = fh.readline()
        # update line number
        line_number += 1
        # skip empty lines     
        if line is NUL: continue
        # strip heading spaces
        line = line.lstrip(SPC)
        # skip comment lines
        if line[0] == _COM: continue
        # parse BITS
        if line[:4] == 'BITS':
            (key, value) = line.split(_SEP)
            bits = int(value.strip())
            continue
        # parse BASE
        if line[:4] == 'BASE':
            (key, value) = line.split(_SEP)
            base = {
                'HEX': 16,
                'DEC': 10,
                'BIN':  2,
                }[value.strip()]
            continue
        # append data to the table in binary form
        # words separators is expected to be spaces
        for word in line.split():
            # only the least significant bit are kept
            # the most significant bits exceeding the
            # value of 'bits' are simply ignored
            # the bits are stored in reversed order
            table += f'{int(word, base):0{bits}b}'[::-1][:bits]
    # done
    return table, bits

######################################################################
#                                                                  LUT
######################################################################
# inputs are ordered with the least significant bit first

def lut(table, *inputs):
    A = [NUL.join(I) for I in zip(*(inputs[::-1]))]
    return NUL.join([UKN if UKN in a else table[int(a, 2)] for a in A])

######################################################################
#                                                                 TEST
######################################################################

if __name__ == "__main__":

    TESTS = [
        # 'name_duplicate',
        # 'random_bits',
        # 'startup_bits',
        # 'load_table',
        # 'lut',
        ]

    if 'lut' in TESTS:

        print("two single bit inputs")
        print(lut("ABCD", "U", "0"))
        print(lut("ABCD", "1", "U"))
        print(lut("ABCD", "0", "1"))
        print(lut("ABCD", "1", "1"))
        print("three single bit inputs")
        print(lut("ABCDEFGH", "U", "0", "0"))
        print(lut("ABCDEFGH", "1", "U", "0"))
        print(lut("ABCDEFGH", "0", "1", "U"))
        print(lut("ABCDEFGH", "1", "1", "0"))
        print(lut("ABCDEFGH", "0", "0", "1"))
        print(lut("ABCDEFGH", "1", "0", "1"))
        print(lut("ABCDEFGH", "0", "1", "1"))
        print(lut("ABCDEFGH", "1", "1", "1"))
        print("two quadruple bits inputs")
        print(lut("ABCD", "U000", "0000"))
        print(lut("ABCD", "1111", "0U00"))
        print(lut("ABCD", "0000", "11U1"))
        print(lut("ABCD", "1111", "111U"))
        print("three quadruple bits inputs")
        print(lut("ABCDEFGH", "U000", "0000", "0000"))
        print(lut("ABCDEFGH", "1111", "0U00", "0000"))
        print(lut("ABCDEFGH", "0000", "1111", "00U0"))
        print(lut("ABCDEFGH", "1111", "1111", "000U"))
        print(lut("ABCDEFGH", "0000", "0000", "1111"))
        print(lut("ABCDEFGH", "1111", "0000", "1111"))
        print(lut("ABCDEFGH", "1111", "1111", "1111"))
        print(lut("ABCDEFGH", "0000", "1111", "1111"))

    if 'load_table' in TESTS:

        from core import logic_system
        from counter import counter
        from clock import clock
        from rom import rom

        ls = logic_system()
        clk = ls.add(clock(name = "clock"))
        rst = ls.add(clock(20, 15, 5, 1, name = "reset"))
        cnt = ls.add(counter(2, name = "counter"))
        cnt.add_clk(clk.Q)
        cnt.add_clr(rst.Q)
        gate1 = ls.add(rom(*load_table(f'and.rom'), name = 'AND'))
        gate1.add_address(cnt.Q)
        gate2 = ls.add(rom(*load_table(f'eor.rom'), name = 'EOR'))
        gate2.add_address(cnt.Q)
        ls.display()
        ls.open("./export.vcd")
        ls.run_until(150)
        ls.close()

    if 'startup_bits' in TESTS:

        print(startup_bits(16, '0'))
        print(startup_bits(16, '1'))
        print(startup_bits(16, 'U'))
        print(startup_bits(16, 'R'))
        print(startup_bits(16, 'I'))

    if 'random_bits' in TESTS:

        print(random_bits(16))
        print(random_bits(16))
        print(random_bits(16))
        print(random_bits(16))
        print(random_bits(16))

    if 'name_duplicate' in TESTS:

        # define a test class with the name property 
        class objectclass():
            def setname(self, name):
                self.name = name

        # declare a empty list of objects
        O = []
        # instantiate 8 objects with same generic name 'A'
        for i in range(8):
            # create new object
            o = objectclass()
            # use name_duplicate() to build a new name
            n = name_duplicate(O, "A")
            # set object name using the new name
            o.setname(n)
            # append new object to list
            O.append(o)
        # print the name for each object
        print([o.name for o in O])
