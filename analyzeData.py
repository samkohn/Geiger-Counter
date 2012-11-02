#!/usr/bin/env python

import csv

class DataSet:
    def __init__ (self, count = [], time = []):
        self.counts = count
        self.times = time

def readInput(filename):
    with open(filename, 'rb') as csvfile:
        # If a dict is desired, change to csv.DictReader() with the same arguments.
        # However, the code written below will have to be edited to deal with a dictionary
        reader = csv.reader(csvfile, delimiter='\t')
        count = []
        time = []
        for row in reader:
            count.append(row[1])
            time.append(row[0])
    
    print count
    print time
    
    data = DataSet(count[1:], time[1:])
    
    print data.counts
    print data.times
    return data
