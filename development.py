#!/usr/bin/python3
# file: development.py
# content: development code
# created: 2020 November 14 Saturday
# modified:
# modification:
# author: roch schanen
# comment: system architecture simulator

if __name__ == "__main__":

    from sys import version as pythonVersion

    print("file: development.py")
    print("content: system simulator development")
    print("created: 2020 November 14 Saturday")
    print("author: roch schanen")
    print("comment:")
    print("run Python3:" + pythonVersion);

    # to fix end of line OS dependence
    from os  import linesep as _EOL
    _EOLN = -len(_EOL) 

    # to compute the rom address size
    from numpy import log as ln
    from math import ceil

    # exit on error
    from sys import exit

    # read file and collect data

    rom, b, n = '', None, 0

    fh = open('rom.txt','r')

    l = fh.readline();

    while l:

        s = l[:_EOLN].strip()

        l = fh.readline()
        n += 1

        # skip empty line        
        if not s: 
            continue
        
        # skip commented line
        if s[0] == '#':
            continue
        
        if s[0] == '%':
            if s[1:].strip() == 'BINARY': b = 2; continue
            if s[1:].strip() == 'DECIMAL': b = 10; continue
            if s[1:].strip() == 'HEXADECIMAL': b = 16; continue
            print(f'unknown command, current line is {n}')
            exit()

        if not b: b = 16

        for w in s.split():
            rom += f'{int(w, b):08b}'[::-1]

    # compute size and fill up missing area
    size = ceil(ln(len(rom))/ln(2))
    rom += 'U'*(2**size-len(rom))

    # display table bits
    m = 64
    if len(rom)//m:
        for i in range(len(rom)//m):
            print(rom[i*m:(i+1)*m])
    else: print(rom)

    print(f'data table length is {len(rom)}')
    print(f'address width is {size}')
