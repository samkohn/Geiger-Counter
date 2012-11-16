'''A GUI program to analyze data from the geiger counter experiment'''

# The GUI package for python
import Tkinter as tk
import tkFileDialog as tkfd

# Our analysis tools
import analyzeData as ad

class App:

    def __init__(self, master):
        
        self.root = master
        frame = tk.Frame(self.root)
        frame.pack()

        self.quitButton = tk.Button(frame, text="Quit", fg="red", command=frame.quit)
        self.quitButton.pack(side=tk.LEFT)

        self.hiButton = tk.Button(frame, text="Say Hi!", command=self.sayHi)
        self.hiButton.pack(side=tk.LEFT)

        buttonFrame = tk.Frame(frame)
        self.addMenuButtons(frame)
        buttonFrame.pack(side=tk.LEFT)

        self.dataSet = None

    def sayHi(self):
        print "Hello, World!"

    def addMenuButtons(self, master):
        buttons = [
            ("Import .wav File", self.importWavFile),
            ("Import Saved Data", self.openBinary),
            ("Save Data to Disk", self.saveBinary),
            ("Get Count Rate", self.getCountRate),
            ("Get Intervals", self.getIntervals),
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

    def getCountRate(self):
        if self.dataSet:
            #prompt for desired bin spacing

            #inputDialog = tk.TopLevel(self.root, title="Count Rate")
            labelText = "Enter the desired sample length in seconds"
            #tk.Label(inputDialog, text=labelText).pack()
            #submitButton = tk.Button(inputDialog, text="OK", command=

            dialog = InputDialog(self.root, "Count Rate", labelText)
            binSpacing = dialog.getInput()
            

            print str(self.dataSet.getCountRate(binSpacing))
            #do something with the results
            

        else:
            #say that you need to import data first
            pass


    def getIntervals(self):
        if self.dataSet:
            print self.dataSet.getInterval()
        else:
            pass

    def getTotalCounts(self):
        if self.dataSet:
            print self.dataSet.getTotalCounts()

        else:
            # That same need to import data
            pass




    def saveBinary(self):
        if self.dataSet:
            filename = tkfd.asksaveasfilename(initialdir=".", title="Save Data")
            self.dataSet.save(filename)
            print "saved"
        else:
            #say that you need to import data first
            pass


    def openBinary(self):
        filename = tkfd.askopenfilename(initialdir=".", title="Open File")
        self.dataSet = ad.DataSet.fromSavedFile(filename)
        print "opened"




class InputDialog:
    def __init__ (self, parent, title, label):
        
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.parent = parent

        self.label = tk.Label(self.window, text=label).pack()

        self.spinbox = tk.Spinbox(self.window, from_=0, increment=0.1)
        self.spinbox.pack(padx=5)

        self.submitButton = tk.Button(self.window, text="OK", command=self.submit)
        self.submitButton.pack(pady=5)
        self.value = 0

    def getInput(self):
        self.parent.wait_window(self.window)
        return self.value

    def submit(self):
        try:
            self.value = float(self.spinbox.get())
            self.window.destroy()
        except TypeError:
            self.label.configure(bg="red", text="Must be a number!")



root = tk.Tk()

app = App(root)

root.mainloop()
