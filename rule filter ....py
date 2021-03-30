#rule = "{S->0|A0; A->1|2|...|9|A0|A1|...|A9|B1|...|B9; B->+|-}"
rule = "{S->0|A0; A->1|2|3|4|5|6|7|8|9|A0|A1|A2|A3|A4|A5|A6|A7|A8|A9|B1|B2|B3|B4|B5|B6|B7|B8|B9; B->+|-}"
#rule = "{S->0|A0; A->0|1|...|9}"
#rule = "{S->0|A0; A->10|11|...|98|99}"
#rule = "{A-> A0|A1|...|A9}"
def filterdots(rulelist):
    rule = rulelist
    filtered = 0
    while filtered == 0:
        filtered = 1
        i = 0
        while i < len(rule):
            if rule[i] == ".":
                if rule[i+1] == ".":
                    if rule[i+2] == ".":
                        filtered = 0
                        bars = 0
                        n = 1
                        found = 0
                        while found == 0:
                            if rule[i-1] == "|":
                                if rule[i-1-n] == "|":
                                    found = 1
                            n = n + 1
                        n = n - 2
                        itemleft = rule[i-1-n:i-1]
                        itemright = rule[i+4:i+4+n]
                        itemmiddle = ""
                        if itemleft == "0" and itemright == "9":
                            itemmiddle = "1|2|3|4|5|6|7|8"
                        if itemleft == "1" and itemright == "9":
                            itemmiddle = "2|3|4|5|6|7|8"
                        if itemleft == "2" and itemright == "9":
                            itemmiddle = "3|4|5|6|7|8"
                            
                        if itemleft == "A0" and itemright == "A9":
                            itemmiddle = "A1|A2|A3|A4|A5|A6|A7|A8"
                        if itemleft == "A1" and itemright == "A9":
                            itemmiddle = "A2|A3|A4|A5|A6|A7|A8"
                        if itemleft == "A2" and itemright == "A9":
                            itemmiddle = "A3|A4|A5|A6|A7|A8"

                        if itemleft == "B0" and itemright == "B9":
                            itemmiddle = "B1|B2|B3|B4|B5|B6|B7|B8"
                        if itemleft == "B1" and itemright == "B9":
                            itemmiddle = "B2|B3|B4|B5|B6|B7|B8"
                        if itemleft == "B2" and itemright == "B9":
                            itemmiddle = "B3|B4|B5|B6|B7|B8"
                            
                        rule = rule[:i] + itemmiddle + rule[i+3:]
                        
            i = i + 1
    #print("rule: " + rule)
    return(rule)

print(filterdots(rule))


