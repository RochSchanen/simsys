# file: toolbox.py
# content: tools
# created: 2025 June 02 Monday
# author: Roch Schanen

from toolbox import *
from numpy.random import randint

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

def startup_bits(bits = 1, behaviour = 'U'):
    return {
        'U': 'U'*bits,
        'R': random_bits(bits),
        '0': '0'*bits,
        '1': '1'*bits,
        }[behaviour]

######################################################################
###                                                         LOAD_TABLE
######################################################################

def load_table(fp):
    # initialise
    table, base, bits, line_number = NUL, 16, 8, 0
    # open file
    fh = open(f'{fp}.rom','r')
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

        # parse representation
        if line[0] == '%':
            if line[1:].strip() == 'BIN' : base = 2; continue
            if line[1:].strip() == 'DEC' : base = 10; continue
            if line[1:].strip() == 'HEX' : base = 16; continue
            print(f'unknown representation "{line[1:].strip()}", at line {line_number}.')
            exit()
        # default representation is hexadecimal
        if base is None: base = 16
        
        # append table to the table in binary format
        # words are separated by spaces
        for word in line.split():
            # only the 'bits' least significant bit are kept
            # the bits exceeding the word 'bits' are ignored
            table += f'{int(word, base):0{bits}b}'[::-1][:bits]
    # done
    return bits, table
