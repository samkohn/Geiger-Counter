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
            ("Import Saved Data", self.importBinary),
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
        self.dataSet = ad.DataSet.fromFile(filename)
        print "imported"

    def getCountRate(self):
        if self.dataSet:
            #prompt for desired bin spacing
            binSpacing = 2
            self.dataSet.getCountRate(binSpacing)
            #do something with the results

        else:
            #say that you need to import data first
            pass


    def getIntervals(self):
        pass
    def getTotalCounts(self):
        pass


root = tk.Tk()

app = App(root)

root.mainloop()
