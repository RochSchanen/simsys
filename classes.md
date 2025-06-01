# classes.md

**core.py**

- EOL, SPC, NUL, TAB  

- logic_port()  
    > logic_port.**\_\_init\_\_**(name, width, port, subset)  
    > logic_port.**size**()  
    > logic_port.**set**(new_state)  
    > logic_port.**get**(subset)  
    > logic_port.**update**()  
    > logic_port.**export**()  

- logic_device()  
    > logic_device.**\_\_init\_\_**(name)  
    > logic_device.**export**()  
    > logic_device.**update_input_ports**()  
    > logic_device.**update_output_ports**(timeStamp)  
    > logic_device.**name_duplicate**(object_list, name)  
    > logic_device.**add_input_port**(port, name, subset)  
    > logic_device.**add_output_port**(width, name, port, subset)  
    > logic_device.**add**(device)  
    (device specific)  
    > logic_device.**start**()    
    > logic_device.**display**()    
    > logic_device.**update**(timestamp)    

- logic_system(logic_device)  
    > system.**\_\_init\_\_**(name)    
    > system.**getName**(generic)  
    > system.**displayDevices**()  
    > system.**openFile**(pathName)  
    > system.**closeFile**()  
    > system.**runStep**()  
    > system.**runUntil**(time)  
    > system.**add**(device)  

**clock.py**  

- clock(logic_device)  
    > clock.**\_\_init\_\_**(period, shift, width, count, name)  
    > clock.**display**()  
    > clock.**update**(timeStamp)  

**counter.py**  

- **random_bits**(width)  

- counter(logic_device)  
    > counter.**\_\_init\_\_**(width, name)  
    > counter.**add_clk**(port, subset)  
    > counter.**add_clr**(port, subset)  
    > counter.**display**()  
    > counter.**update**()  

**rom.py**  

- EOL, SPC, NUL, TAB  

- rom(logic_device)  
    > rom.**table_check**(table)  
    > rom.**load**(fp)  
    > rom.**\_\_init\_\_**(table, width, name)  
    > rom.**add_address**(port, subset)  
    > rom.**display**()  
    > rom.**update**(timeStamp)  
