#!/usr/bin/env python

import csv
import scipy as sp

class DataSet:
    def __init__ (self, count = [], time = []):
        # Defines counts and times lists, while ensuring that the data being passed in is actually
        # a number (based on the data read using csv.reader(), these lists are actually strings containing
        # numbers, but this format of the data works fine with matplotlib).
        self.counts = [value for value in count if value.isdigit() == True]
        self.times = [value for value in time if value.isdigit() == True]
        
        # maxTimeResolution defines the binWidth (the time between each sampling of the data).
        # This is a number
        self.maxTimeResolution = abs(float(self.times[len(self.times)-1]) - float(self.times[len(self.times)-2]))
        
    
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
    
    data = DataSet(count, time)
    
    print data.counts
    print data.times
    print data.maxTimeResolution
    return data

def rebin( a, newshape):
    '''Rebin an array to a new shape.
       newshape must be a factor of a.shape.
       Source: http://www.scipy.org/Cookbook/Rebinning
    '''

    assert len(a.shape) == len(newshape)
    assert not sp.sometrue(sp.mod( a.shape, newshape ))

    slices = [ slice(None,None, old/new) for old,new in zip(a.shape,newshape) ]
    return a[slices]