#!/usr/bin/python3
# file: development.py
# content: system simulator development
# created: 2020 November 14 Saturday
# modified:
# modification:
# author: roch schanen
# comment: system architecture simulator

if __name__ == "__main__":

    from sys import version as pythonVersion

    print("file: development.py")
    print("content: system simulator development")
    print("created: 2020 November 14 Saturday")
    print("author: roch schanen")
    print("comment:")
    print("run Python3:" + pythonVersion);

    from core import system
    from library import lut

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
