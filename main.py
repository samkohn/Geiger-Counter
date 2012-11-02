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

def main():
    #print "hello, world"
    #ad.readInput("test.txt")
    array = sp.linspace(1,10)
    print array
    pp.plot(array,array, 'ro')
    pp.show()


main()
