#!/usr/bin/python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET


class jobResult(object):

    def __init__ (self):
        self.command = ''
        self.execTime = ''
        self.result = ''

    def XmlToObject(self, XMLString):
        
        root = ET.fromstring(XMLString)
        
        for command in root.iter("{http://www.w3.org/2001/XMLSchema-instance}command"):
            
            self.command = command.text

        for execTime in root.iter("{http://www.w3.org/2001/XMLSchema-instance}execTime"):
            
            self.execTime = float(execTime.text)

        for result in root.iter("{http://www.w3.org/2001/XMLSchema-instance}result"):
            
            self.result = int(result.text)

    
    def toString(self):
        string = "";
        if self.command != None :
            string += "Commande : " + self.command + "\n"
        else:
            string += "Commande : Aucune \n"

        if self.execTime != None :
            string += "Temps d'exécution : " + str(self.execTime) + "\n"
        else:
            string += "Temps d'execution : Aucun \n"

        if self.result != None:
            string += "resultat : " + str(self.result) + "\n"
        else:
            string += "resultat : Aucun \n"
        return string;


        

        
            
        
        


