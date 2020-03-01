#!/usr/bin/python3

import ipaddress
import struct

"""
greg dunlap / Celtic Cow
02.29.20

take output of hex fw conn dump

fw tab -t connections -u > file.txt

convert from hex IP's to human format

"""

def cleandata(element):

    if(element[len(element)-1] == "\n"):
        element = element.rstrip(">\n")
    if((element[0] == "(") and (element[len(element)-1] == "\n")):
        element = element.lstrip("(")
        element = element.rstrip(")\n")
    if(element == "->"):
        element = "FFFFFFFF"
    if((element[0] == "<") and (element[len(element)-1] == "\n")):
        element = element.lstrip("<")
        element = element.rstrip(">\n")
    if(element[0] == "<"):
        element = element.lstrip("<")
    if(element[0] == "("):
        element = element.lstrip("(")
    if(element[len(element)-1] == ","):
        element = element.rstrip(",")
    if(element[len(element)-1] == ";"):
        element = element.rstrip(";")
    if(element[len(element)-1] == ">"):
        element = element.rstrip(">")
    if(element[len(element)-1] == ")"):
        element = element.rstrip(")")

    #print("^^^^^^^^^^^^^^^")
    #print(element)
    #print("$$$$$$$$$$$$$$$")

    return(element)

def hex2dec(ip_addr):

    addr_long = int(ip_addr, 16)
    hex(addr_long)
    dec = ipaddress.IPv4Address(struct.pack(">L", addr_long))

    return(dec)

if __name__ == "__main__":

    debug = 1

    print("start")

    #ip_addr = "FFFFFFFF"

    #ip_addr = "92120289"  #146.18.2.137
    #ip_addr = "0AFF1205"   #10.255.18.5

    #ip_addr = input("What is the HEX IP: ")

    #addr_long = int(ip_addr, 16)
    #hex(addr_long)

    #struct.pack("<L", addr_long)

    ###  >L vs <L   bad mojo

    #print(ipaddress.IPv4Address(struct.pack(">L", addr_long)))

    fw_log = open("test1.txt", "r")

    for x in fw_log:
        print(x)
        conn_entry = x.split(" ")
        for entry in conn_entry:
            san_data = cleandata(entry)

            #print(san_data)
            try:
                print(san_data)
                print(hex2dec(san_data))
            except:
                print(san_data)

        #print(conn_entry[0])
        #print(conn_entry[1])


    fw_log.close()
    #end of main