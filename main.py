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


def plotObject(obj):
    times = sp.array(obj.times)
    counts = sp.array(obj.counts)
    pp.plot(times, counts)
    pp.show()

def main():
    data = ad.readInput('test.txt')
    plotObject(data)

    #array = sp.linspace(1,10)
    #print array
    #pp.plot(array,array, 'ro')
    #pp.show()


main()
