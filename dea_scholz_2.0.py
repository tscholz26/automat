"""@package docstring
Documentation for this module.

More details.
"""

from tkinter import *
import math, time
master = Tk()
master.title("Simulation DEA")

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
    alphabet: zum erreichen der entsprechenden folgezstände nötige alphabetelemente
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
        global current
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
            print("final state reached")
        else:
            print("final state not reached")

            
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
            labelfinal["text"] = "FINAL STATE"
        else:
            labelfinal["text"] = "no final state"
        global avouts
        avouts = []
        for avout in self.__outcomes:
            if not (avout in avouts):
                avouts.append(avout)
        n = len(avouts)
        print(avouts)
        print("zu zeichnende kreise: " + str(n))
        global r
        current.setx(300)
        current.sety(100)
        canvas1.create_oval(current.x()-r,current.y()-r,current.x()+r,current.y()+r)
        if current.final():
            canvas1.create_oval(300-r+5,100-r+5,300+r-5,100+r-5)
        canvas1.create_text(current.x(), current.y(), text = current.name())
        i = 0
        for name in avouts:
            if n == 1:
                zst(name).setx(100)
            else:
                zst(name).setx(100 + 600/(n-1)*i)
            i = i + 1
            zst(name).sety(500)
            canvas1.create_oval(zst(name).x()-r, zst(name).y()-r, zst(name).x()+r, zst(name).y()+r)
            canvas1.create_text(zst(name).x(), zst(name).y(), text = name)
            if zst(name).final() == 1:
                print(name + " ist zielzustand")
                canvas1.create_oval(zst(name).x()-r+5, zst(name).y()-r+5, zst(name).x()+r-5, zst(name).y()+r-5)
            #pfeillinie
            dx = 300 - zst(name).x()
            dy = 100 - zst(name).y()
            print("dx|dy = " + str(dx) + "|" + str(dy))
            sx = dx * math.sqrt(r*r/(dx*dx+dy*dy))
            sy = dy * math.sqrt(r*r/(dx*dx+dy*dy))
            xstart = 300 - sx
            ystart = 100 - sy
            xend = zst(name).x() + sx
            yend = zst(name).y() + sy
            uy = 10
            ux = uy*dx/dy
            xm = (xstart + xend)/2
            ym = (ystart + yend)/2
            canvas1.create_line(xstart,ystart,(xstart+xend)/2-ux, (ystart+yend)/2-uy)
            canvas1.create_line((xstart+xend)/2+ux, (ystart+yend)/2+uy, xend, yend)
            enumeration = ""
            for item in current.getalphabet():
                if current.getoutcomes()[current.getalphabet().index(item)] == name:
                    print("item found")
                    if enumeration == "":
                        enumeration = item
                    else:
                        enumeration = enumeration + "," + item
            canvas1.create_text(xm, ym, text = enumeration)
            #beschriftung, spitze



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
    print("clicked on: " + str(clickx) + " | " + str(clicky))

def release(eventclick):
    global clickx
    global clicky
    global relx
    global rely
    global r
    relx = eventclick.x
    rely = eventclick.y
    print("released on: " + str(relx) + " | " + str(rely))

    global avouts
    for state in avouts:
        print("überprüfung")
        if clickx > zst(state).x()-r:
            if clickx < zst(state).x()+r:
                if clicky > zst(state).y()-r:
                    if clicky < zst(state).y()+r:
                        print(zst(state).name() + " was clicked at")
                        current.setcurrent(zst(state))
                        
    

        
"""Test DEA:
q_0 = State("q_0", ["q_0", "q_1", "q_3"], ["a","1","3"],  0)
q_1 = State("q_1", ["q_1", "q_2"], ["1","2"], 100, 100, 0)
q_2 = State("q_2", ["q_0"], ["f"], 100, 100, 0)
q_3 = State("q_3", ["q_1", "q_2", "q_3"], ["1","2","3"], 100, 100, 1)
statelist = [q_0, q_1, q_2, q_3]
startval = q_0
"""

#Eingabe des DEAS
q_2 = State("q_2", ["q_05"], ["0"], 100, 100, 0)
q_05 = State("q_05", ["q_0", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013"], ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], 100, 100, 1)
q_0 = State("q_0", ["q_0", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013"], ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], 100, 100, 0)
q_013 = State("q_013", ["q_0", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_4", "q_4"], ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "-"], 100, 100, 1)              
q_4 = State("q_4", [], [], 100, 100, 1)
statelist = [q_2, q_05, q_0, q_013, q_4]
global startval
startval = q_2

label1 = Label(master, text = "alphabet item to use: ")
label1.grid(row = 0, column = 0, pady = 15)

entryitem = Entry(master)
entryitem.grid(row = 0, column = 1)

buttonuse = Button(master, text = "use", command = lambda:(current.use(entryitem.get())))
buttonuse.grid(row = 0, column = 2)

buttonreset = Button(master, text = "reset", command = initdea)
buttonreset.grid(row = 0, column = 3)

labelfinal = Label(master, text = "XXXXXX")
labelfinal.grid(row = 0, column = 4)

canvas1 = Canvas(master, width = 800, height = 600)
canvas1.grid(row = 1, column = 0, columnspan = 5)
canvas1.bind("<Button-1>", click)
canvas1.bind("<ButtonRelease-1>", release)


#Initialisierung des Startzustandes
initdea()




    

    






