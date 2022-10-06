#!/usr/bin/python3
# This scripts identifies tags and mac addresses of networking interfaces and configure them accordingly.
# Imports
import json # to parse metadata json file
import os
import gi
gi.require_version("NM", "1.0")
from gi.repository import GLib, NM

# Vars
metadata_file = "meta_data.json.sample" # The input file that contains mac
                                        # address and tag for each device

config_file = "config.json.sample" # The input file that contains networkin parameters to be configured in the NIC.

# Classes

# Definition of class NIC including mac and tag
class NIC:
    def __init__(self,mac,tag):
        self.mac = mac.upper()
        self.interface = None
        self.tag = tag.upper()
        self.ip = None
        self.prefix = None
        self.gw = None
        self.nameserver = None

    def set_ip_settings(self,ip=None,prefix=None,gw=None,nameserver=None):
        self.ip = ip
        self.prefix = prefix
        self.gw = gw
        self.nameserver = nameserver

    def set_interface(self,interface):
        self.interface = interface

    def set_connection(self,connection_id):
        self.id = connection_id

    def get(self,all_settings=True):
       if all_settings:
           print(self.id,self.tag,self.interface,self.mac,self.ip,self.prefix,self.gw,self.nameserver)

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
          if device["tags"][0].upper() == nic.tag:
             nic.set_ip_settings(ip=device["ip"],prefix=device["prefix"],gw=device["gateway"],nameserver=device["nameserver"])
except IOError:
    print('Error opening input file')

client = NM.Client.new(None)
devices = client.get_devices()
for device in devices:
    for nic in nics:
        try:
          if device.get_hw_address() == nic.mac:
            nic.set_interface(device.get_iface())
            nic.set_connection(device.get_active_connection().get_id())
            new_config = "nmcli con mod "+ "'" + nic.id + "'" + " ipv4.method manual ipv4.addresses " + nic.ip + "/" + nic.prefix + " ipv4.gateway " + nic.gw + " ipv4.dns " + nic.nameserver + " ipv6.method disabled"
            save_config = "nmcli con up " + "'" + nic.id + "'"
            os.system(new_config)
            os.system(save_config)
        except:
          print("An error occurred when setting the network configuration")
