#!/usr/bin/env python

import csv
import scipy.io.wavfile as wav

# All times must be in seconds
class DataSet:
    ''' Basic class that contains counts and time, as well as defining a rebinning function'''
    def __init__ (self, time = [], rate):
        # Defines lists of floats for times
        self.times = time
        
        # maxTimeResolution is a float that defines the binWidth (the time between each sampling of the data).
        self.maxTimeResolution = rate
    
    @classmethod
    def fromFile(cls, filename):
        (rate, data) = wav.read(filename)

        aboveThreshold = 0
        times = []
        THRESHOLD = 15000
        for i, level in enumerate(data):
            if i % rate == 0:
                print "Analyzed " + str(i/rate) + "seconds"
            if level <= THRESHOLD:
                aboveThreshold = 0
            elif aboveThreshold == 1:
                continue
            else:
                aboveThreshold = 1
                times.append(float(i)/float(rate))

        print "numCounts = " + str(len(times))
        return cls(times, rate)
    
    def rebin(self, newBinWidth):
        ''' Rebins data for some arbitrary multiple of the maxTimeResolution. A new object is returned'''
        # Determine the factor by which to scale the bins
        rebinningFactor = newBinWidth/self.maxTimeResolution
        
        # Define new variables to use in the rebinning
        newCounts = []
        newTimes = []
        
        # Determine range for i by subtracting the overflow from the length of times.
        # This does truncate the data, but it is not a full bin, so it doesn't make sense
        # to count as a bin.
        overflow = len(self.times) % rebinningFactor
        upperLimit = (len(self.times) - overflow) / rebinningFactor;
        
        for i in range(0, upperLimit):
            # newTimes are determined by the index times the newBinWidth
            newTimes.append(newBinWidth*i)
            
            # newCounts is the sum of all of the counts in all of the old bins that are
            # consolidated in the new bin. The bounds are determined by newBinWidth*i and
            # newBinWidth*(i+1). Further, this number is divided by a rebinningFactor
            # to ensure that the return result is counts per second.
            newCount = sum( self.counts[ newBinWidth*i : newBinWidth*(i+1) ] )
            newCounts.append( newCount / rebinningFactor)
            
        # Create a new object to return, so we can keep the original data
        newDataSet = DataSet(newCounts, newTimes)
        
        return newDataSet
    
def readInput(filename):
    ''' Basic function that raeds tab seperated input from text files and processes it into
        lists of floats of times and counts'''
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
