'''A GUI program to analyze data from the geiger counter experiment'''

# The GUI package for python
import Tkinter as tk
import tkFileDialog as tkfd
import tkMessageBox as tkmb
import tkSimpleDialog as tksd

# Our analysis tools
import analyzeData as ad
import PlotData as pd

class App:
    '''The driver class for the program, which contains all of the methods and
    GUI elements for the program'''

    def __init__(self, master):
        '''Creates a new App window from scratch'''

        #save the root TK frame
        self.root = master

        #create a frame for all of the buttons
        frame = tk.Frame(self.root)
        frame.pack()

        #Quit button
        self.quitButton = tk.Button(frame, text="Quit", fg="red", command=frame.quit)
        self.quitButton.pack(side=tk.LEFT)

        #label to display the name of the currently loaded file
        self.fileName = tk.Label(frame, text="No File")
        self.fileName.pack(side=tk.BOTTOM)

        #frame to hold the analysis buttons
        buttonFrame = tk.Frame(frame)

        #add all of the buttons for analysis
        self.addMenuButtons(frame)
        buttonFrame.pack(side=tk.LEFT)

        #the DataSet that is being analyzed
        self.dataSet = None

        #label for .wav file import progress
        self.progressLabel = None

    def addMenuButtons(self, master):
        '''Add the standard set of analysis buttons to the given master frame.'''

        #list of buttons and associated actions to execute on click
        buttons = [
            ("Calibrate .wav Importer", self.showThresholdGraph),
            ("Import .wav File", self.importWavFile),
            ("Import Saved Data", self.openBinary),
            ("Save Data to Disk", self.saveBinary),
            ("Export Data in Plaintext", self.export),
            ("Plot Count Rate vs. Time", self.getCountRate),
            ("Plot Count Rate Histogram", self.getCountRateHist),
            ("Plot Intervals Histogram", self.getIntervals),
            ("Get Total Counts", self.getTotalCounts)
        ]


        #create the buttons
        for label, cmd in buttons:
            b = tk.Button(master, text=label, command=cmd)
            b.pack(anchor=tk.S)


    # to do: update labels
    def importWavFile(self):
        '''Get the data from a .wav file. Prompts the user with a file dialog.
        Prompts the user for a threshold value.  This is the value of the .wav 
        data that will trigger a count (higher = stricter, fewer counts detected).'''

        #prompt for file name
        filename = tkfd.askopenfilename(title="Pick your .wav file", initialdir=".", parent=self.root)
        if not filename:
            return
        print filename

        #grab the data rate (points per second) and a list of data
        rate, wavData = ad.DataSet.readWaveFile(filename)

        #grab threshold from user
        labelText = "Enter the threshold for detecting a count. If you don't know what this means, read the lab manual!"
        threshold = tksd.askinteger("Threshold", labelText, parent=self.root, minvalue=0, initialvalue=15000)
        if not threshold:
            return

        #list of the time of each count
        times = []

        # label for showing import progress
        if self.progressLabel: # if it already exists
            pass
        else:
            self.progressLabel = tk.Label(self.root)
            self.progressLabel.pack(side=tk.BOTTOM)

        #boolean for if the current data is during a count or not during a count
        # 0 means no count, 1 means count
        aboveThreshold = 0

        #loop through data and grab count times
        for i, level in enumerate(wavData):
            #update the progress label every second (i % rate == 0)
            if i % rate == 0:
                self.updateFileProgress(self.progressLabel, i, len(wavData))
                self.root.update_idletasks()
                print "gui reached ", i, "data points"

            #check if the current data level is above the threshold
            aboveThreshold = ad.DataSet.fromWaveData(i, level, aboveThreshold, times, rate, threshold) 

        #when the loop is finished, update the label one last time
        self.progressLabel.configure(text="Import Progress: 100%")

        print "numCounts = " + str(len(times))

        #length of file (in seconds) is used in class ad.DataSet
        fileLength = float(len(wavData))/float(rate)
        
        # create DataSet
        self.dataSet = ad.DataSet(times, rate, fileLength)
        print "imported"

        #display the name of the current file in a label
        self.updateFileLabel(filename)

    def updateFileProgress(self, label, value, maximum):
        '''Updates the label with the expression "Progress: <percent complete>%",
        where <percent complete> is the first two characters of value/maximum'''

        text = "Progress: " + str(value/float(maximum) * 100)[0:2] + "%"
        label.configure(text=text)

    def getCountRate(self):
        '''Plots the count rate as a function of time. The rates are calculated
        for each "bin" (i.e. independent sample)'''

        #Check if data has been imported. if not, give a warning
        if self.dataSet:

            #prompt for desired bin spacing
            labelText = "Enter the desired sample length in seconds"
            binSpacing = tksd.askfloat("Count Rate", labelText, parent=self.root, minvalue=0, initialvalue=1)
            if not binSpacing:
                return

            #plot the count rate in matplotlib
            pd.plotCountRate(self.dataSet, binSpacing)
            
        else:
            #say that you need to import data first
            self.showImportAlert()

    def getCountRateHist(self):
        '''Plots a histogram of the count rate.  The number of bins is 
        for the histogram, and the sample length is how long the count rate
        is averaged over (equivalent to "sample length" for the count rate
        vs. time graph.'''

        #check if data has been imported. if not, give a warning
        if self.dataSet:

            #ask for number of bins for histogram
            labelText = "Enter the number of bins"
            numBins = tksd.askinteger("Count Rate Histogram", labelText, parent=self.root, minvalue=1)
            if not numBins:
                return

            #ask for length of sample to calculate count rate
            labelText = "Enter the sample length (seconds)"
            sampleLength = tksd.askfloat("Sample Length", labelText, parent=self.root, minvalue=0)
            if not sampleLength:
                return

            #plot histogram in matplotlib
            pd.plotHistOfCountRates(self.dataSet, sampleLength, numBins)

        else:
            self.showImportAlert()

    def getIntervals(self):
        '''Plots a histogram of the time interval length between consecutive
        counts.'''

        #check if data has been imported. if not, give a warning
        if self.dataSet:

            #ask for the number of bins for the histogram
            labelText = "Enter the desired number of bins in the histogram"
            numBins = tksd.askinteger("Intervals Histogram", labelText, parent=self.root, minvalue=1)
            if not numBins:
                return

            #plot the histogram in matplotlib
            pd.plotHistOfIntervals(self.dataSet, numBins)

        else:
            self.showImportAlert()

    def getTotalCounts(self):
        '''Displays the total number of counts in a given sample'''
        
        #check if data has been imported. if not, give a warning
        if self.dataSet:

            #fetch the value from the stored data
            totalCounts = self.dataSet.getTotalCounts()

            #display the value in a window
            print totalCounts
            tkmb.showinfo("Total counts", str(totalCounts) + " counts total")

        else:
            self.showImportAlert()




    def saveBinary(self):
        '''Saves the currently imported data in a binary file for easy import
        in the future. Prompts for a file name in a dialog.
        This is much faster than importing from .wav file so it should be
        used every time except for the first that the data is imported.'''

        #check if data has been imported. if not, give a warning
        if self.dataSet:
            
            #prompt for the save location
            filename = tkfd.asksaveasfilename(initialdir=".", title="Save Data")
            if not filename:
                return
            self.dataSet.save(filename)
            print "saved"

        else:
            #say that you need to import data first
            self.showImportAlert()


    def export(self):
        '''Exports the count times to a return-separated text file with a one-line header'''

        #check if data has been imported. if not, give a warning
        if self.dataSet:
            
            #prompt for the save location
            filename = tkfd.asksaveasfilename(initialdir=".", title="Export")
            if not filename:
                return
            self.dataSet.exportCSV(filename)
            print "exported"

        else:
            #say that you need to import data first
            self.showImportAlert()


    def openBinary(self):
        '''Imports a previously-saved binary file containing a data set.
        This is much faster than importing from .wav file so it should be
        used every time except for the first that the data is imported.'''

        #prompt for file name
        filename = tkfd.askopenfilename(initialdir=".", title="Open File")
        if not filename:
            return

        #import the file and record the DataSet
        self.dataSet = ad.DataSet.fromSavedFile(filename)
        print "opened"

        #update the label showing the current file
        self.updateFileLabel(filename)

    def showImportAlert(self):
        '''Show an alert dialog indicating there is no active data.'''

        #show the alert dialog
        tkmb.showerror("No Data", "You need to import data first!")

    def updateFileLabel(self, filename):
        '''Update the label that displays the currently active file.'''

        #show the first directory in the path and the file name:
        # e.g. Users/.../data.wav
        # or Users\...\data.wav

        #different file separator for windows and unix
        #first, unix
        if(filename.find("/") >= 0):
            path = filename.split("/")
            self.fileName.configure(text=path[1] + "/.../" + path[len(path)-1])
        else:
            #escape backslashes! \ => \\
            path = filename.split("\\")
            self.fileName.configure(text=path[1] + "\\...\\" + path[len(path)-1])

    def showThresholdGraph(self):
        '''Shows a graph of the .wav amplitudes so that the user can figure out a good threshold'''
        #pass
        #import the first 5 seconds of the .wav file

        #prompt for file name
        filename = tkfd.askopenfilename(title="Pick your .wav file", initialdir=".", parent=self.root)
        if not filename:
            return

        rate, wavData = ad.DataSet.readWaveFile(filename)
        #get the first 5 seconds of data
        numEntriesFor5Sec = rate * 5;
        first5Sec = wavData[1:numEntriesFor5Sec];
        
        #plot data
        pd.plot(first5Sec, "Calibrate the Threshold!")



        


# Create the Tk application window
root = tk.Tk()

# Create the App which is defined above
app = App(root)

# Give the app window a title
app.root.title("Geiger Counter Analysis")

# Run the app (mainloop is tk syntax for "go")
root.mainloop()
