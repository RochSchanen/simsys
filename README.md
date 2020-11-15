# forewords

The simsys package is a first attempt at helping building a computer logic from scratch.
The focus is based on reliability more than speed.
It is to be added to the development of brickworks.
The code will remain fairly simple (if slow) for easy debugging.
The only output so far is a VCD file which records every port values and transitions
The VCD file can easily be displayed using GTKwave (available on many platforms)
Optimisation should come last but should preserve code clarity: it is meant for development, not for productivity

# to do

- introduce high impedance values for buses: buffer device
- to do: allow to declare additional ouput port that form a subset of existing ouput ports: build bus or sigle out wires from a bus
- bus, subset, wire
- memory
- processor
- debug tools: find disconnected inputs when display
- create port constants vcc and gnd
- maybe parallel, serial load
- select random level at start up / "U" / "0" / "1"
- add a delay to the reset pulse.
- add a clear input to the reset device
- add standard gate constants for the lut
- use integer for single wire subset (if isinstance(subset, int): self.w = [subset])
