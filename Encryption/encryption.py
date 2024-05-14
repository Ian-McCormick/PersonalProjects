import tkinter as tk
from tkinter import filedialog
import os

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Main:
    def __init__(self):
        self.root = tk.Tk()
        #create labels
        tk.Label(self.root, text="Password: ").grid(row=0, column=0)
        tk.Label(self.root, text="File for decryption: ").grid(row=1, column=0)

        #create entries
        self.password = tk.Entry(self.root)
        self.password.grid(row=0, column=1)

        self.fullFileName = ""
        self.fileToView = tk.Label(self.root, text="")
        fileButton = tk.Button(self.root, text = "Select File", command = lambda: self.changeFileToView())
        fileButton.grid(row=1, column=2)

        #create execution buttons
        tk.Button(self.root, text="Add Entry", command= lambda: self.addEntry()).grid(row=2, column=0)
        tk.Button(self.root, text="Decrypt Entry", command= lambda: self.decryptEntry()).grid(row=2, column=1)
        self.root.mainloop()

    def changeFileToView(self):
        self.fullFileName = filedialog.askopenfilename(initialdir=CURRENT_DIRECTORY,
                    title="Select Battle Map")
        
        self.fileToView.config(text = self.fullFileName.split("/")[-1])
        self.root.update()

    def addEntry(self):
        return
    
    def decryptEntry(self):
        return

Main()