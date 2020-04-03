#!/usr/bin/python3

import ipaddress
import struct
import sys
import argparse

"""
greg dunlap / Celtic Cow
03.12.20

take output of hex fw conn dump

fw tab -t connections -u > file.txt

convert from hex IP's to human format

version 0.4
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

def main():

    parser = argparse.ArgumentParser(description='Checkpoint Hex Conn Table convert to human format')
    parser.add_argument("-f", required=True, help="name of input file")

    args = parser.parse_args()

    inputfile = args.f 

    debug = 0

    #inputfile = sys.argv[1]
    #inputfile = "ute-h.txt"
    fw_log = open(inputfile, "r")

    for x in fw_log:
        if(debug == 1):
            print("^^^^^^^^^^^^^^^^^")
            print(x)
            print("@@@@@@@@@@@@@@@@@")
        
        """
        skip sections of header
        """
        if("localhost:" in x):
            continue
        if("---- connections ----" in x):
            continue
        if("dynamic, id 8158" in x):
            continue
        if(x == "\n"):
            #blank line at end of table
            continue

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
                    export = outstring.split(" ")
                    #print(outstring)
                    rule = export[1] + " " + export[3] + " -> " + export[4] + " " + export[6] + " " + export[7] + " : " + export[len(export)-2] 
                    print(rule)
                else:
                    if(debug == 1):
                        print("else me")
                        print(san_data)
                    outstring = outstring + san_data + " "
        if(debug == 1):
            print("-----")
            print(outstring)
            print("*****")

    fw_log.close()
#end of main
if __name__ == "__main__":
    main()