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


def plotCountRate(data, timeResolution = 1):
    '''Plot the count rate per time using a given
    time resolution.  If timeResolution is blank then the
    default is data.maxTimeResolution (i.e. do nothing).'''


    # Rebin if necessary
#    if timeResolution:
#        data = data.rebin(timeResolution)
#


    (rates, binEdges) = data.getCountRate(timeResolution)

    # Plot
    graph = pp.figure().add_subplot(111)

    graph.plot(binEdges[0:(len(binEdges)-1)],rates)
    graph.set_title("Count Rate. sample size = " + str(timeResolution) + " sec.")
    pp.show()


def plotHistOfCountRates(data, timeResolution = 1, numOfBins = 10):
    '''Plot the distribution of count rates. Splits the given DataSet
    into separate 'samples' based on the timeResolution, so that 
    numSamples = totalTime/timeResolution. If a time resolution is 
    not given, a default value of 1s is used'''

    #if timeResolution:
    #    data = data.rebin(timeResolution)

    (rates, binEdges) = data.getCountRate(timeResolution)

    # Make a histogram of the count rates from the DataSet
    #(distribution, binEdges) = sp.histogram(rates, numOfBins)

    graph = pp.figure().add_subplot(111)

    #graph.plot(binEdges[range(len(binEdges) - 1)], distribution, 'ro')
    (n, bins, patches) = graph.hist(rates, numOfBins)
    graph.set_title("Hist of count rates. " + str(numOfBins) + " bins, sample length " + str(timeResolution) + " sec, bin width = " + str(bins[1]-bins[0]) + " sec.")
    pp.show()


def plotHistOfIntervals(data, numOfBins = 10):
    '''Plot a histogram of the time interval between consecutive counts'''

    #hist, binEdges = sp.histogram(data.getInterval(), numOfBins)

    graph = pp.figure().add_subplot(111)

    #graph.plot(binEdges[0:(len(binEdges)-1)], hist)
    (n, bins, patches) = graph.hist(data.getInterval(), numOfBins)
    graph.set_title("Hist of interval between consecutive counts. " + str(numOfBins) + " bins, bin width = " + str(bins[1]-bins[0]) + " sec.")
    pp.show()

def main():
    '''All times are in seconds'''
    data = ad.readInput('test.txt')
    plotCountRatePerTime(data, 2)
    pp.clf()
    plotHistOfCountRates(data)
    



#main()
