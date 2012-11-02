#!/usr/bin/env python

import csv

# All times must be in seconds
class DataSet:
    def __init__ (self, count = [], time = []):
        # Defines lists of floats for counts and times
        self.counts = count
        self.times = times
        
        # maxTimeResolution defines the binWidth (the time between each sampling of the data).
        # This is a number
        self.maxTimeResolution = abs(self.times[len(self.times)-1] - self.times[len(self.times)-2])
    
    def rebin(self, newBinWidth):
        # Determine the factor by which to scale the bins
        rebinningFactor = newBinWidth/self.maxTimeResolution
        
        newCounts = []
        newTimes = []
        for i in range(0,len(self.times)/rebinningFactor):
            newCounts.append( sum( self.counts[ newBinWidth*i : newBinWidth*(i+1) ] ))
            newTimes.append(newBinWidth*i)
        
        newDataSet = DataSet(newCounts, newTimes)
        
        return newDataSet
    
def readInput(filename):
    with open(filename, 'rb') as csvfile:
        # csv.reader returns a list containing strings, from a tab seperated text file.
        # Based on data taken with PRA 5, the first element in entry of the list it the time,
        # while the second is the rows
        reader = csv.reader(csvfile, delimiter='\t')
        count = []
        time = []
        for row in reader:
            time.append(row[0])
            count.append(row[1])
    
    # Ensures that the data being passed in is actually a number (based on the data read using
    # csv.reader(), these lists are actually strings containing numbers, so this format must be
    # converted into numbers using float()).
    count = [float(value) for value in count if value.isdigit() == True]
    time = [float(value) for value in time if value.isdigit() == True]
    
    data = DataSet(count, time)
    
    print data.counts
    print data.times
    print data.maxTimeResolution
    return data