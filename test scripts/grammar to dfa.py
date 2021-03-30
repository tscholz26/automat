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
    N = []
    Tp = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","+","-"]
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
        
convert(ich1)

