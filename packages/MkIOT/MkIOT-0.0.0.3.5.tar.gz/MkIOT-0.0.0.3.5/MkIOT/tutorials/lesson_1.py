"""
Hello, How are you? Good I hope, it's nice to meet you.
~Mark


MkIOT

These tutorials are to help you grasp MkIOT.

MkIOT was designed to make programming networking IOT devices simple and less time consuming.
-- Not to be confused - MkIOT helps you transmit data through a network, and more.


There are endless things you can create with programming, let MkIOT help you build it faster and more secure.

"""



# Let's start off with something simple, Let's get our IP Address for this device
from MkIOT import Get_Device_IPS

print(Get_Device_IPS())

# >> {'ext': ['192.168.0.3'], 'local': ['127.0.0.1']}
# You now have a dictionary containg a list of Exterior IP Addresses (Local LAN Networks) and list of Local IP Addresses (Loop back)
# We'll set a global variable for this device's first LAN IP
DEVICE_IP = Get_Device_IPS()['ext'][0]

print(DEVICE_IP)
# >> 192.168.0.3

# Lets get the Public IP Address, if your device is connected to the internet
from MkIOT import GetPublicIP

print(GetPublicIP())

# xxx.xxx.xxx.xxx
