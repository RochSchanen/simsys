# file: toolbox.py
# content: tools
# created: 2025 June 02 Monday
# author: Roch Schanen

from numpy.random import randint

######################################################################
###                                                            SYMBOLS
######################################################################

EOL, SPC, NUL, TAB = f'\n', f' ', f'', f'\t'

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

def random_bits(bits = 1, blocklength = 8):
    # initialise
    n, table = 0, NUL
    # build enough random bits
    while n < bits:
        table += f'{randint(1<<blocklength):0{blocklength}b}'
        n += blocklength
    # cut-off excess and return
    return table[0:bits]

######################################################################
###                                                       STARTUP_BITS
######################################################################

def startup_bits(bits = 1, behav = 'U'):
    return {
        'U': 'U'*bits,
        'R': random_bits(bits),
        '0': '0'*bits,
        '1': '1'*bits,
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
        if line[0] == '#': continue
        # parse BITS
        if line[:4] == 'BITS':
            (key, value) = line.split('=')
            bits = int(value.strip())
            continue
        # parse BASE
        if line[:4] == 'BASE':
            (key, value) = line.split('=')
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
            table += f'{int(word, base):0{bits}b}'[::-1][:bits]
    # done
    return table, bits

######################################################################
#                                                                 TEST
######################################################################

if __name__ == "__main__":

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
