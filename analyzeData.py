#!/usr/bin/env python

import scipy as sp
import scipy.io.wavfile as wav
import pickle

# All times must be in seconds
class DataSet:
    ''' Basic class that contains counts and time, as well as defining a rebinning function'''
    def __init__ (self, time = [], rate = 96000, fLength = 0):
        # Defines lists of floats for times
        self.times = time
        
        # maxTimeResolution is a float that defines the binWidth (the time between each sampling of the data).
        self.maxTimeResolution = rate
        
        # fileLength describes how long the file is in seconds
        self.fileLength = fLength
        
        # Define empty interval and countRate list, which will be filled by interval below
        self.intervals = []
        self.countRates = []
    
    @classmethod
    def readWaveFile(cls, filename):
        ''' Effectively a overloaded constructor for pulling in data from a wave file. THRESHOLD is the level
            above which a waveform can be considered a count. It range can be from 0 to 32768, constrained
            by output values from the (16 bit signed) wave file.'''
        (rate, data) = wav.read(filename)

        return (rate, data)

    @classmethod
    def fromWaveData(cls, i, level, aboveThreshold, inTimes, rate, THRESHOLD = 15000):
        if i % rate == 0:
            print "Analyzed " + str(i/rate) + "seconds"
        if level <= THRESHOLD:
            aboveThreshold = 0
        elif aboveThreshold == 1:
            return aboveThreshold
        else:
            aboveThreshold = 1
            inTimes.append(float(i)/float(rate))
        return aboveThreshold
    
    @classmethod
    def fromSavedFile(cls, filename = "dataSet.bin"):
        fIn = open(filename, "rb")
        newDataSet = pickle.load(fIn)
        fIn.close()
        return newDataSet
    
    @classmethod
    def getDeadTime(cls, firstSample, secondSample, combinedSample, sampleRate = 1):
        ''' Calculates the dead time from two sample, along with a combined sample. The first three inputs to this
            function must be dataSet objects, while the sampleRate must be an a number, in seconds, in the same 
            form as would be passed getCountRate()'''
        # Dead time is defined as \tau = (n1 + n2 - n12)/(2n1*n2)
        n1 = firstSample.getCountRate(sampleRate)
        n2 = secondSample.getCountRate(sampleRate)
        n12 = combinedSample.getCountRate(sampleRate)
        deadTime = (n1 + n2 - n12)/(2*n1*n2)
        
        return deadTime
    
    def getCountRate(self, sampleSize = 1):
        ''' Gets an array with the count rates calculated in each interval 
            of width sampleSize. The input, sampleSize, is in seconds. It returns the rates in counts / second'''
        numBins = int(self.fileLength / sampleSize)

        # Ignore all times after the last full bin
        maxTime = numBins * sampleSize

        (rates, binEdges) = sp.histogram(self.times, numBins, (0, maxTime))
        
        self.countRates = rates/sampleSize

        return (self.countRates, binEdges)
        
    def getInterval(self):
        ''' Calculates the interval between each count, and returns a list with those intervals '''
        self.intervals = []
        
        # len(self.times)-1 because the interval list will by definition be shorter than times by 1
        for i in range(0,len(self.times)-1):
            self.intervals.append(self.times[i+1] - self.times[i])
            
        return self.intervals
    
    def getTotalCounts(self):
        ''' Returns the total number of counts in the sample. To compare this number, the length
            of the recordings must be same '''
        return len(self.times)
    
    def save(self, filename = "dataSet.bin"):
        fOut = open(filename, "wb")
        
        pickle.dump(self, fOut)
        fOut.close()
    
    def rebin(self, newBinWidth):
        ''' Rebins data for some arbitrary multiple of the maxTimeResolution. A new object is returned.
            This function is generally deprecated, as any arbitrary count rate can now be calculated in
            getCountRate()'''
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
