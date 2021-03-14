#!/usr/bin/python3
# file: example.py
# content: system simulator example
# created: 2021 March 13 Saturday
# modified:
# modification:
# author: roch schanen
# comment:

from core import system
from library import clock, counter, rom, GetRomFromFile
# instantiate a simulator system
S = system("version 0.00")
# instantiate a clock
myClock = S.add(clock(name = 'Clock'))
# instantiate a reset using a clock
myReset = S.add(clock(100, 35, 65, count = 1, name = 'Reset'))
# instantiate a counter (default is 4 bits counter)
myCounter = S.add(counter(name = 'Counter'))
myCounter.linkTrigger(myClock.Q) # link clock to counter trigger
myCounter.linkClear(myReset.Q) # link reset to counter clear
# instantiate 4x1 bits rom to make a NAND gate
myGate = S.add(rom('1110', name = 'NAND')) 
myGate.linkAddress(myCounter.Q, [0, 1]) # link to counter output Q0 and Q1
# instantiate 16x8 bits rom
myRom = S.add(rom(GetRomFromFile('rom.txt'), 8, name = 'ROM')) 
myRom.linkAddress(myCounter.Q) # link to counter output Q0, Q1, Q2, Q3
# show all devices defined
S.displayDevices()
# open export file
S.openFile()
# run simulator 
S.runUntil(500) # 150ns
# close export file
S.closeFile()
