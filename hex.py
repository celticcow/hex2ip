#!/usr/bin/python3

import ipaddress
import struct
import sys

"""
greg dunlap / Celtic Cow
03.06.20

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

    return(element)

def hex2dec(ip_addr):

    addr_long = int(ip_addr, 16)
    hex(addr_long)
    dec = ipaddress.IPv4Address(struct.pack(">L", addr_long))

    return(dec)

def zerohex2dec(num):
    i = int(num, 16)
    return(str(i))


if __name__ == "__main__":

    debug = 0

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
        if(debug == 1):
            print("^^^^^^^^^^^^^^^^^")
            print(x)
            print("@@@@@@@@@@@@@@@@@")

        outstring = ""
        conn_entry = x.split(" ")
        for entry in conn_entry:

            san_data = cleandata(entry)

            if(san_data[0:4] == "0000"):
                if(debug == 1):
                    print(zerohex2dec(san_data))
                outstring = outstring + zerohex2dec(san_data) + " "
            else:
                #print(san_data)
                try:
                    if(debug == 1):
                        print(san_data)
                        print(hex2dec(san_data))
                        print("ip-me")
                    outstring = outstring + str(hex2dec(san_data)) + " "
                except ValueError as e:
                    if(debug == 1):
                        print("EXCEPT")
                        print(san_data)
                    outstring = outstring + san_data + " "
                    print(outstring)
                else:
                    if(debug == 1):
                        print("else me")
                        print(san_data)
                    outstring = outstring + san_data + " "
        if(debug == 1):
            print("-----")
            print(outstring)
            print("*****")
        #print(conn_entry[0])
        #print(conn_entry[1])


    fw_log.close()
    #end of main