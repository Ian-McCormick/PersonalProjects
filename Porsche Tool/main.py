import tkinter as tk
from PIL import Image, ImageTk
import json

#our data classes
class Problem:
    def __init__(self, name, desc, sev, PS, AS):
        self.name = name
        self.description = desc
        self.severity = sev
        self.possibleSolutions = PS
        self.attemptedSolutions = AS

class Solution:
    def __init__(self, name, parts):
        self.name = name
        self.parts = parts

class Part:
    def __init__(self, name, brand, no, cost, origin):
        self.name = name
        self.brand = brand
        self.no = no
        self.cost = cost
        self.origin = origin

class Invoice:
    def __init__(self, store, date, cost, parts):
        self.store =store
        self.date = date
        self.cost = cost
        self.parts = parts

#loads all previously saved problems
def loadProblems():
    try:
        problemData = json.load(open("problems.JSON"))
        outputProblems = []
        for problem in problemData["problems"]:
            name = problem["name"]
            desc = problem["description"]
            sev = int(problem["severity"])
            PS = loadSolutions(problem["possibleSolutions"])
            AS = loadSolutions(problem["attemptedSolutions"])
            outputProblems.append(Problem(name, desc, sev, PS, AS))
        return outputProblems
    except:
        return []

def loadSolutions(solutionList):
    solutions = []
    for sol in solutionList:
        sname = sol["name"]
        sparts = loadParts(sol["parts"])
        solutions.append(Solution(sname, sparts))
    return solutions

def loadParts(partList):
    parts = []
    for part in partList:
        pname = part["name"]
        pbrand = part["brand"]
        pno = part["no"]
        pcost = float(part["cost"])
        porigin = part["origin"]
        parts.append(Part(pname, pbrand, pno, pcost, porigin))
    return parts

def loadInvoices():
    try:
        invoiceData = json.load(open("invoices.JSON"))
        outputInvoices = []
        for invoice in invoiceData["invoices"]:
            store = invoice["store"]
            date = invoice["date"]
            cost = float(invoice["cost"])
            parts = loadParts(invoice["parts"])
            outputInvoices.append(Invoice(store, date, cost, parts))
    except:
        return []

#color codes for severity, from green to red
def getColor(severity):
    if severity == 5:
        return "#FF0000"
    elif severity == 4:
        return "#FF4500"
    elif severity == 3:
        return "#9ACD32"
    elif severity == 2:
        return "#32CD32"
    elif severity == 1:
        return "#00FF00"
    else:
        return "#FFFFFF"

#used to display and edit details of a particular problem
def displayProblem(problem, topLevel):
    top = tk.Toplevel(topLevel)
    top.grab_set()
    top.geometry("720x720")
    top.title(problem.name)
    tk.Label(top, text=problem.description).grid(row=0, column=0)

def createProblem(problems, topLevel, parentRow):
    WIDTH = 25
    SEVERITY_OPTIONS = [1,2,3,4,5]
    top = tk.Toplevel(topLevel)
    top.grab_set()
    top.geometry("720x720")
    top.title("Create Problem")
    curRow = 0

    possibleSolutions = []
    attemptedSolutions = []

    #get name
    tk.Label(top, text="Name:").grid(row=curRow, column=0)
    nameEntry = tk.Entry(top, width=WIDTH + 8)
    nameEntry.grid(row=curRow, column=1)
    curRow += 1

    #get description
    tk.Label(top, text="Description:").grid(row=curRow, column=0)
    descEntry = tk.Text(top, height=4, width=WIDTH)
    descEntry.grid(row=curRow, column=1)
    curRow += 1

    #get severity
    tk.Label(top, text="Severity:").grid(row=curRow, column=0)
    sevEntry = tk.StringVar()
    sevEntry.set(1) 
    tk.OptionMenu(top, sevEntry, *SEVERITY_OPTIONS).grid(row=curRow, column=1)
    curRow += 1

    #generate initial solutions
    tk.Label(top, text="Add possible solution:").grid(row=curRow, column=0)
    PSListBox = tk.Listbox(top)
    PSListBox.grid(row=curRow, column=1)
    for sol in possibleSolutions:
        PSListBox.insert(tk.END, sol.name)
    tk.Button(top, text="Create Solution", command=lambda: createSolution(possibleSolutions, PSListBox, top)).grid(row=curRow, column= 2)
    tk.Button(top, text="Remove Solution", command=lambda: removeSolution(top, possibleSolutions, PSListBox)).grid(row=curRow, column= 3)
    curRow += 1

    #if anything has been tried yet
    tk.Label(top, text="Add possible solution:").grid(row=curRow, column=0)
    ASListBox = tk.Listbox(top)
    ASListBox.grid(row=curRow, column=1)
    for sol in attemptedSolutions:
        ASListBox.insert(tk.END, sol.name)
    tk.Button(top, text="Create Solution", command=lambda: createSolution(attemptedSolutions,ASListBox, top)).grid(row=curRow, column= 2)
    tk.Button(top, text="Remove Solution", command=lambda: removeSolution(top, attemptedSolutions,ASListBox)).grid(row=curRow, column= 3)
    curRow += 1

    #create the problem
    tk.Button(top, text="Add Problem", command=lambda:updateProblemList(topLevel, top, parentRow, problems, nameEntry.get(),descEntry.get("1.0", tk.END), 
                                                                        int(sevEntry.get()), possibleSolutions, attemptedSolutions)).grid(row=curRow, column=0)
    curRow += 1

def updateProblemList(parent, child, curRow, problems, name, desc, sev, PS, AS):
    newProblem = Problem(name, desc, sev, PS, AS)
    problems.append(newProblem)
    parent.update()
    drawProblemList(parent, curRow, problems)
    child.destroy()

def createSolution(solutions, listBox, topLevel):
    WIDTH = 25
    top = tk.Toplevel(topLevel)
    top.grab_set()
    top.geometry("720x720")
    top.title("Create Solution")
    curRow = 0

    tk.Label(top, text="Name:").grid(row=curRow, column=0)
    nameEntry = tk.Entry(top, width=WIDTH + 8)
    nameEntry.grid(row=curRow, column=1)
    curRow += 1

    parts = []
    partListBox = tk.Listbox(top)
    partListBox.grid(row=curRow, column=1)
    for part in parts:
        partListBox.insert(tk.END, part.name)
    tk.Button(top, text="Create Part", command=lambda: createPart(top, partListBox, parts)).grid(row=curRow, column= 2)
    tk.Button(top, text="Remove Part", command=lambda: removePart(top, parts, partListBox)).grid(row=curRow, column=3)
    curRow += 1

    tk.Button(top, text="Add Solution", command=lambda:createSolutionObject(topLevel, top, solutions, listBox, nameEntry.get(), parts)).grid(row=curRow, column=0)

def createSolutionObject(parent, child, solutions, listBox, name, parts):
    if not name.strip() == "":
        newSolution = Solution(name, parts)
        solutions.append(newSolution)
        listBox.insert(tk.END, newSolution.name)
    parent.update()
    child.destroy()

def removeSolution(parent, solutions, solutionsBox):
    sel = solutionsBox.get(solutionsBox.curselection())
    for sol in solutions:
        if sol.name == sel:
            solutions.remove(sol)
    index = solutionsBox.get(0, tk.END).index(sel)
    solutionsBox.delete(index)
    parent.update()

def createPart(topLevel, partsBox, parts):
    WIDTH = 25
    top = tk.Toplevel(topLevel)
    top.grab_set()
    top.geometry("720x720")
    top.title("Create Part")
    curRow = 0

    tk.Label(top, text="Name:").grid(row=curRow, column=0)
    nameEntry = tk.Entry(top, width=WIDTH + 8)
    nameEntry.grid(row=curRow, column=1)
    curRow += 1

    tk.Label(top, text="Brand:").grid(row=curRow, column=0)
    brandEntry = tk.Entry(top, width=WIDTH + 8)
    brandEntry.grid(row=curRow, column=1)
    curRow += 1

    tk.Label(top, text="Part Number:").grid(row=curRow, column=0)
    numEntry = tk.Entry(top, width=WIDTH + 8)
    numEntry.grid(row=curRow, column=1)
    curRow += 1

    tk.Label(top, text="Cost:").grid(row=curRow, column=0)
    costEntry = tk.Entry(top, width=WIDTH + 8)
    costEntry.grid(row=curRow, column=1)
    curRow += 1

    tk.Label(top, text="Origin:").grid(row=curRow, column=0)
    originEntry = tk.Entry(top, width=WIDTH + 8)
    originEntry.grid(row=curRow, column=1)
    curRow += 1

    tk.Button(top, text="Add Part", command=lambda:createPartObject(topLevel, top, parts, partsBox, nameEntry.get(), brandEntry.get(), numEntry.get(),
                                                                            costEntry.get(), originEntry.get(), curRow)).grid(row=curRow, column=0)

def createPartObject(parent, child, parts, partsBox, name, 
                     brand,partNo, costStr, origin, curRow):
    try:
        cost = float(costStr)
    except:
        tk.Label(child, text="Cost must be a number", fg="#ff0000").grid(row=curRow+1, column=0)
        return
    if not name.strip() == "":
        parts.append(Part(name, brand, partNo, cost, origin))
        partsBox.insert(tk.END, name)
    parent.update()
    child.destroy()

def removePart(parent, parts, partsBox):
    sel = partsBox.get(partsBox.curselection())
    for part in parts:
        if part.name == sel:
            parts.remove(part)
    index =partsBox.get(0, tk.END).index(sel)
    partsBox.delete(index)
    parent.update()

def drawProblemList(window, curRow, problems):
    tempRow = curRow
    for problem in problems:
        boxColor = getColor(problem.severity)
        tk.Button(window, text=problem.name, bg=boxColor, command=lambda: displayProblem(problem, window)).grid(row=curRow, column=0)
        tk.Button(window, text="DELETE", command=lambda: None).grid(row=curRow, column=1)
        curRow += 1

def createInvoice(parent, invoices, parentRow):
    child = tk.Toplevel(parent)
    child.grab_set()
    child.geometry("720x720")
    child.title("Create Invoice")

    curRow = 0
    tk.Label(child, text= "Store: ").grid(row=curRow, column= 0)
    storeEntry = tk.Entry(child)
    storeEntry.grid(row=curRow, column=1)
    curRow += 1

    tk.Label(child, text="date: ").grid(row=curRow, column=0)
    dateEntry = tk.Entry(child)
    dateEntry.grid(row=curRow, column=1)
    curRow += 1

    tk.Label(child, text="cost: ").grid(row=curRow, column=0)
    costEntry = tk.Entry(child)
    costEntry.grid(row=curRow, column=1)
    curRow += 1

    parts = []
    partListBox = tk.Listbox(child)
    partListBox.grid(row=curRow, column=1)
    tk.Button(child, text="Create Part", command=lambda: createPart(child, partListBox, parts)).grid(row=curRow, column= 2)
    tk.Button(child, text="Remove Part", command=lambda: removePart(child, parts, partListBox)).grid(row=curRow, column=3)
    curRow += 1

    tk.Button(child, text="Create Invoice", command=lambda: createInvoiceObject(parent, child, invoices, parentRow, storeEntry.get(), dateEntry.get(),
                                                                                costEntry.get(), parts)).grid(row=curRow, column= 0)

def createInvoiceObject(parent, child, invoices, displayRow, store, date, cost, parts):
    if not store.strip() == "":
        newInvoice = Invoice(store, date, cost, parts)
        invoices.append(newInvoice)

    parent.update()
    updateInvoiceList(parent, displayRow, invoices)
    child.destroy()

def updateInvoiceList(parent, parentRow, invoices):
    temp = parentRow
    for invoice in invoices:
        tk.Label(parent, text=invoice.store).grid(row = parentRow, column=0)
        tk.Label(parent, text=invoice.date).grid(row = parentRow, column=1)
        tk.Label(parent, text=invoice.cost).grid(row = parentRow, column=2)
        
        temp += 1

def viewInvoices(parent, invoices):
    child = tk.Toplevel(parent)
    child.grab_set()
    child.geometry("720x720")
    child.title("Invoices")

    curRow = 2
    tk.Label(child, text="Store").grid(row = 1, column=0)
    tk.Label(child, text="Date").grid(row = 1, column=1)
    tk.Label(child, text="Cost").grid(row = 1, column=2)
    tk.Button(child, text="Create Invoice", command=lambda: createInvoice(child, invoices, curRow)).grid(row=0, column=0)

def main():
    baseInfo = json.load(open("mainInfo.JSON"))
    mainWindow = tk.Tk()
    mainWindow.geometry("720x720")
    mainWindow.title("Porsche Maintenence Tracker")
    
    photo = ImageTk.PhotoImage(Image.open("Porsche-Logo.png"))
    mainWindow.wm_iconphoto(True, photo)
    problems = loadProblems()
    invoices = loadInvoices()

    tk.Label(mainWindow, text=baseInfo["Car YMM"], height=2).grid(row=1, column=0)
    tk.Label(mainWindow, text=baseInfo["VIN"], height=2).grid(row=2, column=0)
    tk.Label(mainWindow, text="$" + baseInfo["Cost"], height=2).grid(row=3, column=0)
    tk.Button(mainWindow, text="View Invoices", command=lambda:viewInvoices(mainWindow, invoices)).grid(row=3, column=1)
    tk.Label(mainWindow, height=3).grid(row=4, column=0)

    tk.Label(mainWindow, text="PROBLEMS").grid(row=5, column=0)
    tk.Button(mainWindow, text="Create problem", command=lambda: createProblem(problems, mainWindow, curRow)).grid(row=5, column=1)
    curRow = 6
    drawProblemList(mainWindow, curRow, problems)

    mainWindow.mainloop()

main()

exampleProblem = {
    "name": "misfire",
    "description": "An intermittent misfire",
    "severity": "5",
    "possibleSolutions": [{
        "name": "replace injectors",
        "parts":[{
            "name":"Fuel Injectors",
            "brand": "Bosch",
            "no": "10399U255",
            "cost": "84.50",
            "origin": "fiveOmotorsport"
        }]
    }],
    "attemptedSolutions":[{
        "name": "replace spark parts",
        "parts": [{
            "name":"Spark Plugs",
            "brand": "NGK",
            "no": "UNKNOWN",
            "cost": "0.00",
            "origin": "UNKNOWN"
        },
        {
            "name":"Spark Wires",
            "brand": "NGK",
            "no": "UNKNOWN",
            "cost": "0.00",
            "origin": "UNKNOWN"
        }]
    }]
}

#problems = {"problems": [exampleProblem]}
#with open("problems.json", "w") as OF:
#    OF.write(json.dumps(problems, indent=4))