# classes.md

**core.py**
    
    + system
    system.__init__(name)
    system.getName(generic)
    system.displayDevices()
    system.openFile(pathName)
    system.closeFile()
    system.runStep()
    system.runUntil(time)
    system.add(device)

    + portCommon
    portCommon.addSignal()
    portCommon.get(subset)
    portCommon.size()
    portCommon.export()

    + outPort(portCommon)
    outPort.__init__(bits, name)
    outPort.set(newvalue)

    + inPort(portCommon)
    inPort.__init__(port, name, subset)
    inPort.update()

    + Device
    Device.__init__(name)
    Device.writeVar(f, t, p)
    Device.makeModule(f, t)
    Device.export()
    Device.display()
    Device.updateInputPorts()
    Device.updateOutputPorts(timestamp)

**clock.py**

    + clock(Device)
    clock.__init__(period, shift, width, count, name)
    clock.display()
    clock.updateOutputPort(timeStamp)

**counter.py**

    + counter(Device)
    counter._randbits(size)
    counter.__init__(size, name)
    counter.ilk_clk(port, subset)
    counter.ilk_clr(port, subset)
    counter.display()
    counter.updateOutputPort()

**rom.py**

    + rom(Device)
    rom.tableCheck(table)
    rom.tableImport(filename)
    rom.__init__(table, width, name)
    rom.ilk_a(port, subset)
    rom.display()
    rom.updateOutputPort(timeStamp)

