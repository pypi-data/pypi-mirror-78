# woerterbuch.py - Importiere und nutze Wörterbücher
# Copyright 2020 Jakob Stolze <https://github.com/jarinox>

import os as _os
import csv as _csv


class Abkuerzungen:
    def __init__(self):
        self.verzeichnis = {
            "ABK": "Abkürzung",
            "ADJ": "Adjektiv",
            "ADV": "Adverb",
            "AKK": "Akkussativ",
            "ART": "Artikel",
            "ATT": "attributiv",
            "AUX": "Hilfsverb",
            "BEG": "begleitend",
            "B/G": "begleitend und stellvertretend",
            "CAU": "kausal",
            "COU": "Land",
            "DAT": "Dativ",
            "DEF": "bestimmt",
            "DEM": "Demonstrativpronomen",
            "EIG": "Eigenname",
            "EIZ": "erweiterter Infinitif mit zu",
            "FEM": "femininum",
            "GEB": "Gebiet",
            "GEN": "Genitiv",
            "GEO": "geographischer Eigenname",
            "GRU": "Grundform",
            "IND": "unbestimmt",
            "INF": "Infinitiv",
            "INJ": "Interjektion",
            "IMP": "Imperativ",
            "INR": "Interrogativpronomen",
            "KJ1": "Konjunktiv 1",
            "KJ2": "Konjunktiv 2",
            "KMP": "Kompositum",
            "KON": "Konjunktion",
            "LOK": "lokal",
            "MAS": "maskulinum",
            "MOD": "modal",
            "MOU": "Gebierge",
            "NAC": "Nachname",
            "NEB": "nebenordnend",
            "NEG": "Neptionspartikel",
            "NEU": "neutrum",
            "NIL": "Wortform nicht gefunden",
            "NOA": "ohne Artikel",
            "NOG": "ohne Genus",
            "NOM": "Nominativ",
            "NON": "nicht-schwach",
            "PA1": "Partizip 1",
            "PA2": "Partizip 2",
            "PER": "personal",
            "PLU": "plural",
            "POS": "possesiv",
            "PRÄ": "Präsens",
            "PRD": "prädikativ",
            "PRI": "proporional",
            "PRO": "Pronomen",
            "PRP": "Präposition",
            "PRT": "Präteritum, Imperfekt",
            "REF": "reflexiv",
            "REL": "relativ",
            "RIN": "relativ oder interrogativ",
            "SFT": "schwach",
            "SIN": "singular",
            "SOL": "alleinstehend",
            "STD": "Stadt",
            "STV": "stellvertretend",
            "SUB": "Substantiv",
            "SUP": "Superlativ",
            "SZ": "Satzzeichen",
            "SZE": "Satzendezeichen",
            "SZK": "Komma",
            "SZT": "Satztrennzeichen",
            "TMP": "temporal",
            "UNT": "unterordnend",
            "VER": "Verb",
            "VGL": "vergleichend",
            "VOR": "Vorname",
            "WAT": "Gewässer",
            "ZAL": "Zahlwort",
            "ZAN": "Zahl bzw Ziffernfolge",
            "ZUS": "Verbzusatz",
            "1": "1. Person",
            "2": "2. Person",
            "3": "3. Person",
            "A": "höflich",
            "B": "vertraut",
        }

    def info(self, abk):
        """Gibt die Bedeutung einer Abkürzung zurück."""
        if(abk in self.verzeichnis.keys()):
            return self.verzeichnis[abk]
        else:
            return False

class Woerterbuch:
    """Diese Klasse ermöglicht das Importieren und Benutzen von Wörterbuch Datenbanken."""
    def __init__(self, path=_os.path.dirname(__file__)+"/data/german.csv"):
        self.path = path
        self.importieren()
    
    def importieren(self):
        """Importiere ein Wörterbuch."""
        csvfile = open(self.path, "r")
        re = _csv.reader(csvfile)
        self.db = list(re)
    
    def suche(self, wort, case=True):
        """Durchsuche das Wörterbuch nach einem Wort."""
        wortLower = wort.lower()
        treffer = []
        for item in self.db:
            if(case):
                if(item[0] == wort):
                    treffer.append(item)
            else:
                if(item[0].lower() == wortLower):
                    treffer.append(item)
        if(treffer == []):
            treffer = False
        return treffer
    
    def konjugiere(self, verb, person, zeit, kj=0):
        """Konjugiere ein Verb."""
        ergebnis = self.suche(verb.lower())
        if(ergebnis):
            istVerb = False
            for wort in ergebnis:
                if("VER" in wort[2].split(":")):
                    istVerb = True
                    grundform = wort[1]

                    person = person.upper().split(":")
                    zeit = zeit.upper()

                    ergebnisse = []
                    for item in self.db:
                        if(item[1] == grundform):
                            eig = item[2].split(":")
                            if(person[0] in eig and person[1] in eig and zeit in eig):
                                ergebnisse.append(item)
                    
                    if(len(ergebnisse) == 1):
                        return ergebnisse[0][0]
                    elif(len(ergebnisse) > 1):
                        e2 = []
                        if(kj == 0):
                            for ergebnis in ergebnisse:
                                eig = ergebnis[2].split(":")
                                if not("KJ1" in eig or "KJ2" in eig):
                                    e2.append(ergebnis)
                        else:
                            for ergebnis in ergebnisse:
                                eig = ergebnis[2].split(":")
                                if("KJ"+str(kj) in eig):
                                    e2.append(ergebnis)
                        if(len(e2) == 0):
                            return ergebnisse[0][0]
                        else:
                            return e2[0][0]
            
            if istVerb:
                print("gmrde: Zeit und/oder Person nicht gefunden")
            else:
                print("gmrde: nur Verben können konjugiert werden")
            
            return False
        else:
            print("gmrde: Verb nicht gefunden")
            return False

