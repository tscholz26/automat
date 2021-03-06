"""@package docstring
Documentation for this module.

More details.
"""

global current

class State():
    """
    Diese Klasse beschreibt Zustände
    outcomes: verschiedene folgezustände in bestimmter reihenfolge
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
        """Diese Methode dient dazu, den Namen des Zustands zurückzugeben.
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
        if len(self.__outcomes) > 0:
            asknextstate()
        else:
            answer = input("dead end! restart? (y/n) ")
            print("--------------------------------------------------")
            if answer == "y":
                initdea()

            
    def getoutcomes(self):
        return(self.__outcomes)

    def getalphabet(self):
        return(self.__alphabet)

    def draw(self):
        avouts = []
        for avout in self.__outcomes:
            if not (avout in avouts):
                avouts.append(avout)
        n = len(avouts)
        print("zu zeichnende kreise: " + str(n))




def asknextstate():
    #current.draw()
    alph = current.getalphabet()
    outc = current.getoutcomes()
    alphitem = (input("next alphabet item used? "))
    if alphitem in alph:
        nextname = outc[alph.index(alphitem)]
        if nextname in outc:
            for nextstate in statelist:
                if nextname == nextstate.name():
                    current.setcurrent(nextstate)
            #asknextstate()
        else:
            print("mistake occured")
            asknextstate()
    else:
        print("item not available atm")
        asknextstate()

#Startwert definieren und anzeigen
def initdea():
    global current
    current = startval
    print("Starting state has been set")
    current.showstate()
    asknextstate()

        
"""Test DEA:
q_0 = State("q_0", ["q_0", "q_1", "q_3"], ["a","1","3"],  0)
q_1 = State("q_1", ["q_1", "q_2"], ["1","2"], 20, 40, 0)
q_2 = State("q_2", ["q_0"], ["f"], 20, 40, 0)
q_3 = State("q_3", ["q_1", "q_2", "q_3"], ["1","2","3"], 20, 40, 1)
statelist = [q_0, q_1, q_2, q_3]
startval = q_0
"""

#Eingabe des DEAS
q_2 = State("q_2", ["q_05"], ["0"], 20, 40, 0)
q_05 = State("q_05", ["q_0", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013"], ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], 20, 40, 1)
q_0 = State("q_0", ["q_0", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013"], ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], 20, 40, 0)
q_013 = State("q_013", ["q_0", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_013", "q_4", "q_4"], ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "-"], 20, 40, 1)              
q_4 = State("q_4", [], [], 20, 40, 1)
statelist = [q_2, q_05, q_0, q_013, q_4]
startval = q_2


#Initialisierung des Startzustandes
current = startval
initdea()






