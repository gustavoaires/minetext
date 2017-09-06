# -*- coding: latin-1 -*-
#Desenvolvido por Adail Carvalho
#Twitter: @Adail_Carvalho
#Git: AdailCarvalho

import csv
import sys
import os
import random
from os import system
from coordinateformater import*
from portugueseprocessor import*
from datetime import date

class TextProcess():
        def __init__(self):
            self.output_file = 0
            self.day = 0
            self.clean = TextCleaner()
            self.named = NamedEntity()
            self.regex = RegexpReplacer()
            self.points = CoordinateFormater()
            self.reader = 0
   
        def processTwitterText(self, file):
            self.reader = csv.DictReader(file, delimiter = '\t')
            self.day = date.today()
            self.output_file = open('C:/Users/jose.adail/workspace/TextProcessor/output/tweets_%s.tsv' %self.day,'a')
            
            for line in self.reader:
                try:
                    text = line["text"]
                    latLon = line["coordinates"]
                    latLon = self.points.formatCoordinate(latLon)
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
                    row = line["id"]+"\t"+(text).encode('latin-1','ignore')+"\t"+(lat)+"\t"+(lon)+"\n"
                    self.output_file.write(row)

                except (UnicodeDecodeError, csv.Error, AttributeError, KeyError) as e:
                        print e, "\n"
                        print "Header label: id    text    coordinates"
            self.output_file.close()
                
        def processFacebookText(self,file):
                self.reader = csv.DictReader(file, delimiter = '\t')
                self.day = date.today()
                self.output_file = open('C:/Users/jose.adail/workspace/TextProcessor/output/comments_%s.tsv' %self.day,'a')

                for line in self.reader:
                    try:
                        text = line["text"]
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
                        row = line["sentiment"]+"\t"+line["id"]+"\t"+(text).encode('latin-1','ignore')+"\n"
                        self.output_file.write(row)
                    
                    except(UnicodeDecodeError, csv.Error, AttributeError, KeyError) as e:
                            print e, "\n"
                            print "Header label: id    text"
                self.output_file.close()
                
        def createTrainingSet(self,file):
                self.reader = csv.DictReader(file, delimiter = '\t')
                rand = []
                num = 0
                count = 1
                for i in range(1000):
                        num = random.randrange(1,605)
                        rand.append(num)
                for line in self.reader:
                        try:
                                text = line["text"]
                                for i in range(len(rand)-1):
                                        if rand[i]==count:
                                                print line["id"]+"\t",
                                                print (text).encode('latin-1','ignore')
                                                break
                        except (UnicodeDecodeError, csv.Error, AttributeError, KeyError) as e:
                                print e, "\n"
                                print "Header label: id    text"
                        count+=1
                        
        def processName(self,file):
                self.reader = csv.DictReader(file, delimiter = '\t')
                self.output_file = open('C:/Users/jose.adail/workspace/TextProcessor/names/tagged_names.txt','a')
                for line in self.reader:
                        try:
                                text = line["name"]
                                text = self.clean.removeOneCharacter(text)
                                text = self.clean.removeAccent(text) # Remover acentos
                                text = self.named.tokenizeWords(text)
                                for n in text:
                                        if n != "":
                                                n = (n).encode('latin-1','ignore')
                                                self.output_file.write(n+"_NPROP\n")
                        except (UnicodeDecodeError, csv.Error, AttributeError, KeyError) as e:
                                print e, "\n"
                                print "Header label: name    name_tag"

                for line in self.reader:
                        try:
                                text = line["name_tag"]
                                text = self.clean.removeOneCharacter(text)
                                text = self.clean.removeAccent(text) # Remover acentos
                                text = self.named.tokenizeWords(text)
                                for n in text:
                                        if n != "":
                                                n = (n).encode('latin-1','ignore')
                                                self.output_file.write(n+"_NPROP\n")
                        except (UnicodeDecodeError,csv.Error,AttributeError,KeyError) as e:
                                print e, "\n"
                self.output_file.close()
        
        def menu(self):
            print "__________________________________________"
            print "-*-Text Processor -*-"
            print "__________________________________________"
            print "1. Create Training Set"
            print "2. Process Twitter Text"
            print "3. Process Facebook Text"
            print "4. Process Names"
            print "5. About"
            print "6. Exit"        
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
                
        def openCSV(self,path):
                if os.path.exists(path):
                        with open(path,"rU") as file:
                                opt = ''
                                system('cls')
                                self.menu()
                                opt = str(raw_input("Select: "))
                                if opt == '1':
                                    self.createTrainingSet(file)
                                    system('pause')
                                    system('cls')
                                    
                                if opt == '2':
                                    self.processTwitterText(file)
                                    system('pause')
                                    system('cls')
                                    
                                if opt == '3':
                                    self.processFacebookText(file)
                                    system('pause')
                                    system('cls')
                                    
                                if opt == '4':
                                    self.processName(file)
                                    system('pause')
                                    system('pause')
                                    
                                if opt == '5':
                                    system('cls')
                                    self.showInfo()
                                    system('pause')
                            
                                if opt == '6':
                                    print "Exit..."
                                    system('pause')
                                    system('cls')                
                                    
                else:                
                        print "Arguments: [file separetade by TAB]"
                   

tp = TextProcess()
file =sys.argv[1]
if __name__ == "__main__":
        system('cls')
        tp.openCSV(file)