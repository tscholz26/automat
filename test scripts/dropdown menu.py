from tkinter import *

master = Tk()
menubar = Menu(master)

#enlist different cascades
statemenu= Menu(menubar, tearoff = 0)
alphabetmenu = Menu(menubar, tearoff = 0)
alphabetfullmenu = Menu(menubar, tearoff = 0)
helpmenu = Menu(menubar, tearoff = 0)


#define cascades
statemenu.add_command(label = "reset", command = lambda:(print("reset finished")))
statemenu.add_command(label = "prev", command = lambda:(print("went one step back")))
    
alphabetmenu.add_command(label = "1", command = lambda:(print("1")))
alphabetmenu.add_command(label = "2", command = lambda:(print("2")))
alphabetmenu.add_command(label = "3", command = lambda:(print("3")))

global n
n = int

for i in range(0,10):
    alphabetfullmenu.add_command(label = i, command = lambda x = i: useitem(x))

def useitem(x):
    global n
    n = int(x)
    print(str(n))
    
helpmenu.add_command(label = "info about colors", command = lambda:(print("colorinfo")))
helpmenu.add_command(label = "popup tips", command = lambda:(print("tipps hier zu finden")))
helpmenu.add_separator()
helpmenu.add_command(label = "show DEA", command = lambda:(print("dea showed")))


#add cascades to menubar
menubar.add_cascade(label = "States", menu = statemenu)
menubar.add_cascade(label = "Alphabet", menu = alphabetmenu)
menubar.add_cascade(label = "Full alp", menu = alphabetfullmenu)
menubar.add_cascade(label = "Help", menu = helpmenu)

master["menu"] = menubar

