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

    def __init__(self, master):
        
        self.root = master
        frame = tk.Frame(self.root)
        frame.pack()

        self.quitButton = tk.Button(frame, text="Quit", fg="red", command=frame.quit)
        self.quitButton.pack(side=tk.LEFT)

        self.fileName = tk.Label(frame, text="No File")
        self.fileName.pack(side=tk.BOTTOM)

        buttonFrame = tk.Frame(frame)
        self.addMenuButtons(frame)
        buttonFrame.pack(side=tk.LEFT)

        self.dataSet = None

    def addMenuButtons(self, master):
        buttons = [
            ("Import .wav File", self.importWavFile),
            ("Import Saved Data", self.openBinary),
            ("Save Data to Disk", self.saveBinary),
            ("Plot Count Rate vs. Time", self.getCountRate),
            ("Plot Count Rate Histogram", self.getCountRateHist),
            ("Plot Intervals Histogram", self.getIntervals),
            ("Get Total Counts", self.getTotalCounts)
        ]


        for label, cmd in buttons:
            b = tk.Button(master, text=label, command=cmd)
            b.pack(anchor=tk.S)


    def importWavFile(self):
        filename = tkfd.askopenfilename(title="Pick your .wav file", initialdir=".", parent=self.root)
        print filename
        self.dataSet = ad.DataSet.fromWaveFile(filename)
        print "imported"
        self.updateFileLabel(filename)

    def getCountRate(self):
        if self.dataSet:
            #prompt for desired bin spacing

            #inputDialog = tk.TopLevel(self.root, title="Count Rate")
            labelText = "Enter the desired sample length in seconds"
            #tk.Label(inputDialog, text=labelText).pack()
            #submitButton = tk.Button(inputDialog, text="OK", command=

            #dialog = InputDialog(self.root, "Count Rate", labelText)
            binSpacing = tksd.askfloat("Count Rate", labelText, parent=self.root, minvalue=0)
            

            #print str(self.dataSet.getCountRate(binSpacing))
            #do something with the results
            pd.plotCountRate(self.dataSet, binSpacing)
            

        else:
            #say that you need to import data first

            self.showImportAlert()

    def getCountRateHist(self):
        if self.dataSet:
            labelText = "Enter the number of bins"
            numBins = tksd.askinteger("Count Rate Histogram", labelText, parent=self.root, minvalue=1)
            labelText = "Enter the sample length (seconds)"
            sampleLength = tksd.askfloat("Sample Length", labelText, parent=self.root, minvalue=0)
            pd.plotHistOfCountRates(self.dataSet, sampleLength, numBins)

        else:
            self.showImportAlert()

    def getIntervals(self):
        if self.dataSet:
            print self.dataSet.getInterval()
            labelText = "Enter the desired number of bins in the histogram"
            numBins = tksd.askinteger("Intervals Histogram", labelText, parent=self.root, minvalue=1)
            pd.plotHistOfIntervals(self.dataSet, numBins)
        else:
            self.showImportAlert()

    def getTotalCounts(self):
        if self.dataSet:
            totalCounts = self.dataSet.getTotalCounts()
            print totalCounts
            tkmb.showinfo("Total counts", str(totalCounts) + " counts total")

        else:
            self.showImportAlert()




    def saveBinary(self):
        if self.dataSet:
            filename = tkfd.asksaveasfilename(initialdir=".", title="Save Data")
            self.dataSet.save(filename)
            print "saved"
        else:
            #say that you need to import data first
            self.showImportAlert()


    def openBinary(self):
        filename = tkfd.askopenfilename(initialdir=".", title="Open File")
        self.dataSet = ad.DataSet.fromSavedFile(filename)
        print "opened"
        self.updateFileLabel(filename)

    def showImportAlert(self):
        tkmb.showerror("No Data", "You need to import data first!")

    def updateFileLabel(self, filename):
        if(filename.find("/") >= 0):
            path = filename.split("/")
            self.fileName.configure(text=path[1] + "/.../" + path[len(path)-1])
        else:
            path = filename.split("\\")
            self.fileName.configure(text=path[1] + "\\...\\" + path[len(path)-1])
        



#class InputDialog:
#    def __init__ (self, parent, title, label):
#        
#        self.window = tk.Toplevel(parent)
#        self.window.title(title)
#        self.parent = parent
#
#        self.label = tk.Label(self.window, text=label).pack()
#
#        self.spinbox = tk.Spinbox(self.window, from_=0, increment=0.1)
#        self.spinbox.pack(padx=5)
#
#        self.submitButton = tk.Button(self.window, text="OK", command=self.submit)
#        self.submitButton.pack(pady=5)
#        self.value = 0
#
#    def getInput(self):
#        self.parent.wait_window(self.window)
#        return self.value
#
#    def submit(self):
#        try:
#            self.value = float(self.spinbox.get())
#            self.window.destroy()
#        except TypeError:
#            self.label.configure(bg="red", text="Must be a number!")



root = tk.Tk()

app = App(root)
app.root.title("Geiger Counter Analysis")

root.mainloop()
