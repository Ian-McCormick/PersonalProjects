import math
from tkinter import *

class planet:
    def __init__(self, radius, atm, grav):
        self.radius = radius
        self.atm = atm
        self.gc = grav
        
    def set_alt(self, alt, sats):
        if(alt <= self.atm):
            return (-1)
        Tf = 2*math.pi * math.sqrt(((alt+self.radius)**3)/self.gc)
        Ti = ((sats+1)/sats)*Tf
        
        num = self.gc*(Ti**2)
        den = 4*(math.pi**2)
        ai = (num/den)**(1/3)
        Pe = 2*ai-Ap
        return()
       
def load_planets():
    planets = {}
    f = open("Planets.txt","r")
    lines = f.readlines()
    for line in lines:
        line = line.rstrip()
        data = line.split(", ")
        planets[data[0]] = planet(int(data[1]), int(data[2]), float(data[3]))
    return planets

def useMinAlt(mini, entry):
    if mini.get() == 1:
        entry.configure(state = "disabled")
    else:
        entry.configure(state = "normal")

def validate(sats, alt, output):
    error = ""
    valid = True
    try:
        int(sats)
    except:
        valid = False
        error += "Number of satellites has invalid character\n"
    else:
        if int(sats) < 3:
            valid = False
            error += "Number of satellites cannot be less than 3\n"
    try:
        int(alt)
    except:
        valid = False
        error += "Altitude contains invalid character"
    output.config(text = error)
    output.grid(row = 5, column = 1)
    return valid

def calculate(root, planet, sats, mini, alt, output):
    printOut = ""
    output.config(text = "")
    if(not validate(sats, alt, output)):
        return False
    sats = int(sats)
    alt = int(alt)
    
    if(mini == 1):
        theta = ((sats-2)*180)/sats
        Pe = (planet.radius)/ math.sin(math.radians(theta)/2)
    else:
        Pe = planet.radius + alt

    if(Pe <= planet.radius + planet.atm):
        printOut = "final orbit below atmosphere/highest point\nsetting orbit to atmosphere/highest point + 5000m\n"
        Pe = planet.radius+ planet.atm+ 5000
    
    Tf = 2*math.pi * math.sqrt((Pe**3)/planet.gc)
    Ti = ((sats+1)/sats)*Tf
    num = planet.gc*(Ti**2)
    den = 4*(math.pi**2)
    ai = (num/den)**(1/3)
    Ap = 2*ai-Pe

    printOut += "Periapsis: "+ str(round(Pe-planet.radius)) + " Meters\nApoapsis: "+ str(round(Ap-planet.radius)) + " Meters\nCircularize at periapsis"
    output.config(text = output.cget("text") + printOut)
    return True
    
    
def main():
    planets = load_planets()
    root = Tk()
    root.title("KSP Resonant Orbit Calculator")
    
    Label(root, text = "Select the planet: ", anchor = "w").grid(row = 0, column = 0)
    Label(root, text = "Enter desired number of satellites: ", anchor = "w").grid(row = 1, column = 0)
    Label(root, text = "Use Minimum Altitude?", anchor = "w").grid(row = 2, column = 0)
    Label(root, text = "Enter the orbit altitude: ", anchor = "w").grid(row = 3, column = 0)

    sel_planet = StringVar(root)
    sel_planet.set("Moho")
    OptionMenu(root, sel_planet, *planets.keys()).grid(row = 0, column = 1)

    num_sats = StringVar()
    num_sats.set("3")
    Entry(root, textvariable = num_sats).grid(row = 1, column = 1)

    mini = IntVar()
    mini.set(1)
    Checkbutton(root, variable = mini, command=lambda:useMinAlt(mini, ent_alt)).grid(row = 2, column = 1)

    alt = StringVar()
    alt.set("100000")
    ent_alt = Entry(root, textvariable = alt, state = "disabled")
    ent_alt.grid(row = 3, column = 1)

    Button(root, text = "calculate orbit",command= lambda:
           calculate(root, planets[sel_planet.get()], num_sats.get(), mini.get(), alt.get(), output)).grid(row = 5, column = 0)
    
    output = Label(root)
    root.mainloop()
main()
