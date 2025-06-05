# classes.md

**toolbox.py**

- **EOL, SPC, NUL, TAB**  

- **name_duplicate**(objects, name)  
- **random_bits**(bits, block)  
- **startup_bits**(bits, behav)  
- **load_table**(fp)  

**core.py**

- logic_port()  
    > **\_\_init\_\_**(name, width, port, subset)  
    > **size**()  
    > **set**(new_state)  
    > **get**(subset)  
    > **update**()  
    > **export**()  

- logic_device()  
    > **\_\_init\_\_**(name)  
    > **start**()    
    > **add_input_port**(port, name, subset)  
    > **add_output_port**(width, name, port, subset)  
    > **add**(device)  
    > **update_output_ports**(timeStamp)  
    > **update**(timestamp)  
    > **update_input_ports**()  
    > **export**()  
    > **display**()  

- logic_system(logic_device)  
    > **\_\_init\_\_**(name)  
    > **start**()  
    > **open**(fp)  
    > **add_module**(device, t)  
    > **add_signal**(device, port, t)  
    > **runUntil**(time)  
    > **runStep**()  
    > **export**()  
    > **close**()  
    > **display**()  

**clock.py**  

- clock(logic_device)  
    > **\_\_init\_\_**(period, shift, width, count, name)  
    > **update**(timeStamp)  
    > **display**()  

**counter.py**  

- counter(logic_device)  
    > **\_\_init\_\_**(width, name)  
    > **add_clk**(port, subset)  
    > **add_clr**(port, subset)  
    > **update**()  
    > **display**()  

**rom.py**  

- rom(logic_device)  
    > **\_\_init\_\_**(table, width, name)  
    > **add_address**(port, subset)  
    > **update**(timeStamp)  
    > **display**()  
