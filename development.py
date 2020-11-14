#!/usr/bin/python3
# file: development.py
# content: system simulator development
# created: 2020 November 14 Saturday
# modified:
# modification:
# author: roch schanen
# comment: system architecture simulator

    # to do: when declaring bus, create
    # individual ports as well... Think!
    # to do: make bus
    # to do: make memory
    # to do: make processor
    # to do: debug tools. unconnected inputs  
    # to do: create port constants vcc and gnd

if __name__ == "__main__":

    from sys import version as pythonVersion

    print("file: development.py")
    print("content: system simulator development")
    print("created: 2020 November 14 Saturday")
    print("author: roch schanen")
    print("comment:")
    print("run Python3:" + pythonVersion);

    from core import system
    from library import clock

    # instantiate simulator
    S = system("version 0.00")
    
    # # add reset signal
    # rst = S.createReset(35) # hold reset for 35ns

    # instantiate clock
    clk0 = S.add(clock(10,5))
    clk1 = S.add(clock(20,10))
    clk2 = S.add(clock(40,20))

    # instantiate counter and make network
    # cnt = S.createCounter()
    # cnt.addTrigger(clk1.Q) # use clock output 'Q' for counter trigger
    # cnt.addClear(rst.Q) # use reset output 'Q' for counter reset

    # instantiate LUT as a 3 inputs AND gate
    #              I0 = 01010101
    #              I1 = 00110011
    #              I2 = 00001111
    # lut1 = S.createLUT('00000001')
    # lut1.addInput(clk0.Q)
    # lut1.addInput(clk1.Q)
    # lut1.addInput(clk2.Q)

    # show all devices defined
    S.displayDevices()

    # open export file
    S.openFile()    
    # run simulator    
    S.runUntil(500)
    # close export file
    S.closeFile()
