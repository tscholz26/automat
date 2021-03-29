"""@package docstring
Documentation for this module.

More details.
"""

ich0 = "{S->0|A0; A->1|2|...|9|A0|A1|...|A9|B1|...|B9; B->+|-}"
ich1 = "{S->0|A0; A->1|2|3|4|5|6|7|8|9|A0|A1|A2|A3|A4|A5|A6|A7|A8|A9|B1|B2|B3|B4|B5|B6|B7|B8|B9; B->+|-}"
loc = "{S->Ba|Aa; A->a|Aa|Sb; B->b|Ab}"
nils = "{S->aS|aA; A->aA|3D;D->aS|6A|6D|3A}"
luisa = "{S->1A|0B|0; A->1A|0A; B->1B|0S|1|0}"
fabi = "{S->0S|1S|0A; A->0B; B->0C|0; C->0C|1C|0|1}"
marc = "{N->aA|bA; A->aA|bB|c; B->bB|c}"
tristan = "{S->0S|1A|1; A->0B|1A|0|1; B->0S|1A|1}"
savedgrammars = [ich1, fabi, loc, nils, luisa, marc, tristan]
savedgrammarnames = ["Tristan S", "Fabien", "Loc", "Nils", "Luisa", "Marc", "Tristan L"]

vers = "2.5.1"

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

global usecolor
usecolor = bool
usecolor = 1
global showprev
showprev = bool
showprev = 1
global showbar
showbar = bool
showbar = 0
global currentgrammar


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
        refreshalphabetmenu()
        

    def showstate(self):
        """Diese Methode gibt Details zum aktuellen Zustand aus
        """
        global current
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

    def addoutcome(self,newoutcome):
        """Diese Methode fügt einen gewünschten Folgezustand hinzu
        """
        self.__outcomes.append(newoutcome)

    def getalphabet(self):
        """Diese Methode gibt die Alphabetelemente aus
        """
        return(self.__alphabet)
    
    def additem(self,newitem):
        """Diese Methode fügt ein gewünschtes Alphabetelement hinzu
        """
        self.__alphabet.append(newitem)

    def setx(self,x):
        """Diese Methode legt eine neue x-Koordinate fest
        """
        self.__x = x

    def sety(self,y):
        """Diese Methode legt eine neue y-Koordinate fest
        """        
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
        global current
        global currentgrammar
        global canvas1
        global labelfinal
        global showbar
        canvas1.delete(ALL)
        global usecolor
        if showbar:
            master.title("Simulation DEA (v" + vers + ")")
        if current.final():
            if showbar:
                labelfinal["text"] = "FINALZUSTAND"
                labelfinal["font"] = "bold"
            else:
                master.title("Simulation DEA (v" + vers + ") (Finalzustand erreicht)")
            if usecolor:
                canvas1["bg"] = "#c0eda1"
        else:
            if showbar:
                labelfinal["text"] = "kein Finalzustand"
            else:
                master.title("Simulation DEA (v" + vers + ") (kein Finalzustand erreicht)" )
            if usecolor:
                canvas1["bg"] = "#f08080"
        global avouts
        avouts = []
        for avout in self.__outcomes:
            if not (avout in avouts):
                avouts.append(avout)
        n = len(avouts)
        global r
        #vorheriges zeichnen
        global showprev
        if showprev:
            if not prev.name() == "prev":
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
    refreshalphabetmenu()
    print("init finished\n--------------------------------------------------")

def zst(name):
    """Diese Methode sucht den Zustand mit dem Name "name" heraus und gibt diesen zurück.
    Man kann so aus strings Variablen von meinem eigenen Typ State machen.
    """
    global statelist
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
    für die Finalzustände lag und leitet diese gegebenenfalls ein.
    """
    global clickx
    global clicky
    global relx
    global rely
    global r
    global current
    relx = eventclick.x
    rely = eventclick.y
    global statelist
    global avouts

    """
    for stateav in avouts:
        if clickverification(zst(stateav).x(), zst(stateav).y(), clickx, clicky, relx, rely):
            print(zst(stateav).name() + " was clicked at")
            current.setcurrent(zst(stateav))
    """
    done = 0
    for stateav in statelist:
        if stateav.name() in current.getoutcomes():
            px = stateav.x()
            py = stateav.y()
            if clickverification(px,py,clickx,clicky,relx,rely) == 1:
                if done == 0:
                    current.setcurrent(stateav)
                    done = 1
        

    if not prev.name() == "prev":
        if clickverification(75,75,clickx,clicky,relx,rely):
            print("previous state was executed (name) : " + prev.name())
            current.setcurrent(prev)

def keypress(key):
    """Diese Methode wird aufgerufen, wenn die Tastatur bedient wird. Falls eine
    Taste gedrückt wird, die mit einem der Menü-Hotkeys übereinstimmt, wird dessen
    Funktion ausgeführt
    """
    if key.char == "h":
        helpwindow()
    if key.char == "r":
        initdea()
    if key.char == "z":
        current.setcurrent(prev)

def clickverification(px,py,cx,cy,rx,ry):
    """Diese Methode überprüft, ob mit einem Mouseclick der Punkt (px|py) getroffen
    wurde. Dabei wurde der Punkt C(xy|cy) angeklickt und bei R(rx|ry) wurde der
    Mousebutton losgelassen.
    """
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
    msg = ("Oben links finden Sie in hellgrau den vorhergehenden\nZustand und oben rechts den aktuellen Zustand.\nUnten sind die möglichen Finalzustände aufgelistet.\nSie können entweder die Finalzustände anklicken,\noder Sie geben das passende Alphabetelement oben\nin das Entry ein und bestätigen. Mit dem reset-Button\nkönnen Sie zum Startzustand zurückkehren. Die rote\nHintergrundfarbe soll anzeigen, dass der aktuelle Zustand\nkein Finalzustand ist, beim Gegenteil davon erfolgt\neine grüne Färbung.")
    labelmsg = Label(popup, text = msg, justify = 'left', font = '15')
    labelmsg.pack(padx = 10, pady = 10)
                        



def convert(r):
    """Diese Funktion wandelt die Regelmenge in einen DEA um, der danach im
    Programm geladen wird. Erst wird dabei die Regelmenge der Grammatik in einzelne
    Regeln zerlegt, dann wird daraus ein NEA gebildet. Aus dem NEA wird dann ein
    DEA gemacht, wobei durch die melt()-Methode jeweils neue Zustände entstehen.
    Zum Schluss wird dieser DEA im Programm geladen.
    """
    global statelist
    global startval
    global current
    
    Np = ["A","B","C","D","E","F","G","G","S"]
    global N
    N = []
    Tp = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","+","-"]
    global T
    T = []
    R = []
    S = str
    #klammern entfernen
    r = r[r.index("{")+1:r.index("}")]
    print("klammern entfernt\nr: " + r + "\n")


    #leerzeichen filtern
    i = 0
    while i < len(r):    
        if r[i] == " ":
            r = r[0:i] + r[i+1:]
        i = i + 1
    print("leerzeichen gefiltert: " + r + "\n")

    
    i = 0
    while i < len(r):
        if r[i] == "-":
            if i < len(r)-1:
                if r[i+1] == ">":
                    r = r[:i] + "$" + r[i+2:]
                    i = 0
        i = i + 1
    print("pfeil ersetzt: " + r + "\n")

    #N, T und S bestimmen
    for i in range(0,len(r)):
        if r[i] in Np:
            if not r[i] in N:
                N.append(r[i])
        if r[i] in Tp:
            if not r[i] in T:
                T.append(r[i])
    S = r[0]
    
    print("Startzustand: " + S)
    print("N: " + str(N))
    print("T: " + str(T))
    

    #regeln seperieren
    i = 0
    while i < len(r):    
        if r[i] == ";":
            newrule = r[0:i]
            R.append(newrule)
            r = r[i+1:]
            i = 0
        i = i + 1
    R.append(r)
    print("regelmenge: " + str(R) + "\n")

    #durch | getrennte regeln vereinzeln
    rulelist =  []
    for rule in R:
        i = 0
        while i < len(rule):
            if rule[i] == "|":
                singlerule = rule[0:i]
                rulelist.append(singlerule)
                rule = rule[0:rule.index("$")+1] + rule[i+1:]
                i = 0
            i = i + 1
        rulelist.append(rule)
    print("regeln vereinzelt: " + str(rulelist) + "\n")


    #nea erstellen
    statelist = []
    global nea
    nea = []
    neanamelist = []
    global dea
    dea = []
    finallist = []
    for rule in rulelist:
        outcomes = []
        alphabet = []
        left = rule[:rule.index("$")]
        right = rule[rule.index("$")+1:]
        item = str
        final = 1
        #t: alphabetsymbole
        #n: zustände
        for i in range(0,len(right)):
            if right[i] in N:
                final = 0
        removed = 0
        for i in range(0,len(right)):
            if removed == 0:
                if right[i] in T:
                    removed = 1
                    item = right[i]
                    if final == 0:
                        right = right[:i]+ right[i+1:]
                    else:
                        right = left + "_final"
                        if right not in finallist:
                            finallist.append(right)
        
        outcomes.append(right)        
        alphabet.append(item)
        newstate = State(left, outcomes, alphabet, 100, 100, 0)
        statelist.append(newstate)
        #zu nea hinzufügen, wenn es noch keinen mit gleichem name gibt
        if not newstate.name() in neanamelist:
            nea.append(newstate)
            neanamelist.append(newstate.name())
    for state in statelist:
        i = 0
        while i < len(nea):
            neastate = nea[i]
            if (state.name() == neastate.name()):
                if not state == neastate:
                    neastate.addoutcome(state.getoutcomes()[0])
                    neastate.additem(state.getalphabet()[0])
            i = i + 1
    for finalstate in finallist:
        nea.append(State(finalstate, [], [], 100, 100, 1))
    
    global deastatelist
    global startval
    deastatelist = []

    global deanamelist
    deanamelist = []
    
    #einbuchstabige alte zustände hinzufügen
    for state in nea:
        if state.name() not in deanamelist:
            defoutc = []
            defalph = []
            for item in state.getalphabet():
                if item not in defalph:
                    defalph.append(item)
            
            for symbol in defalph:
                outcpartlist = []
                outcomename = ""
                for i in range(0,len(state.getoutcomes())):
                    if state.getalphabet()[i] == symbol:
                        newpart = state.getoutcomes()[i]
                        if newpart not in outcpartlist:
                            outcpartlist.append(newpart)
                for outc in outcpartlist:
                    if outcomename == "":
                        outcomename = outc
                    else:
                        outcomename = outcomename + outc
                defoutc.append(outcomename)
            
            defstate = State(state.name(), defoutc, defalph, 100, 100, state.final())
            if defstate.name() not in deanamelist:
                deastatelist.append(defstate)
                deanamelist.append(defstate.name())

    dea = deastatelist
                
    dea = dea + neatodea(nea)
    statelist = dea
    
    for state in dea:
        if state.name() == S:
            startval = state
    return(dea, startval, startval)


def neatodea(nea):
    """Diese Methode greift einen NEA auf und wandelt ihn mithilfe der melt()-Methode
    in einen DEA um, der mit return zurückgegeben wird.
    """
    completeamb = 0
    global deastatelist
    global deanamelist
    global meltlist
    meltlist = []
    for state in nea:
        ambig = 0
        if len(state.getoutcomes()) == 0:
            if state.name() not in deanamelist:
                deastatelist.append(state)
                deanamelist.append(state.name())
                ambig = 1
        for i in range(0,len(state.getalphabet())):
            for j in range(0,len(state.getalphabet())):
                if state.getalphabet()[i] == state.getalphabet()[j]:
                    if i < j:
                        namei = state.getoutcomes()[i]
                        namej = state.getoutcomes()[j]
                        ambig = 1
                        completeamb = 1
                        newstate = namei+"|"+namej
                        if newstate not in meltlist:
                            if not namei == namej:
                                meltlist.append(newstate)
                                print("created state: " + newstate)

    if ambig == 0:
        if state.name() not in deanamelist:
            deastatelist.append(state)
            deanamelist.append(state.name())
    global meltlistdone
    meltlistdone = []
    while len(meltlist) > 0:
        melt()
    return(deastatelist)

def melt():
    """Diese Methode setzt einen Zustand aus mehreren einzelnen Zuständen zusammen.
    Wenn dabei neue Zielzustände entstehen, werden diese rekursiv wieder mit der
    melt()-Methode erstellt
    """
    global nea
    global deastatelist
    global meltlist
    global T
    global deanamelist
    global meltlistdone

    
    alph = []
    outc = []

    startname = meltlist[0]
    meltlistdone.append(startname)
    meltlist = meltlist[1:]
    names = []
    partcount = 1
    for i in range(0,len(startname)):
        if startname[i] == "|":
            partcount = partcount + 1


    nameparts = []
    for i in range(0,partcount-1):
        ind = startname.index("|")
        nameparts.append(startname[:ind])
        startname = startname[ind+1:]
    nameparts.append(startname)
    
    for part in nameparts:
        if part in names:
            partcount = partcount - 1
        else:
            names.append(part)
        
    states = []
    for i in range(0,partcount):
        states.append("")
        
    for i in range(0,partcount):
        for state in nea:
            if state.name() == names[i]:
                states[i] = state

    statesname = ""
    statesnamebars = ""
    for i in names:
        statesname = statesname + i
        if statesnamebars == "":
            statesnamebars = i
        else:
            statesnamebars = statesnamebars + "|" + i

    alphabet = []
    for state in states:
        for i in range(0,len(state.getalphabet())):
            if state.getalphabet()[i] not in alphabet:
                alphabet.append(state.getalphabet()[i])

    final = 0
    for state in states:
        if state.final() == 1:
            final = 1

    for item in T:
        itemused = 0
        outcomeparts = []
        outcomename = ""
        outcomenamebars = ""
        usedlist = []
        for state in states:
            for i in range(0,len(state.getalphabet())):
                if state.getalphabet()[i] == item:
                    itemused = 1
                    if state.getoutcomes()[i] not in usedlist:
                        usedlist.append(state.getoutcomes()[i])
                        outcomename = outcomename + state.getoutcomes()[i]
                        if outcomenamebars == "":
                            outcomenamebars = state.getoutcomes()[i]
                        else:
                            outcomenamebars = outcomenamebars + "|" + state.getoutcomes()[i]

                seenstate = 0
                for deastate in deastatelist:
                    if deastate.name() == outcomename:
                        seenstate = 1
                if seenstate == 0:
                    if not (outcomenamebars in meltlistdone):
                        if not (outcomenamebars in meltlist):
                            if outcomenamebars != "":
                                meltlist.append(outcomenamebars)
                            
        if itemused == 1:
            alph.append(item)
            outc.append(outcomename)

    newstate = State(statesname, outc, alph, 100, 100, final)
    if newstate.name() not in deanamelist:
        deastatelist.append(newstate)
        deanamelist.append(newstate.name())



#Eingabe des DEAS
"""für grammar->dfa:
prev = State("prev", [], [], 100, 100, 1)
statelist, startval, current = convert(ich1)
"""
q_2 = State("q_2", ["q_05"], ["0"], 100, 100, 0)
q_05 = State("q_05", ["q_0", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013"], ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], 100, 100, 1)
q_0 = State("q_0", ["q_0", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013"], ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], 100, 100, 0)
q_013 = State("q_013", ["q_0", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_4", "q_4"], ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "-"], 100, 100, 1)              
q_4 = State("q_4", [], [], 100, 100, 1)
prev = State("prev", [], [], 100, 100, 1)
statelist = [q_2, q_05, q_0, q_013, q_4]
global startval
startval = q_2
current = startval

def exec(regelmenge):
    """Diese Methode legt aus einer Regelmenge mit der convert()-Methode die
    Zustandsmenge und den Startzustand fest und startet die Programmsimulation
    """
    global current
    global statelist
    global startval
    global currentgrammar
    currentgrammar = regelmenge
    statelist, startval, current = convert(regelmenge)
    initdea()

def grammarwindow():
    """Diese Methode öffnet ein neues Fenster, in dem man eine neue
    Regelmenge eingibt und diese im Programm simulieren kann.
    """
    grammarwin = Tk()
    grammarwin.title("Regelmenge implementieren")
    entryrules = Entry(grammarwin, width = 45)
    entryrules.grid(column = 0, row = 0, padx = 10)
    buttonsetgrammar = Button(grammarwin, text = "use", command = lambda:(exec(entryrules.get())))
    buttonsetgrammar.grid(column = 1, row = 0, padx = 10, pady = 10)

def generatewidgets(infobar):
    """Diese Methode generiert die nötigen Widgets für das tkinter-Fenster
    """
    global current
    widgetlist = master.grid_slaves()
    for widget in widgetlist:
        widget.destroy()
    global canvas1
    canvas1 = Canvas(master, width = 600, height = 450)
    canvas1.bind("<Button-1>", click)
    canvas1.bind("<ButtonRelease-1>", release)
    master.bind("<KeyPress>", keypress)
    if infobar == 1:
        global labelfinal
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

        canvas1.grid(row = 1, column = 0, columnspan = 7)        
    if infobar == 0:
        canvas1.grid(row = 0, column = 0)
    global current
    current.draw()


def save():
    """Diese Methode speichert den aktuellen Zustand als .txt-file. Das umfasst die
    aktuelle Regelmenge, den aktuellen Zustand und den vorhergehenden Zustand.
    """
    global currentgrammar
    global current
    global prev
    statefile = open("save.txt", "w")
    statefile.write(currentgrammar + "$" + current.name() + "%" +  prev.name())
    statefile.close

def load():
    """Diese Methode lädt Regelmenge, vorhergehenden Zustand und aktuellen Zustand
    aus einem .txt-file.
    """
    statefile = open("save.txt")
    line = statefile.readlines()
    print("typ: " + str(type(line)))
    x = str(line)[2:-2]
    print("line: " + x)

    grammar = x[:x.index("$")]
    curname = x[x.index("$")+1:x.index("%")]
    prevname = x[x.index("%")+1:]

    #print("grammar: " + grammar + "|")
    #print("cur: " + curname + "|")
    #print("prev: " + prevname + "|")
    exec(grammar)
    global deastatelist
    global current
    newprev = State("prev", [], [], 100, 100, 0)
    for state in deastatelist:
        if state.name() == curname:
            newcur = state
        if state.name() == prevname:
            newprev = state
            print("set prev")
    current.setcurrent(newprev)
    current.setcurrent(newcur)



menubar = Menu(master)
#enlist different cascades
statemenu= Menu(menubar, tearoff = 0)
deamenu = Menu(menubar, tearoff = 0)
deasuggestions = Menu(menubar, tearoff = 0)
alphabetmenu = Menu(menubar, tearoff = 0)
appearancemenu = Menu(menubar, tearoff = 0)
helpmenu = Menu(menubar, tearoff = 0)


#define cascades
statemenu.add_command(label = "Vorgergehender Zustand  (z)", command = lambda:(current.setcurrent(prev)))
statemenu.add_cascade(label = "Folgezustand bestimmen", menu = alphabetmenu)
statemenu.add_separator()
statemenu.add_command(label = "Zustand speichern", command = save)
statemenu.add_command(label = "Zustand laden", command = load)
statemenu.add_separator()
statemenu.add_command(label = "Zurücksetzen  (r)", command = initdea)


deamenu.add_command(label = "Regelmenge Tristan S", command = lambda:(exec(ich1)))
deamenu.add_command(label = "Selbst eingeben", command = grammarwindow)
deamenu.add_separator()
for i in range(0,len(savedgrammars)):
    deasuggestions.add_command(label = (savedgrammarnames[i] + ":   " + savedgrammars[i]), command = lambda x = savedgrammars[i]:exec(x))
deamenu.add_cascade(label = "Vorschläge", menu = deasuggestions)

    
def refreshalphabetmenu():
    """Diese Methode fügt im Menü jeweils Menüpunkte für die aktuell verfügbaren
    Alphabetelemente hinzu.
    """
    global current
    alphabetmenu.delete(0,END)
    for i in current.getalphabet():
        alphabetmenu.add_command(label = i, command = lambda x = i: current.use(str(x)))

def refreshappearancemenu():
    """Diese Methode fügt die Menüpunkte des Erscheinungsbild-Menüs hinzu. Wenn man
    sich gerade im Farbmodus befindet, gibt es den Menüpunkt "Farbmodus ausschalten"
    und umgekehrt.
    """
    appearancemenu.delete(0,END)
    global showbar
    global usecolor
    global showprev     
    if showbar:
        appearancemenu.add_command(label = "Widget-Leiste verbergen", command = lambda:(toggleshowbar(0)))
    else:
        appearancemenu.add_command(label = "Widget-Leiste einfügen", command = lambda:(toggleshowbar(1)))
    if usecolor:
        appearancemenu.add_command(label = "Farbmodus ausschalten", command = lambda:(togglecolor(0)))
    else:
        appearancemenu.add_command(label = "Farbmodus anschalten", command = lambda:(togglecolor(1)))
    if showprev:
        appearancemenu.add_command(label = "Vorhergenenden Zustand verbergen", command = lambda:(toggleshowprev(0)))
    else:
        appearancemenu.add_command(label = "Vorhergehenden Zustand anzeigen", command = lambda:(toggleshowprev(1)))
    

def togglecolor(x):
    """Diese Methode stellt den aktuellen Farbmodus und den dazugehörigen
    Menüpunkt um.
    """
    global usecolor
    global current
    if x == 0:        
        usecolor = 0
        canvas1["bg"] = "#f0f0f0"
    else:
        usecolor = 1
        if current.final():
            canvas1["bg"] = "#c0eda1"
        else:
            canvas1["bg"] = "#f08080"
    refreshappearancemenu()

def toggleshowprev(x):
    """Diese Methode stellt die Anzeige des vorhergehenden Zustands und
    den dazugehörigen Menüpunkt um.
    """
    global showprev
    global current
    if x == 0:
        showprev = 0
    else:
        showprev = 1
    current.draw()
    refreshappearancemenu()

def toggleshowbar(x):
    """Diese Methode stellt die Anzeige der Leiste mit Widgets im Fenster
    und den dazugehörigen Menüpunkt an.
    """
    global showbar
    if x == 0:
        showbar = 0
        generatewidgets(0)
    else:
        showbar = 1
        generatewidgets(1)    
    refreshappearancemenu()

    

def shownea():
    """Diese Methode stellt alle Zustände der nea-Variable dar.
    """
    global nea
    for n in range(0,len(nea)):
        print("\n" + nea[n].name())
        print(nea[n].getoutcomes())
        print(nea[n].getalphabet())
        print(nea[n].final())

def showdea():
    """Diese Methode stellt alle Zustände der deastatelist-Variable dar.
    """
    global deastatelist
    for n in range(0,len(deastatelist)):
        print("\n" + deastatelist[n].name())
        print(deastatelist[n].getoutcomes())
        print(deastatelist[n].getalphabet())

def showlist():
    """Diese Methode stellt alle Zustände der statelist-Variable dar.
    """
    global statelist
    for n in range(0,len(statelist)):
        print("\n" + statelist[n].name())
        print(statelist[n].getoutcomes())
        print(statelist[n].getalphabet())
        print(statelist[n].x())
        print(statelist[n].y())

    
    
helpmenu.add_command(label = "Hilfe anzeigen  (h)", command = helpwindow)


#add cascades to menubar
menubar.add_cascade(label = "Zustände", menu = statemenu)
menubar.add_cascade(label = "Grammatik laden", menu = deamenu)
menubar.add_cascade(label = "Erscheinungsbild", menu = appearancemenu)
menubar.add_cascade(label = "Hilfe", menu = helpmenu)

master["menu"] = menubar


#Initialisierung des Startzustandes
generatewidgets(showbar)
refreshalphabetmenu()
refreshappearancemenu()
exec(ich1)



