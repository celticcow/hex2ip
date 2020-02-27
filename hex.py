#!/usr/bin/python3

import ipaddress
import struct

print("start")

#ip_addr = "FFFFFFFF"

#ip_addr = "92120289"  #146.18.2.137
ip_addr = "0AFF1205"   #

addr_long = int(ip_addr, 16)
hex(addr_long)

#struct.pack("<L", addr_long)

###  >L vs <L   bad mojo

print(ipaddress.IPv4Address(struct.pack(">L", addr_long)))