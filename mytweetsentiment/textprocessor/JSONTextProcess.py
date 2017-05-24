# -*- coding: latin-1 -*-
#Desenvolvido por Adail Carvalho
#Twitter: @Adail_Carvalho
#Git: AdailCarvalho

import sys
import os
import re 
import json
from os import system
from CoordinateFormater import*
from PortugueseProcess import*
from datetime import date

class TextProcess():
    def __init__(self):
        self.output_file = 0
        self.day = 0
        self.clean = TextCleaner()
        self.named = NamedEntity()
        self.regex = RegexpReplacer()
        self.points = CoordinateFormater()
        self.json_data = []

    def processTwitterText(self, file):
        self.day = date.today()
        self.output_file = open('C:/Users/jose.adail/workspace/TextProcessor/mahout/tweets_%s.tsv' %self.day,'a')
        for line in file:
            try:
                self.json_data.append(json.loads(line))
            except (UnicodeDecodeError, UnicodeEncodeError, TypeError,AttributeError,KeyError, ValueError) as e:
                print e, "\n"

        for d in self.json_data:
            try:
                id = d['id']
                text = d['text']
                latLon = d['coordinates']
                latLon = self.points.formatCoordinate(str(latLon))
                lat = latLon[0]
                lon = latLon[1]
                text = self.clean.removeLinks(text)
                text = self.clean.removeAccent(text)
                text = self.named.removeTwitterUsername(text)
                text = self.regex.replaceEmoticon(text)
                text = self.clean.removeRepChar(text)
                text = self.clean.normalizeDigraph(text)
                text = self.named.removePersonName(text)
                text = text.lower()
                text = self.clean.removeSymbols(text)
                text = self.clean.removeStopwords(text)
                text = self.clean.removeOneCharacter(text)
                text = self.clean.removeSufPort(text)
                text = self.clean.normalizeText(text)
                row = str(id)+"\t"+(text).encode('latin-1','ignore')+"\t"+ str(lat) + "\t" + str(lon) + "\n"
                self.output_file.write(row)

            except (UnicodeDecodeError, UnicodeEncodeError, TypeError,AttributeError,KeyError) as e:
                    print e, "\n"
        self.output_file.close()

    def processFacebookText(self, file):
        self.day = date.today()
        self.output_file = open('C:/Users/jose.adail/workspace/TextProcessor/mahout/comments_%s.tsv' %self.day,'a')
        for line in file:
            try:
                self.json_data.append(json.loads(line))
            except(UnicodeDecodeError, UnicodeEncodeError, TypeError,AttributeError,KeyError, ValueError) as e:
                print e, "\n"

        for d in self.json_data:
            try:
                id = d['id']
                text = d['text']
                text = self.clean.removeLinks(text)
                text = self.clean.removeAccent(text)
                text = self.regex.replaceEmoticon(text)
                text = self.clean.removeRepChar(text)
                text = self.clean.normalizeDigraph(text)
                text = self.named.removePersonName(text)
                text = text.lower()
                text = self.clean.removeSymbols(text)
                text = self.clean.removeStopwords(text)
                text = self.clean.removeOneCharacter(text)
                text = self.clean.removeSufPort(text)
                text = self.clean.normalizeText(text)
                row = str(id) + "\t"+(text).encode('latin-1','ignore')+"\n"
                self.output_file.write(row)

            except(UnicodeDecodeError, UnicodeEncodeError, TypeError,AttributeError,KeyError, ValueError) as e:
                    print e, "\n"
        self.output_file.close()

    def menu(self):
        print "__________________________________________"
        print "-*-Text Processor -*-"
        print "__________________________________________"
        print "1. Process Twitter Text"
        print "2. Process Facebook Text"
        print "3. About"
        print "4. Exit"
        print "__________________________________________"

    def showInfo(self):
        print "__________________________________________"
        print "-*-Text Processor -*-"
        print "__________________________________________"
        print "Developed by Adail Carvalho"
        print "Twitter: @Adail_Carvalho"
        print "E-mail: adail.dux@gmail.com"
        print "December, 2014"
        print "__________________________________________"

    def JSONParser(self,json_file):
        if os.path.exists(json_file):
            with open(json_file) as file:
                opt = ''
                system('cls')
                self.menu()
                opt = str(raw_input("Select: "))

                if opt == '1':
                    self.processTwitterText(file)
                    system('pause')
                    system('cls')

                if opt == '2':
                    self.processFacebookText(file)
                    system('pause')
                    system('cls')

                if opt == '3':
                    system('cls')
                    self.showInfo()
                    system('pause')

                if opt == '4':
                    print "Exit..."
                    system('pause')
                    system('cls')

        else:
                print "Arguments: [JSON File]"

tp = TextProcess()
json_file =sys.argv[1]
if __name__ == "__main__":
    system('cls')
    tp.JSONParser(json_file)
