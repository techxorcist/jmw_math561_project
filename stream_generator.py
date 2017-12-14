#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 15:49:18 2017

@author: jason
"""
#Thanks to https://www.tutorialspoint.com/python3/python_networking.htm
#for the start with Python sockets.

import sys, os
import socket

#Determine whether this is being done locally or in AWS
#if os.environ['NAME'] == 'LAPTOP-KIK2KB0S':
#    input_path='/mnt/c/Users/Jason/VMshare/wedge_transactions/'
#elif os.environ['NAME'] == 'ip-172-31-18-213':
#    input_path='/home/ubuntu/wedgetransactionsbucket/wedge_transaction_files/'
#else:
#    print('Just where the hell do you think you are?')
#    sys.exit

#Set these as appropriate for your environment below.
input_path=''

#This function takes a file name as an argument and iterates through the
#lines in the file, yielding one record (as determined by the newline
#character) each time the function is called.         
def get_data(input_file): 
    with open(input_file, 'r') as f:
        for record in f:
            record = record.encode()
            yield record

#This loop figures out the filenames where the transactions are stored
#and passes the filename to get_data() so trans_generator can be called
#as a generator whenever a socket connection is accepted.
for file in os.listdir(input_path):
    input_filename = input_path + file
    trans_generator = get_data(input_filename)
    
#Set up the socket parameters here.
streamersocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Bind to the socket here, closing the socket if it wasn't properly
#terminated by a previous iteration of the script.
try:
    streamersocket.bind((socket.gethostname(), 12000))
except OSError:
    streamersocket.close(socket.gethostname(), 12000)
    streamersocket.bind((socket.gethostname(), 12000))

#Wait for incoming connections
streamersocket.listen(2)

while True: #The while loop executes when a client socket is accepted
    #When a connection is accepted, return the connection info
    (clientsocket, address) = streamersocket.accept()
    #Note another connection made
    print("Got a connection from %s" % str(address))
    #Load a transaction into msg using the generator
    msg = next(trans_generator)
    #Push that transaction out the socket
    clientsocket.send(msg)
    #Close the socket
    clientsocket.close()