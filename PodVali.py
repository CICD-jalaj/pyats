from genie.testbed import load
import subprocess
import json
import pandas as pd
from io import StringIO
import yaml, copy

import re, datetime, os, re, sys, time


class kubernet:
    '''
    taking input from execute command and converting it in to json
    and validating the Pod Running or not
    '''
    def Pod(self):
        # load the testbed file
        testbed = load('/home/gmcollection/pyats/pyats/testbed.yml')

        # let's see our testbed devices
        testbed.devices
        # TopologyDict({'vimaster-node': <Device vimaster-node at 0x7f7fb8fecb80>})

        # get the device we are interested in
        dev = testbed.devices['vimaster-node']

        # connect and run commands
        dev.connect()
        #login as root user
        dev.sudo("sudo su")
        data = dev.execute('kubectl get pods -ALL -o wide')
        #Regex to fetch the Pod Name,STATUS,IP
        result = re.findall(r"([\w\-]+)\s+\d+\/\d+\s+(\w+)\s+\d+\s+(?=.*\d+\w\s+([\d\.]+)\s+)",data, re.S)
        Jsondict = {}
        #Iterarte the result and update key in dict
        for item in result:
            Jsondict.update({'NAME' : item[0], 'STATUS' : item[1], 'IP' : item[2]})
            #dump and load json
            df = json.dumps(Jsondict, indent = 1)
            item1 = json.loads(df)

            #validate the pod is Running or not

            if item1["STATUS"] == "Running":
                print("Pod_Name: ",item1["NAME"] + "  Pod_STATUS:",item1["STATUS"] + "  Pod_IP:", item1["IP"])
            else:
                print("Pod is down:", item1["NAME"])
ob = kubernet()
ob.Pod()

