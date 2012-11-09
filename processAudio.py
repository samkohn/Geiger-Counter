# File for importing audio levels and outputing count rates

import csv
import scipy.io.wavfile as wav
import matplotlib.pyplot as pp




def testWave(filename):
    (rate, data) = wav.read(filename)

    aboveThreshold = 0
    numCounts = 0
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
            numCounts += 1

    print "numCounts = " + str(numCounts)


def graphWave(filename):
    (rate, data) = wav.read(filename)

    pp.plot(data)
    pp.show()

testWave("strontium.90.11.9.96000.wav")
#graphWave("strontium.90.11.9.96000.wav")
