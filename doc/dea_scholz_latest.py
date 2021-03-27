"""@package docstring
Documentation for this module.

More details.
"""

vers = "2.2.2"

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
    Diese Klasse beschreibt Zustände
    Member-Variablen:
        outcomes: mögliche Folgezustände in bestimmter Reihenfolge
        alphabet: zum Erreichen der entsprechenden Folgezustände nötige Alphabetelemente
        x: x-Koordinate (später in der GUI nötig)
        y: y-Koordinate (später in der GUI nötig)
        final: Wahrheitswert, gibt an, ob der Zustand ein Finalzustand ist
    """
    def __init__(self, name = str, outcomes = [], alphabet = [], x = float, y = float, final = bool):
        self.__name = name
        self.__outcomes = outcomes
        self.__alphabet = alphabet
        self.__x = x
        self.__y = y
        self.__final = final

    def name(self):
        """Diese Methode dient dazu, den Namen des Zustands zurückzugeben.
        """
        return(self.__name)

    def setcurrent(self,newstate):
        """Diese Methode stellt einen neuen Zustand ein. Dabei wird der alte Zustand
        gespeichert und die Variable current (aktueller Zustand) wird zur Variable
        newstate (beide Typ State).
        """
        global prev
        global current
        prev = current
        current = newstate
        print("--------------------------------------------------")
        print("new state has been set")
        current.showstate()
        

    def showstate(self):
        """Diese Methode gibt Details zum aktuellen Zustand aus
        """
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
        """Diese Methode gibt die möglichen Folgezustände zurück
        """
        return(self.__outcomes)

    def getalphabet(self):
        """Diese Methode legt eine neue x-Koordinate fest
        """
        return(self.__alphabet)

    def setx(self,x):
        """Diese Methode legt eine neue y-Koordinate fest
        """
        self.__x = x

    def sety(self,y):
        
        self.__y = y

    def x(self):
        """Diese Methode gibt die x-Koordinate zurück
        """
        return(self.__x)

    def y(self):
        """Diese Methode gibt die y-Koordinate zurück
        """
        return(self.__y)

    def final(self):
        """Diese Methode gibt zurück, ob der State ein Finalzustand ist
        """
        return(self.__final)

    def use(self, item):
        """Diese Methode simuliert die Nutzung eines bestimmten Alphabetelements.
        Dabei wird die bereits beschriebene Methode setcurrent(newstate) genutzt
        """
        global current
        if item in self.__alphabet:
            current.setcurrent(zst(self.__outcomes[self.__alphabet.index(item)]))
        else:
            print("item unavailable")

    def draw(self):
        """Diese Methode ist für die GUI zuständig. Dabei wird der vorhergehende
        Zustand gezeichnet, der aktuelle, die Folgezustände und Pfeile, die den aktuellen
        Zustand mit den Folgezuständen verbinden. Zudem steht auf dem Pfeil, durch welche
        Alphabetelemente man diese FOlgezustände erreicht.
        """
        canvas1.delete(ALL)
        if current.final():
            labelfinal["text"] = "ZIELZUSTAND"
            labelfinal["font"] = "bold"
            canvas1["bg"] = "#c0eda1"
            #master["bg"] = "#c0eda1"
        else:
            labelfinal["text"] = "kein Zielzustand"
            canvas1["bg"] = "#f08080"
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
            color = "#c0c0c0"
            canvas1.create_oval(75-r,75-r,75+r,75+r, outline = color)
            canvas1.create_line(75+r,75,225-r,75, dash =(4,3), fill = color)
            canvas1.create_polygon(225-r,75,225-r-12,71,225-r-12,79, fill = color)
            canvas1.create_text(75,75, text = prev.name(), fill = color)
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
            s = math.sqrt(dx**2+dy**2)
            k1 = 13.5/s
            k2 = 4.5/s
            xsp1 = xend + k1*dx - k2 * dy
            ysp1 = yend + k1*dy + k2 * dx
            xsp2 = xend + k1*dx + k2 * dy
            ysp2 = yend + k1*dy - k2 * dx
            canvas1.create_polygon(xend,yend,xsp1,ysp1,xsp2,ysp2)


#Startwert definieren und anzeigen
def initdea():
    """Hiermit wird das Programm initialisiert. Dabei wird der erste Zustand eingeleitet
    und erste Informationen werden mithilfe der showstate()-Methode ausgegeben.
    """
    global prev
    global current
    global startval
    prev = State("prev", [], [], 100, 100, 1)
    current = startval    
    print("Starting state has been set")
    current.showstate()

def zst(name):
    """Diese Methode sucht den Zustand mit dem Name "name" heraus und gibt diesen zurück.
    Man kann so aus strings Variablen von meinem eigenen Typ State machen.
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
    """Diese Methode wird aufgerufen, wenn Mouse1 losgelassen wird. Dabei wird
    überprüft, ob der Mauszeiger sich bei Klicken und Loslassen auf einem der Boxen
    für die Zielstunde lag und leitet diese gegebenenfalls ein.
    """
    global clickx
    global clicky
    global relx
    global rely
    global r
    relx = eventclick.x
    rely = eventclick.y

    global avouts
    for state in avouts:
        if clickverification(zst(state).x(), zst(state).y(), clickx, clicky, relx, rely):
            print(zst(state).name() + " was clicked at")
            current.setcurrent(zst(state))

    if not prev.name() == "prev":
        if clickverification(75,75,clickx,clicky,relx,rely):
            current.setcurrent(prev)
            print("previous state was executed")

def clickverification(px,py,cx,cy,rx,ry):
    hit = 0
    global r
    if cx > px-r and rx > px-r:
        if cx < px+r and rx < px+r:
            if cy > py-r and ry > py-r:
                if cy < py+r and ry < py+r:
                    hit = 1
    return(hit)

def helpwindow():
    """Diese Methode ruft ein Hilfefenster mit einem erklärenden Text auf
    """
    popup = Tk()
    popup.title("Hilfe")
    msg = ("Oben links finden Sie in hellgrau den vorhergehenden\nZustand und oben rechts den aktuellen Zustand.\nUnten sind die möglichen Zielzustände aufgelistet.\nSie können entweder die Zielzustände anklicken,\noder Sie geben das passende Alphabetelement oben\nin das Entry ein und bestätigen. Mit dem reset-Button\nkönnen Sie zum Startzustand zurückkehren. Die rote\nHintergrundfarbe soll anzeigen, dass der aktuelle Zustand\nkein Finalzustand ist, beim Gegenteil davon erfolgt\neine grüne Färbung.")
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
canvas1.grid(row = 1, column = 0, columnspan = 7)
canvas1.bind("<Button-1>", click)
canvas1.bind("<ButtonRelease-1>", release)


#Initialisierung des Startzustandes
initdea()
