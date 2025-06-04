# README.md

**purpose**

    The simsys project is a attempt at helping to design a computing
    system from scratch. The focus is largely put on reliability rather
    than speed optimisation.  It is later to be added to the development
    of brickworks. The code should remain simple (even if slow). The
    output so far is a VCD file which records all the ports value and
    their transitions. The VCD file can be displayed using GTKwave (a
    software readily available on most platforms). Optimisation will be
    last and will have to preserve the code clarity: it is meant for
    self learning and not for productivity.

**to do list**

    + create port constants vcc and gnd?
    + add parallel, serial load to counter
    + add standard gate tables
    + added delays for wires and devices
    + register, memory, ALU, processor
    + interactivity with other systems?
    + add more state:
        so far:
        '1' for level high
        '0' for level low
        'U' for un-initialised
        add more?
        'Z' for high impedance, floating
        'L' for pull-down
        'H' for pull-up
        '-' for don't care
        'W' for weak
        'X' for collision
    + add startup behaviour at the port level?
