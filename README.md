**notes to self**

The simsys package is a first attempt at helping building a computer logic from scratch.  
The focus is put on reliability rather than speed.  
It is to be added to the development of brickworks.  
The code will remain fairly simple (if slow) for easy debugging.  
The only output so far is a VCD file which records every port values and transitions  
The VCD file can easily be displayed using GTKwave (available on many platforms)  
Optimisation should come last but should preserve code clarity: it is meant for development, not for productivity.  

**some things to do**

- *export the last data on closing VCD file*
- add parameter to port constructor: default value for the port.
- introduce high impedance values for buses: buffer device
- to do: allow to declare additional output port that form a subset of existing output ports:
- build bus or single out wires from a bus
- bus, subset, wire
- memory
- processor
- debug tools: find disconnected inputs when display
- create port constants vcc and gnd
- maybe parallel, serial load
- select random level at start up or "X" or "0" or "1"
- add a delay to the reset pulse.
- add a clear input to the reset device
- add standard gate constants
- use integer for single wire subset (if isinstance(subset, int): self.w = [subset])
- interactivity with other systems
- investigate default values and start up behaviour: this really requires some examination
- define more states
- use '1' for level high, '0' for level low, 'X' for unknown
- use 'Z' for high impedance state, 'L' for pull-down, 'H' for pull-up, 'W' for floating
- use 'U' for uninitialized
- create read memory function and add simple parameter for rom device
- eventually, some delays in the input ports lines and/or in the devices may be added.
- can the system system class and the device class be derived one from on another?
-
