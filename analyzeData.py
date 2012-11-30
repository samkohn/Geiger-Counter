#!/usr/bin/env python
''' analyzeData provides data analysis and storage through the DataSet class for the Geiger-Counter lab
    in Columbia's W3081 Intermediate Physics Laboratory Course'''

import scipy as sp
import scipy.io.wavfile as wav
import pickle

# All times must be in seconds
class DataSet:
    ''' The DataSet class contains methods and members for storing count data, as well as calculating useful values
        for the Geiger-Counter lab.'''
    def __init__ (self, time = [], rate = 96000, fLength = 0):
        ''' Default constructor:
            times contains a list of floats of the starting times for each count.
            maxTimeResolution contains the number of samples per second.
            fileLength contains the length of the file in seconds.
            intervals contains the interval between each count (but is empty until getInterval() is called.
            countRates contains the count rate between each interval, as defined when calling getCountRate(). countRates ie empty until getCountRate() is called.'''
        # Defines lists of floats for times
        self.times = time
        
        # maxTimeResolution is a float that defines the binWidth by denoting the number of samples per second.
        self.maxTimeResolution = rate
        
        # fileLength describes how long the file is in seconds
        self.fileLength = fLength
        
        # Define empty interval and countRate list, which will be filled by interval below
        self.intervals = []
        self.countRates = []
    
    @classmethod
    def readWaveFile(cls, filename):
        ''' Effectively a overloaded constructor for reading in data from a wave file. THRESHOLD is the level
        above which a waveform can be considered a count. It range can be from 0 to 32768, constrained
        by output values from the (16 bit signed) wave file.'''
        (rate, data) = wav.read(filename)

        return (rate, data)

    @classmethod
    def fromWaveData(cls, i, level, aboveThresholdCount, inTimes, rate, samplesPerCount, THRESHOLD = 15000):
        ''' Effectively a overloaded constructor for procesing data from an already open wave file. 
            THRESHOLD is the level above which a waveform can be considered a count. It range can be from 0 to 32768,
            constrained by output values from the (16 bit signed) wave file. This method must be called in a loop,
            as is done in the GUI, to process the entire file.'''
        
        # Define minimum overlap between counts: 3/96000 ~ 31.25 microseconds. minOVerlapCycles rounds down
        # to the lowest integer number of samples
        minOverlap = float(3)/float(96000)
        minOverlapCycles = int(minOverlap*rate)
        
        # Displays a progress meter in the console.
        if i % rate == 0:
            print "Analyzed " + str(i/rate) + "seconds"
        
        # If the level is below THRESHOLD, then there is not count. If it is transitioning from being a count,
        # we must check to see if the end of the count was long enough to be a full count. If not, remove it.
        # This should only be relevant in the event of two overlapping waveforms.
        # NOTE: This means there is a dead time in the algorithm of 31.25 microseconds. This can be adjusted above.
        if level <= THRESHOLD:
            if aboveThresholdCount != 0:
                if aboveThresholdCount <= minOverlapCycles:
                    inTimes.pop(len(inTimes))
            aboveThresholdCount = 0
        
        # If the level is above THRESHOLD for the first time, then it is a new count. Record the beginning time
        # and increment aboveThresholdCount counter.
        elif aboveThresholdCount == 0:
            aboveThresholdCount = 1
            inTimes.append(float(i)/float(rate))
        
        # This is in the middle of a count. The previous level was above THRESHOLD, and this level was as well.
        # samplesPerCount defines a count length. We are only part of the way through the count.
        # Increment aboveThresholdCount and continue.
        elif aboveThresholdCount < samplesPerCount:
            aboveThresholdCount += 1
        
        # A full count has occurred, based on the count length defined by samplesPerCount. However, the level is
        # still above THRESHOLD, so it probably is to be two overlapping counts. If waveform is only one count, 
        # and is slightly longer than defined in samplesPerCount, then it will be removed by the first if statement.
        # If it really is two overlapping counts, this will record the start time and reset the aboveThresholdCount
        # counter.
        elif aboveThresholdCount == samplesPerCount:
            aboveThresholdCount = 1
            inTimes.append(float(i)/float(rate))
        
        return aboveThresholdCount
    
    @classmethod
    def fromSavedFile(cls, filename = "dataSet.bin"):
        ''' Effectively a overloaded constructor for importing previously analzyed data. This method imports
            the DataSet object data from a previously analzyed wave file. This object must have been saved by 
            the pickle module. If the structure of DataSet changes, then this import will likely fail.'''
        fIn = open(filename, "rb")
        
        newDataSet = pickle.load(fIn)
        fIn.close()
        return newDataSet
    
    @classmethod
    def getDeadTime(cls, firstSample, secondSample, combinedSample, sampleRate = 1):
        ''' Effectively a overloaded constructor for calculating the dead time of a Geiger-Counter. This method 
            calculates the dead time from two different samples, along with a sample with the two sources in the 
            Geiger-Counter at the same time. The first three inputs to this function must be dataSet objects,
            while the sampleRate must be an a number, in seconds, in the same form as would be passed getCountRate()'''
        # Dead time is defined as \tau = (n1 + n2 - n12)/(2n1*n2)
        n1 = firstSample.getCountRate(sampleRate)
        n2 = secondSample.getCountRate(sampleRate)
        n12 = combinedSample.getCountRate(sampleRate)
        deadTime = (n1 + n2 - n12)/(2*n1*n2)
        
        return deadTime
    
    def getCountRate(self, sampleSize = 1):
        ''' Begins with a list (numpy array) of the beginning times of each count. The input, sampleSize,
            is in seconds. It returns the rates in counts / second'''
        numBins = int(self.fileLength / sampleSize)

        # Ignore all times after the last full bin
        maxTime = numBins * sampleSize

        (rates, binEdges) = sp.histogram(self.times, numBins, (0, maxTime))
        
        # Returns the count rate in counts / second, rather than counts / bin
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
        ''' Returns the total number of counts in the sample. To compare this number to another recording, the length
            of the recordings must be same (or scaled to account for the different length of recordings). '''
        return len(self.times)
    
    def save(self, filename = "dataSet.bin"):
        ''' Saves the DataSet object to a file, set by the input. This object is saved using the pickle module.'''
        fOut = open(filename, "wb")
        
        pickle.dump(self, fOut)
        fOut.close()
    
    def rebin(self, newBinWidth):
        ''' Rebins data for some arbitrary multiple of the maxTimeResolution. A new object is returned.
            This function is deprecated, as any arbitrary count rate can now be calculated in getCountRate()'''
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
