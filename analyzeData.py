#!/usr/bin/env python

import csv

def readInput(filename):
    with open(filename, 'rb') as csvfile:
        # If a dict is desired, change to csv.DictReader() with the same arguments.
        # However, the code written below will have to be edited to deal with a dictionary
        reader = csv.reader(csvfile, delimiter='\t')
        for row in reader:
            print row[1]
    