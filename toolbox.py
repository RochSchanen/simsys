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

