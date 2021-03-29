"""@package docstring
Documentation for this module.

More details.
"""

vers = "2.3.1"

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
        self.__outcomes.append(newoutcome)

    def getalphabet(self):
        """Diese Methode gibt die ALphabetelemente aus
        """
        return(self.__alphabet)
    
    def additem(self,newitem):
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
                master.title("Simulation DEA (v" + vers + ") (kein Finalzustand erreicht)")
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
    für die Finalzustände lag und leitet diese gegebenenfalls ein.
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

def keypress(key):
    if key.char == "h":
        helpwindow()
    if key.char == "z":
        initdea()

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
current = startval

def generatewidgets(infobar):
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



menubar = Menu(master)
#enlist different cascades
statemenu= Menu(menubar, tearoff = 0)
alphabetmenu = Menu(menubar, tearoff = 0)
appearancemenu = Menu(menubar, tearoff = 0)
helpmenu = Menu(menubar, tearoff = 0)


#define cascades
statemenu.add_command(label = "Vorgergehender Zustand", command = lambda:(current.setcurrent(prev)))
statemenu.add_cascade(label = "Folgezustand", menu = alphabetmenu)
statemenu.add_separator()
statemenu.add_command(label = "Zurücksetzen  (z)", command = initdea)
    
def refreshalphabetmenu():
    alphabetmenu.delete(0,END)
    for i in current.getalphabet():
        alphabetmenu.add_command(label = i, command = lambda x = i: current.use(str(x)))

def refreshappearancemenu():
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
    global usecolor
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
    global showprev
    if x == 0:
        showprev = 0
    else:
        showprev = 1
    current.draw()
    refreshappearancemenu()

def toggleshowbar(x):
    global showbar
    if x == 0:
        showbar = 0
        generatewidgets(0)
    else:
        showbar = 1
        generatewidgets(1)    
    refreshappearancemenu()

    
helpmenu.add_command(label = "Hilfe anzeigen  (h)", command = helpwindow)
#helpmenu.add_command(label = "show DEA", command = lambda:(print("dea showed")))


#add cascades to menubar
menubar.add_cascade(label = "Zustände", menu = statemenu)
menubar.add_cascade(label = "Erscheinungsbild", menu = appearancemenu)
menubar.add_cascade(label = "Hilfe", menu = helpmenu)


master["menu"] = menubar


#Initialisierung des Startzustandes
generatewidgets(showbar)
initdea()
refreshalphabetmenu()
refreshappearancemenu()


#zu tun: speichern/öffnen der zustände https://exeter-data-analytics.github.io/python-intro/files.html
#im programm implementieren: grammatik mit regelmenge->dea->in programm einfügen









ich0 = "{S->0|A0; A->1|2|...|9|A0|A1|...|A9|B1|...|B9; B->+|-}"
ich1 = "{S->0|A0; A->1|2|3|4|5|6|7|8|9|A0|A1|A2|A3|A4|A5|A6|A7|A8|A9|B1|B2|B3|B4|B5|B6|B7|B8|B9; B->+|-}"
loc = "{S->Ba|Aa; A->a|Aa|Sb; B->b|Ab}"
nils = "{S->aS|aA; A->aA|3D;D->aS|6A|6D|3A}"
luisa = "{S->1A|0B|0; A->1A|0A; B->1B|0S|1|0}"
fabi = "{S->0S|1S|0A; A->0B; B->0C|0; C->0C|1C|0|1}"
marc = "{N->aA|bA; A->aA|bB|c; B->bB|c}"
tristan = "{S->0S|1A|1; A->0B|1A|0|1; B->0S|1A|1}"


def convert(r):
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
            #print("newrule: " + newrule)
            r = r[i+1:]
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
                #print("singlerule: " + singlerule)
                rule = rule[0:rule.index("$")+1] + rule[i+1:]
                #print("new R part: " + str(rule))
                i = 0
            i = i + 1
        rulelist.append(rule)
        #print("new singlerule: " + rule)
    print("regeln vereinzelt: " + str(rulelist) + "\n")


    #nea erstellen
    global statelist
    statelist = []
    global nea
    nea = []
    neanamelist = []
    global dea
    dea = []
    finallist = []
    #statecount = 0
    for rule in rulelist:
        left = rule[:rule.index("$")]
        right = rule[rule.index("$")+1:]
        item = str
        final = 1
        for i in range(0,len(right)):
            if right[i] in N:
                final = 0
            if right[i] in T:
                item = right[i]
                if final == 0:
                    right = right[:i]+ right[i+1:]
                else:
                    right = left + "_final"
                    if right not in finallist:
                        finallist.append(right)
        outcomes = []
        outcomes.append(right)
        alphabet = []
        alphabet.append(item)
        #newstate = State(left, outcomes, alphabet, 100, 100, final)
        #print("nea final: " + str(final))
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
            #nea[i] = neastate
            i = i + 1
    for finalstate in finallist:
        nea.append(State(finalstate, [], [], 100, 100, 1))

    global deastatelist
    global startval
    deastatelist = []
    dea = neatodea(nea)
    showdea()
    """
    for state in dea:
        if state.name() == "S":
            startstate = state
    """
    startstate = dea[3]
    
    return(dea,startstate)

def neatodea(nea):
    completeamb = 0
    global deastatelist
    global deanamelist
    deanamelist = []
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
                            meltlist.append(newstate)
                            print("added item: " + newstate)
            """
                        for zst in nea:
                                #print("name: " + zst.name())
                                if state.getoutcomes()[i] == zst.name():
                                    statei = zst
                                if state.getoutcomes()[j] == zst.name():
                                    statej = zst
            """
    if ambig == 0:
        if state.name() not in deanamelist:
            deastatelist.append(state)
            deanamelist.append(state.name())
    print("meltlist0: " + str(meltlist))
    while len(meltlist) > 0:
        #melt(meltlist[0])
        melt()
    return(deastatelist)

def melt():
    global nea
    global deastatelist
    global meltlist
    global T
    global deanamelist

    alph = []
    outc = []

    startname = meltlist[0]
    meltlist = meltlist[1:]
    #print("prepare melting: " + startname)
    #print(meltlist)
    names = []
    while len(startname) > 0:
        barfound = 0
        i = 0
        while i < len(startname):
            if startname[i] == "|":
                names.append(startname[:i])
                startname = startname[i+1:]
                barfound = 1
            i = i + 1
        if barfound == 0:
            names.append(startname)
            startname = ""
    #print("names: " + str(names))

    partcount = len(names)

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

    print(statesname)

    alphabet = []
    for state in states:
        for i in range(0,len(state.getalphabet())):
            if state.getalphabet()[i] not in alphabet:
                alphabet.append(state.getalphabet()[i])
    #print("alphabet gesamt: " + str(alphabet))

    final = 0
    for state in states:
        if state.final() == 1:
            final = 1
    #print("final: " + str(final))

    """
    for item in alphabet:
        outcomes = []
        outcomeitemlist = []
        for state in states:
            for i in range(0,len(state.getalphabet())):
                if state.getalphabet()[i] == item:
                    outcomepart = state.getoutcomes()[i]
                    #if outcomepart not in outcomeitemlist:
                    if 1 == 1:
                        outcomeitemlist.append(outcomepart)
        #zusammensetzen
        outcomeitem = ""
        outcomeitembars = ""
        for symbol in outcomeitemlist:
            outcomeitem = outcomeitem + symbol
            if outcomeitembars == "":
                outcomeitembars = symbol
            else:
                outcomeitembars = outcomeitembars + "|" + symbol
        outcomes.append(outcomeitem)
    print("outcomes: " + str(outcomes))
    """
    for item in T:
        itemused = 0
        outcomeparts = []
        outcomename = ""
        outcomenamebars = ""
        for state in states:
            for i in range(0,len(state.getalphabet())):
                if state.getalphabet()[i] == item:
                    itemused = 1
                    outcomename = outcomename + state.getoutcomes()[i]
                    if outcomenamebars == "":
                        outcomenamebars = state.getoutcomes()[i]
                    else:
                        outcomenamebars = outcomenamebars + "|" + state.getoutcomes()[i]

                        seenstate = 0
                        for deastate in deastatelist:
                            #print("deastate: " + str(deastate.name()))
                            #print("outcstate: " + str(outcomename))
                            if deastate.name() == outcomename:
                                seenstate = 1
                                print("duped")
                        if seenstate == 0:
                            if not (outcomenamebars in meltlist):
                                meltlist.append(outcomenamebars)
                        
        #print(outcomename)
        if itemused == 1:
            alph.append(item)
            outc.append(outcomename)
    #print(alph)
    #print(outc)
    newstate = State(statesname, outc, alph, 100, 100, final)
    if newstate.name() not in deanamelist:
        deastatelist.append(newstate)
        deanamelist.append(newstate.name())
    #print("DEA len: " + str(len(deastatelist)))
    
def shownea():
    global nea
    for n in range(0,len(nea)):
        print("\n" + nea[n].name())
        print(nea[n].getoutcomes())
        print(nea[n].getalphabet())

def showdea():
    global deastatelist
    for n in range(0,len(deastatelist)):
        print("\n" + deastatelist[n].name())
        print(deastatelist[n].getoutcomes())
        print(deastatelist[n].getalphabet())



statelist,startval = convert(ich1)
current = startval
initdea()
#convert(fabi)
#shownea()
#showdea()



