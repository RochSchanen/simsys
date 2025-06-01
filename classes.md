# classes.md

**core.py**

- EOL, SPC, NUL, TAB  

- logic_port()  
    > **\_\_init\_\_**(name, width, port, subset)  
    > **size**()  
    > **set**(new_state)  
    > **get**(subset)  
    > **update**()  
    > **export**()  

- logic_device()  
    > **\_\_init\_\_**(name)  
    > **export**()  
    > **update_input_ports**()  
    > **update_output_ports**(timeStamp)  
    > **name_duplicate**(object_list, name)  
    > **add_input_port**(port, name, subset)  
    > **add_output_port**(width, name, port, subset)  
    > **add**(device)  
    device specific:  
    > **start**()    
    > **display**()    
    > **update**(timestamp)    

- logic_system(logic_device)  
    > **\_\_init\_\_**(name)    
    > **getName**(generic)  
    > **displayDevices**()  
    > **openFile**(pathName)  
    > **closeFile**()  
    > **runStep**()  
    > **runUntil**(time)  
    > **add**(device)  

**clock.py**  

- clock(logic_device)  
    > **\_\_init\_\_**(period, shift, width, count, name)  
    > **display**()  
    > **update**(timeStamp)  

**counter.py**  

- **random_bits**(width)  

- counter(logic_device)  
    > **\_\_init\_\_**(width, name)  
    > **add_clk**(port, subset)  
    > **add_clr**(port, subset)  
    > **display**()  
    > **update**()  

**rom.py**  

- EOL, SPC, NUL, TAB  

- rom(logic_device)  
    > **table_check**(table)  
    > **load**(fp)  
    > **\_\_init\_\_**(table, width, name)  
    > **add_address**(port, subset)  
    > **display**()  
    > **update**(timeStamp)  
