#!/usr/bin/env python
import pychaos
import sys
import time


if len(sys.argv)<4:
    print("You must specify a <server:port> <PSNAME> <current value>");
    sys.exit(1);
else:
    pychaos.setOptions({"uri":sys.argv[1]})

try:
## get the output channel
    ps_out=pychaos.getChannel(sys.argv[2],0);
    if(ps_out[0]["stby"]):
        ## e' off metti polarity pos
        print(sys.argv[2] + " CLEAR STBY  and polarity pos")
        pychaos.setAttribute(sys.argv[2],"polarity",1)
        pychaos.setAttribute(sys.argv[2],"stby",0)


    pychaos.setAttribute(sys.argv[2],"current",sys.argv[3])
    ## give time to set busy
    print("Wating the command will set busy")

    time.sleep(3)
    while True:
        ps_all=pychaos.getChannel(sys.argv[2],-1);
        if(ps_all[0]["system"]["busy"] == False):
            print("Operation Ended")
            print(ps_all)
            break;
        else:
            print("."),
            sys.stdout.flush()


except pychaos.ChaosException as err:
    print("EXCEPTION:",err)
