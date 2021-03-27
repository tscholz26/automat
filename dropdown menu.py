from tkinter import *
master = Tk()

answer = StringVar(master)

liste = ["1", "2", "3"]
dmenu = OptionMenu(master, answer, *liste)
dmenu.pack()

liste2 = ["uohou", "uizhiuz", "uihiu"]
def setnew(neu):
    dmenu['menu'].delete(0, 'end')
    for item in neu:
        #dmenu['menu'].add_command(label=item, command=tk._setit(var, item))
        #dmenu['menu'].add(item)
        dmenu.set_menu(default = None, *liste2)

menu2 = Menu(master, answer, *liste)
menu2.pack()

setnew(liste2)
