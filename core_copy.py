# CHARACTERS SYMBOLS (system dependent?)

    def export(self):
        # load configuration
        sh, fh, N = self.config
        # recursively build the export string
        expstr = ""
        for d in sh.devicelist.values(): expstr += d.export()
        # check for empty string
        if expstr is NUL: return
        # export the string
        fh.write(f"#{sh.time:04}")
        fh.write(f"{SPC}{expstr}{EOL}")
        # done
        return

    def close(self):
        # export current state
        self.export()
        # close file
        fh.close()
        # save configuration
        self.config = sh, fh, N
        return

# SYSTEM #############################################################

# the system class collects devices, runs the engine and exports the results

class system():

    # to generate one step in the simulation:
    # the step resolution is 1ns by default
    # this should be later made a parameter
    def runStep(self):
        # export state to file
        self.file.export()
        # increase time by one interval (1ns)
        self.time += 1
        # update device outputs
        for device in self.devicelist.values():
            device.updateOutputPorts(self.time)
        # update device inputs
        for device in self.devicelist.values():
            device.updateInputPorts()        
        # done
        return

    # to generate steps until 'time' is reached:
    # this can be used multiple times, each time with a 'time' value 
    # larger than the previous. this allows for executing extra code
    # at specific moment of the simulation 
    def runUntil(self, time):
        while self.time < time:
            self.runStep()
        return

# EXAMPLE ############################################################

    # instantiate simulator
    S = system("version 0.00")    

    # show all devices defined
    S.displayDevices()

    # open export file
    S.openFile()    
    # run simulator    
    S.runUntil(500)
    # close export file
    S.closeFile()
