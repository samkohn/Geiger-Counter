#!/usr/bin/env python

import csv

class DataSet:
    def __init__ (self, count = [], time = []):
        self.counts = count
        self.times = time
        self.maxTimeResolution = abs(float(self.times[len(self.times)-1]) - float(self.times[len(self.times)-2]))
        

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
    
    # Remove header strings
    count = [value for value in count if value.isdigit() == True]
    time = [value for value in time if value.isdigit() == True]
            
    #data = DataSet(count[1:], time[1:])
    data = DataSet(count, time)
    
    print data.counts
    print data.times
    print data.maxTimeResolution
    return data
