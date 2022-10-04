#!/usr/bin/python3
# This scripts identifies tags and mac addresses of networking interfaces and configure them accordingly.
# Imports
import json # to parse metadata json file

# Vars
metadata_file = "meta_data.json.sample" # The input file that contains mac
                                        # address and tag for each device

# Classes

# Definition of class NIC including mac and tag
class NIC:
    def __init__(self,mac,tag):
        self.mac = mac
        self.tag = tag

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
