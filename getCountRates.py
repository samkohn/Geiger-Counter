import scipy as sp

def getCountRateArray(self, sampleSize = 1)
    '''Gets an array with the count rates calculated in each interval
    of width sampleSize'''

    numBins = int(self.duration / sampleSize)

    # Ignore all times after the last full bin
    maxTime = numBins * sampleSize

    (rates, binEdges) = sp.histogram(self.times, numBins, (0, maxTime))

    print rates
    return (rates, binEdges)
