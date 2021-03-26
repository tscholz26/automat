"""@package docstring
Documentation for this module.

More details.
"""

from tkinter import *
import math, time

#master = Tk()


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
        print("outcomes: ")
        #for outcome in self.__outcomes:
        #    print(outcome)
        for i in range (0,len(self.__outcomes)):
            print(str(self.__alphabet[i]) + " --> " + self.__outcomes[i])
        if self.__final:
            print("final state reached")
        else:
            print("final state not reached")
            
    def getoutcomes(self):
        return(self.__outcomes)

    def getalphabet(self):
        return(self.__alphabet)

q_0 = State("q_0", ["q_0", "q_1", "q_3"], ["a","1","3"], 20, 40, 0)
q_1 = State("q_1", ["q_1", "q_2"], ["1","2"], 20, 40, 0)
q_2 = State("q_2", ["q_0"], ["f"], 20, 40, 0)
q_3 = State("q_3", ["q_1", "q_2", "q_3"], ["1","2","3"], 20, 40, 1)

statelist = [q_0, q_1, q_2, q_3]
#Startwert definieren und anzeigen
current = q_0
print("Starting state has been set")
current.showstate()


def asknextstate():
    alph = current.getalphabet()
    outc = current.getoutcomes()
    alphitem = (input("next alphabet item used? "))
    if alphitem in alph:
        nextname = outc[alph.index(alphitem)]
        if nextname in outc:
            for nextstate in statelist:
                if nextname == nextstate.name():
                    current.setcurrent(nextstate)
            asknextstate()
        else:
            print("mistake occured")
            asknextstate()
    else:
        print("item not available atm")
        asknextstate()

asknextstate()


#noch zu tun
# fehler, wenn alphabet nicht genauso viele elemente hat wie outcomes (fehlerbehebung direkt bei der eingabe)



