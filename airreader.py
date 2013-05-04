#!/usr/bin/python

#######################################################
#			Airreader.py
#  Because sometimes we just want to do it easily
#######################################################

# Airreader connects as a kismet client and snarfs access points names
# The end-goal is a list of network names / bssids around your wifi card
# This tool specifically is for screen-scraping by any/everything, unlike iw

# KNOWN ISSUES: Cuts off SSIDs that have spaces in them to the first word before the space
# TODO: fix that

import socket
import time
import argparse
import sys

if len(sys.argv)<3 or ("-h" in sys.argv[1]):
    print "---------Airreader.py---------"
    print "Usage:"
    print "python airreader.py [kismet ip] [kismet port] [sniff seconds]"
    print ""
    print "Typical values:"
    print "python airreader.py 127.0.0.1 2501 10"
    print ""
    print "Bugs/Comments: Bryanhalf@gmail.com"
    exit()

ip = sys.argv[1]
port = int(sys.argv[2])
listen_time = sys.argv[3]

#establish socket
sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
sock.connect((ip,port))

#set up kismet to deliver us the networks in a good format
sock.sendall("!1 REMOVE time\n")

#I removed channel.  I dont think you/i need it.
sock.sendall("!1 enable DOT11SSID bssidmac,ssid\n")

#start listening to kismet for a prescribed amount of time
now = time.time()
data = []
while (time.time() - now) < int(listen_time):
    data.append(sock.recv(512))

#join all the socket reads
data_joined = ''.join(data)

#split the reads on newlines
data = data_joined.split('\n')

#throw away like the first 6 lines because they are kismet garbage
data = data[6:]

wifi_dict = {}
#print the resulting list, leaving out the kismet protocol garbage column

for line in data:
    if len(line)<=2:
        continue
    #there's room for improvement here since I removed channel.  It could be readded.
    splitline = line.split(' ')
    mac = splitline[1:2][0]
    #channel = line[2:3]
    ssid = ' '.join(splitline[2:-1])
    if len(mac) >= 10:
        wifi_dict[mac] = ssid

for entry in wifi_dict:    
    print("%s,%s" % (entry,wifi_dict[entry]))

#gently close the door, don't leave it open
sock.shutdown(socket.SHUT_RD)
