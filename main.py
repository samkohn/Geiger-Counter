###############################
# Python script for analyzing pra data
###############################

# Imports
# External modules
import scipy as sp
import matplotlib as ml
import matplotlib.pyplot as pp

# Our modules
import analyzeData as ad


def plotCountRatePerTime(data, timeResolution = None):
    '''Plot the count rate per time using a given
    time resolution.  If timeResolution is blank then the
    default is data.maxTimeResolution (i.e. do nothing).'''


    # Rebin if necessary
    if timeResolution:
        data = data.rebin(timeResolution)

    times = sp.array(data.times)
    counts = sp.array(data.counts)

    # Plot
    pp.plot(times, counts)
    pp.show()


def plotHistOfCountRates(data, timeResolution = None, numOfBins = 10):
    '''Plot the distribution of count rates. Splits the given DataSet
    into separate 'samples' based on the timeResolution, so that 
    numSamples = totalTime/timeResolution. If a time resolution is 
    not given, the maximum possible is used for the DataSet given'''

    if timeResolution:
        data = data.rebin(timeResolution)

    # Make a histogram of the count rates from the DataSet
    hist, bin_edges = sp.histogram(data.counts, numOfBins)

    print len(hist)
    print len(bin_edges)

    pp.plot(bin_edges[range(len(bin_edges) - 1)], hist, 'ro')
    pp.show()

def main():
    '''All times are in seconds'''
    data = ad.readInput('test.txt')
    plotCountRatePerTime(data, 2)
    pp.clf()
    plotHistOfCountRates(data)
    


main()
