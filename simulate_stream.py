# -*- coding: utf-8 -*-
"""
This snippet of code will simulate the arrival of streaming transaction data
from a wedge transaction file. To use it, put one or more transaction files in
input_path. (Two samples I am using are in the repo.)

get_data() creates a generator that, when called, iterates through the transaction
file in order to grab the next line. The for loop will progress through the 
files in input_path and pass input_filename to get_data(), storing the yielded
value as trans_generator. Pull that value from the generator with next() and you
can simulate the arrival of a streamed transaction, to do with it what you will
from there on out.
"""


import os

#Place one or more Wedge transaction files in the input path
input_path='/mnt/c/Users/Jason/VMshare/wedge_transactions/'

#https://indico.io/blog/fast-method-stream-data-from-big-data-sources/
def get_data(input_file, delimiter = '\t'): #my files are tab delimited
    with open(input_file, 'r') as f:
        for record in f:                 
            x = record.strip().split(delimiter)
            yield x
            
for file in os.listdir(input_path):
    input_filename = input_path + file
    trans_generator = get_data(input_filename)

next(trans_generator)