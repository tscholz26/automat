"""@package docstring
Documentation for this module.

More details.
"""

vers = "2.1"

from tkinter import *
import math, time
master = Tk()
master.title("Simulation DEA (v" + vers + ")")

global prev
global current
global r
r = 30

global clickx
global clicky
global relx
global rely

class State():
    """
    Diese Klasse beschreibt zstände
    outcomes: verschiedene folgezstände in bestimmter reihenfolge
    alphabet: zum erreichen der entsprechenden folgezustände nötige alphabetelemente
    """
    def __init__(self, name = str, outcomes = [], alphabet = [], x = float, y = float, final = bool):
        self.__name = name
        self.__outcomes = outcomes
        self.__alphabet = alphabet
        self.__x = x
        self.__y = y
        self.__final = final

    def name(self):
        """Diese Methode dient dazu, den Namen des zstands zurückzugeben.
        """
        return(self.__name)

    def setcurrent(self,newstate):
        global prev
        global current
        prev = current
        current = newstate
        print("--------------------------------------------------")
        print("new state has been set")
        current.showstate()
        

    def showstate(self):
        print("name: " + self.__name)
        current.draw()
        if len(self.__outcomes) > 0:
            print("outcomes: ")
            for i in range (0,len(self.__outcomes)):
                print(str(self.__alphabet[i]) + " --> " + self.__outcomes[i])
        else:
            print("possible outcomes: none")
        if self.__final:
            print("FINAL STATE")
        else:
            print("no final state")

            
    def getoutcomes(self):
        return(self.__outcomes)

    def getalphabet(self):
        return(self.__alphabet)

    def setx(self,x):
        self.__x = x

    def sety(self,y):
        self.__y = y

    def x(self):
        return(self.__x)

    def y(self):
        return(self.__y)

    def final(self):
        return(self.__final)

    def use(self, item):
        global current
        if item in self.__alphabet:
            current.setcurrent(zst(self.__outcomes[self.__alphabet.index(item)]))
        else:
            print("item unavailable")

    def draw(self):
        canvas1.delete(ALL)
        if current.final():
            labelfinal["text"] = "ZIELZUSTAND"
            labelfinal["font"] = "bold"
        else:
            labelfinal["text"] = "kein Zielzustand"
        global avouts
        avouts = []
        for avout in self.__outcomes:
            if not (avout in avouts):
                avouts.append(avout)
        n = len(avouts)
        global r
        #vorheriges zeichnen
        if not prev.name() == "prev":
            print("vorheriges zeichnen: ")            
            canvas1.create_oval(75-r,75-r,75+r,75+r, outline = "#a9a9a9")
            canvas1.create_line(75+r,75,225-r,75, dash =(4,3), fill = "#a9a9a9")
            canvas1.create_polygon(225-r,75,225-r-12,71,225-r-12,79, fill = "#a9a9a9")
            canvas1.create_text(75,75, text = prev.name(), fill = "#a9a9a9")
        #aktuelles zeichnen
        current.setx(225)
        current.sety(75)
        canvas1.create_oval(current.x()-r,current.y()-r,current.x()+r,current.y()+r)
        if current.final():
            canvas1.create_oval(225-r+5,75-r+5,225+r-5,75+r-5)
        canvas1.create_text(current.x(), current.y(), text = current.name())
        #mögliche neue zustände
        i = 0
        for name in avouts:
            if n == 1:
                zst(name).setx(75)
            else:
                zst(name).setx(75 + 450/(n-1)*i)
            i = i + 1
            zst(name).sety(375)
            canvas1.create_oval(zst(name).x()-r, zst(name).y()-r, zst(name).x()+r, zst(name).y()+r)
            canvas1.create_text(zst(name).x(), zst(name).y(), text = name)
            if zst(name).final() == 1:
                canvas1.create_oval(zst(name).x()-r+5, zst(name).y()-r+5, zst(name).x()+r-5, zst(name).y()+r-5)
            #pfeillinie
            dx = 225 - zst(name).x()
            dy = 75 - zst(name).y()
            sx = dx * math.sqrt(r*r/(dx*dx+dy*dy))
            sy = dy * math.sqrt(r*r/(dx*dx+dy*dy))
            xstart = 225 - sx
            ystart = 75 - sy
            xend = zst(name).x() + sx
            yend = zst(name).y() + sy
            uy = 10
            ux = uy*dx/dy
            xm = (xstart + xend)/2
            ym = (ystart + yend)/2
            canvas1.create_line(xstart,ystart,(xstart+xend)/2-ux, (ystart+yend)/2-uy)
            canvas1.create_line((xstart+xend)/2+ux, (ystart+yend)/2+uy, xend, yend)
            #beschriftung
            enumeration = ""
            for item in current.getalphabet():
                if current.getoutcomes()[current.getalphabet().index(item)] == name:
                    if enumeration == "":
                        enumeration = item
                    else:
                        enumeration = enumeration + "," + item
            canvas1.create_text(xm, ym, text = enumeration)
            #spitze
            k1 = 0.04
            k2 = 0.013
            xsp1 = xend + k1*dx - k2 * dy
            ysp1 = yend + k1*dy + k2 * dx
            xsp2 = xend + k1*dx + k2 * dy
            ysp2 = yend + k1*dy - k2 * dx
            canvas1.create_polygon(xend,yend,xsp1,ysp1,xsp2,ysp2)


#Startwert definieren und anzeigen
def initdea():
    global current
    global startval
    current = startval
    print("Starting state has been set")
    current.showstate()

def zst(name):
    """sucht zst mit name "name" heraus, vergleichar mit str(int)
    """
    for state in statelist:
        if name == state.name():
            result = state
    return(result)



def click(eventclick):
    """Diese Methode setzt die Variable mousedown, die zeigt, ob die Maus gerade
    gehalten wird, auf 1 und ändert currentx und currenty auf die Koordinaten des
    Punktes, der angeklickt wurde.

    Args:
        eventlick: vom System angelegt, enthält u.A. x/y Koordinaten des Punkts
    """
    global clickx
    global clicky
    clickx = eventclick.x
    clicky = eventclick.y

def release(eventclick):
    global clickx
    global clicky
    global relx
    global rely
    global r
    relx = eventclick.x
    rely = eventclick.y

    global avouts
    for state in avouts:
        if clickx > zst(state).x()-r:
            if clickx < zst(state).x()+r:
                if clicky > zst(state).y()-r:
                    if clicky < zst(state).y()+r:
                        print(zst(state).name() + " was clicked at")
                        current.setcurrent(zst(state))

def helpwindow():
    popup = Tk()
    popup.title("Hilfe")
    msg = ("Oben links finden Sie in hellgrau den vorhergehenden\nZustand und oben rechts den aktuellen Zustand.\nUnten sind die möglichen Zielzustände aufgelistet.\nSie können entweder die Zielzustände anklicken,\noder Sie geben das passende Alphabetelement oben\nin das Entry ein und bestätigen. Mit dem reset-Button\nkönnen Sie zum Startzustand zurückkehren.")
    labelmsg = Label(popup, text = msg, justify = 'left', font = '15')
    labelmsg.pack(padx = 10, pady = 10)
                        
    


#Eingabe des DEAS
q_2 = State("q_2", ["q_05"], ["0"], 100, 100, 0)
q_05 = State("q_05", ["q_0", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013"], ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], 100, 100, 1)
q_0 = State("q_0", ["q_0", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013"], ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], 100, 100, 0)
q_013 = State("q_013", ["q_0", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_4", "q_4"], ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "-"], 100, 100, 1)              
q_4 = State("q_4", [], [], 100, 100, 1)
prev = State("prev", [], [], 100, 100, 1)
statelist = [q_2, q_05, q_0, q_013, q_4]
global startval
startval = q_2

label1 = Label(master, text = "Alphabetelement: ")
label1.grid(row = 0, column = 0, pady = 15)

entryitem = Entry(master)
entryitem.grid(row = 0, column = 1)

buttonuse = Button(master, text = "Anwenden", command = lambda:(current.use(entryitem.get())))
buttonuse.grid(row = 0, column = 2)

buttonreset = Button(master, text = "Zurücksetzen", command = initdea)
buttonreset.grid(row = 0, column = 3)

buttonhelp = Button(master, text = " ? ", command = helpwindow)
buttonhelp.grid(row = 0, column = 4)

labelfinal = Label(master, text = "XXXXXX")
labelfinal.grid(row = 0, column = 5)

canvas1 = Canvas(master, width = 600, height = 450)
canvas1.grid(row = 1, column = 0, columnspan = 6)
canvas1.bind("<Button-1>", click)
canvas1.bind("<ButtonRelease-1>", release)


#Initialisierung des Startzustandes
initdea()




    

    






