# README.md

**purpose**

    The simsys project is a coarse attempt at helping to design a computing system from scratch. The focus is largely put on reliability rather than speed optimisation.  It is later to be added to the development of brickworks. The code should remain fairly simple (if slow). The only output so far is a VCD file which records all the ports value and their transitions.  The VCD file can be displayed using GTKwave which is readily available on many platforms.  Optimisation will be last and has to preserve code clarity: it is meant for development and not for productivity.

**to do list**

    + introduce high impedance values for buses: buffer device
    + bus, subset, wire
    + register, memory, ALU, processor
    + When display, check for device setup
    + create port constants vcc and gnd
    + add parallel, serial load to counter
    + configure start up value "0", "1", "U" or random
    + add standard gate tables
    + interactivity with other systems
    + add more state:
        '1' for level high
        '0' for level low
        'U' for unknown
        'Z' for high impedance state
        'L' for pull-down
        'H' for pull-up, 
    + added delays for wires and devices
    + add sub devices
