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

def rebin_factor( a, newshape ):
    '''Rebin an array to a new shape.
       newshape must be a factor of a.shape.
       Source: http://www.scipy.org/Cookbook/Rebinning
    '''

    assert len(a.shape) == len(newshape)
    assert not sp.sometrue(sp.mod( a.shape, newshape ))

    slices = [ slice(None,None, old/new) for old,new in zip(a.shape,newshape) ]
    return a[slices]

def plotCountRatePerTime(data, timeResolution = None):
    '''Plot the count rate per time using a given
    time resolution.  If timeResolution is blank then the
    default is data.maxTimeResolution (i.e. do nothing).'''

    times = sp.array(data.times)
    counts = sp.array(data.counts)

    if timeResolution:
        numBinsToCombine = timeResolution/data.maxTimeResolution
        times = ad.rebin(times, numBinsToCombine)
        counts = ad.rebin(counts, numBinsToCombine)


    pp.plot(times, counts)
    pp.show()

def main():
    data = ad.readInput('test.txt')
    plotCountRatePerTime(data)

    #array = sp.linspace(1,10)
    #print array
    #pp.plot(array,array, 'ro')
    #pp.show()


main()
