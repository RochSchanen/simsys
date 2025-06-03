# file: toolbox.py
# content: tools
# created: 2025 June 02 Monday
# author: Roch Schanen

from numpy.random import randint

######################################################################
###                                                            SYMBOLS
######################################################################

EOL, SPC, NUL, TAB = f"\n", f" ", f"", f"\t"

######################################################################
###                                                     NAME_DUPLICATE
######################################################################

def name_duplicate(object_list, name):
    # bypass no name
    if name is None: return NUL
    # build name list
    name_list = [obj.name for obj in object_list]
    name_counter, name_string = 0, f"{name}"
    while name_string in name_list:
        name_string = f"{name}{name_counter}"
        name_counter += 1
    return name_string

######################################################################
###                                                        RANDOM_BITS
######################################################################

def random_bits(width = 1):
    n, s = 0, ""
    while n < width:
        s += f'{randint(256):0{8}b}'
        n += 8
    return s[0:width]

######################################################################
###                                                         LOAD_TABLE
######################################################################

def load_table(fp):
    # initialise
    data, base, line_number = NUL, None, 0
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
        
        # append data to the table in binary format
        # words are separated by spaces
        for word in line.split():
            # only the 'width' least significant bit are kept
            # the bits exceeding the word 'width' are ignored
            data += f'{int(word, base):0{width}b}'[::-1][:width]
    # done
    return width, data
