#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 18:25:35 2017

@author: jason
"""
#Thanks to https://www.tutorialspoint.com/python3/python_networking.htm
#for the start with Python sockets.

import csv, socket, json
from collections import defaultdict
from pprint import pprint

#This function creates and opens a socket to the machine with transaction
#data and then receives a string through the socket, closes the socket cleanly
#and returns the string.
def call_stream_object(host="ip-172-31-18-213", port=12000):
    # create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    # connect to hostname using port
    s.connect((host, port))
    # Receive up to 1024 bytes (more than enough for one transaction)
    msg = s.recv(1024)                                     
    # close the socket
    s.close()
    return(msg)
    
#These need to be specified here. It merits looking into how to pass these
#from the script initiation.
host = "ip-172-31-18-213"
port = 12000
transactions = 10000 #Number of times to open a socket and pull a transaction

#Initialize a directory to store the results.
produceTracker = defaultdict(list)

#This loop opens a socket and retrieves msg from it. msg was sent from the
#generator since this is what it does when it accepts an incoming socket
#request. Do this as many times as specified in transactions.

for i in range(transactions-1):
    #Call the function and load the result in the variable msg
    msg = call_stream_object(host,port)
    #move msg out of byte format
    row = msg.decode()
    #figure out the delimeter for this row
    dialect = csv.Sniffer().sniff(row, [',',';'])
    #load the transaction fields into a list
    fields = row.replace('"','').strip().split(dialect.delimiter)

    if fields[9] == '2': #Department = produce
        #Grab 5 of the 50 or so fields in the full transaction record
        UPC = fields[4]
        description = fields[5]
        quantity = float(fields[10])
        scale = float(fields[11])
        spend = float(fields[14])
        
        #Populate a dictionary with the fields harvested.
        if UPC in produceTracker.keys():
            #sum what needs to be summed for cumulative totals
            quantity = quantity + float(produceTracker[UPC][1])
            scale = scale + float(produceTracker[UPC][2])
            spend = spend + float(produceTracker[UPC][3])
            produceTracker[UPC] = [description, quantity, scale, spend]
        else:
            #added an entry to the dictionary for new items
            produceTracker[UPC] += [description, quantity, scale, spend]

pprint(produceTracker) #easier to read than the JSON

#write the results to a JSON file that can be the basis for anything else.
with open('produceTracker_results.json', 'w') as fout:
    json.dump(json.loads(json.dumps(produceTracker)), fout)