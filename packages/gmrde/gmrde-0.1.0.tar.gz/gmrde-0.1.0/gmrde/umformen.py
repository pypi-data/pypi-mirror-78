# umformen.py - Wörter und Sätze umformen
# Copyright 2020 Jakob Stolze <https://github.com/jarinox>


frws = ["wer", "wo", "was", "wen", "wem", "welche", "welcher", "welches", "welchem", "wohin", "woher", "womit", "wie", "wann", "woran", "warum", "weshalb", "weswegen", "wozu"]

def pronomenTausch(pronom):
    """Tausche ein Pronomen der 1. Person Singular zur 2. Person Singular oder anders herum"""
    pronom = pronom.lower()
    if(pronom == "ich"): #ich du
        return "du"
    elif(pronom == "du"):
        return "ich"
    elif(pronom == "mich"): # mich dich
        return "dich"
    elif(pronom == "dich"):
        return "mich"
    elif(pronom == "dir"): # dir mir
        return "mir"
    elif(pronom == "mir"):
        return "dir"
    elif(pronom == "meine"): # meine deine
        return "deine"
    elif(pronom == "deine"):
        return "meine"
    elif(pronom == "dein"): # dein mein
        return "mein"
    elif(pronom == "mein"):
        return "dein"
    elif(pronom == "meiner"): # meiner deiner
        return "deiner"
    elif(pronom == "meiner"):
        return "deiner"
    elif(pronom == "meinem"): # meinem deinem
        return "deinem"
    elif(pronom == "meinem"):
        return "deinem"
    elif(pronom == "deinen"): # meinen deinen
        return "meinen"
    elif(pronom == "meinen"):
        return "deinen"
    elif(pronom == "deines"): # meines deines
        return "meines"
    elif(pronom == "meines"):
        return "deines"
    else:
        return pronom

def pronomenTauschW(woerterbuch, pronom):
    """Benutzt ein Wörterbuch um ein Pronomen der 1. Person Singular zur 2. Person Singular oder anders herum zu konvertieren."""
    pronom = pronom.lower()
    ergebnisse = woerterbuch.suche(pronom, case=False)

    if(pronom == "ich"):
        return "du"
    elif(pronom == "du"):
        return "ich"
    else:
        weiter = False
        for ergebnis in ergebnisse:
            if("PRO" in ergebnis[2].split(":")):
                weiter = ergebnis

        if(weiter):
            if(weiter[1] in ["der", "die", "das"]):
                return pronom
            elif(pronom[0] == "m"):
                return "d"+pronom[1:]
            elif(pronom[0] == "d"):
                return "m"+pronom[1:]
            else:
                return pronom
        else:
            return pronom

def personFiltern(eigenschaften):
    perz = "1"
    persp = "SIN"
    if("2" in eigenschaften):
        perz = "2"
    elif("3" in eigenschaften):
        perz = "3"
    if("PLU" in eigenschaften):
        persp = "PLU"
    return persp + ":" +  perz

def zeitFilten(eigenschaften):
    zeit = "PRÄ"
    if("PRT" in eigenschaften):
        zeit = "PRT"
    return zeit

def frageZuAntwort(woerterbuch, frage, case=True):
    """Erstelle eine Antwort aus einer Frage. Beispiel: wer bist du -> ich weiß nicht, wer ich bin"""
    frageLower = frage.lower()
    
    frageNeu = ""
    chars = "abcdefghijklmnopqrstuvwxyzßöäü 1234567890?!."
    for i in range(0, len(frage)):
        if(frageLower[i] in chars):
            frageNeu += frage[i]

    frage = frageNeu
    while("  " in frage):
        frage = frage.replace("  ", " ")

    fragen = frage.replace("!", ".").replace("?", ".").replace(" und ", ".").replace(" oder ", ".").split(".")
    fragen = list(filter(None, fragen))

    arten = []
    antworten = []

    for i in range(0, len(fragen)):
        person = "SIN:2"
        zeit = "PRÄ"
        frw = "ob"
        px = True
        vx = True

        if(fragen[i][0] == " "):
            fragen[i] = fragen[i][1:]
        fragen[i] = fragen[i].strip()
        fragen[i] = fragen[i].split(" ")

        arten.append([])
        antworten.append("")
        iz = 0
        for wort in fragen[i]:
            iz += 1
            if(wort.lower() in frws and iz < 4):
                frw = wort.lower()
                arten[-1].append(["PRO"])
            else:
                ergebnis = woerterbuch.suche(wort, case=True)
                if not(ergebnis):
                    ergebnis = woerterbuch.suche(wort, case=False)
                if(ergebnis):
                    ergebnis = ergebnis[0]
                    arten[-1].append(ergebnis[2].split(":"))
                    if("PRO" in arten[-1][-1]):
                        neuPronom = pronomenTauschW(woerterbuch, wort)
                        antworten[-1] += neuPronom + " "
                        if(px and not("ART" in arten[-1][-1])):
                            nergebnis = woerterbuch.suche(neuPronom, case=False)
                            if(nergebnis):
                                person = personFiltern(nergebnis[0][2].split(":"))
                                px = False
                    
                    elif("VER" in arten[-1][-1]):
                        if(vx):
                            vx = False
                            zeit = zeitFilten(arten[-1][-1])
                            if(px):
                                person = personFiltern(arten[-1][-1])
                                if(person == "SIN:2"):
                                    person = "SIN:1"
                                elif(person == "SIN:1"):
                                    person = "SIN:2"
                                px = False
                        else:
                            antworten[-1] += wort + " "
                    else:
                        antworten[-1] += wort + " "
                    if("VOR" in arten[-1][-1] or "NAC" in arten[-1][-1]):
                        if(px):
                            person = "SIN:3"
                            px = False
                else:
                    if(wort[0].upper() == wort[0] and case):
                        arten[-1].append(["SUB"])
                        antworten[-1] += wort + " "
                    elif not(case):
                        antworten[-1] += wort + " "
                        arten[-1].append(ergebnis)
                    else:
                        arten[-1].append(ergebnis)
        
        for j in range(0, len(arten[-1])):
            if(arten[-1][j]):
                if("VER" in arten[-1][j]):
                    konj = woerterbuch.konjugiere(fragen[i][j], person, zeit)
                    if(konj):
                        antworten[-1] += konj + " "
                        break
        
        antworten[-1] = "Ich weiß nicht, " + frw + " " + antworten[-1].strip()
    
    antwort = ""
    for i in range(0, len(antworten)):
        if(i/2 == int(i/2)):
            antwort += antworten[i]
            if(i == len(antworten) - 1):
                antwort += "."
            else:
                antwort += " und "
        else:
            antworten[i] = antworten[i][0].lower() + antworten[i][1:]
            antwort += antworten[i] + ". "
    return antwort