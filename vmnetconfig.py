#!/usr/bin/python3
# This scripts identifies tags and mac addresses of networking interfaces and configure them accordingly.
# Imports
import json # to parse metadata json file

# Vars
metadata_file = "meta_data.json.sample" # The input file that contains mac
                                        # address and tag for each device

config_file = "config.json.sample" # The input file that contains networkin parameters to be configured in the NIC.

# Classes

# Definition of class NIC including mac and tag
class NIC:
    def __init__(self,mac,tag):
        self.mac = mac
        self.tag = tag
        self.ip = None
        self.prefix = None
        self.gw = None
        self.nameserver = None

    def set(self,ip=None,prefix=None,gw=None,nameserver=None):
        self.ip = ip
        self.prefix = prefix
        self.gw = gw
        self.nameserver = nameserver

    def get(self,all_settings=True):
       if all_settings:
           print(self.tag,self.mac,self.ip,self.prefix,self.gw,self.nameserver)

# A list of nics
nics = [];

# Parsing devices from metadata file.
# Each pair of mac,tag will instantiated as a new nic

try:
  with open(metadata_file,'r') as input_file:
      input_data = json.load(input_file)
  devices = input_data["devices"]
  for device in devices:
    nics.append(NIC(device["mac"],device["tags"][0]))  
except IOError:
    print('Error opening input file')

try:
  with open(config_file,'r') as input_file:
      input_data = json.load(input_file)
  devices = input_data["devices"]
  for device in devices:
      for nic in nics:
          if device["tags"][0] == nic.tag:
             nic.set(ip=device["ip"],prefix=device["prefix"],gw=device["gateway"],nameserver=device["nameserver"])
except IOError:
    print('Error opening input file')

for nic in nics:
    nic.get()
