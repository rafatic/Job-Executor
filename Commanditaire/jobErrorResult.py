#!/usr/bin/python
# -*- coding: utf-8 -*-


import xml.etree.ElementTree as ET

class jobErrorResult(object):

    def __init__ (self):
        self.type = ''
        self.code = ''
        self.message = ''

    
    def XmlToObject(self, XMLString):
        
        root = ET.fromstring(XMLString)

        for type in root.iter("{http://www.w3.org/2001/XMLSchema-instance}type"):
            
            self.type = type.text

        for code in root.iter("{http://www.w3.org/2001/XMLSchema-instance}code"):
            
            self.code = code.text

        for message in root.iter("{http://www.w3.org/2001/XMLSchema-instance}message"):
            
            self.message = message.text
        

    def toString(self):
        string = "";
        if self.type != None :
            string += "Erreur : " + self.type + "\n"
        else:
            string += "Erreur : Inconnue \n"

        if self.code != None :
            string += "Code de sortie : " + self.code + "\n"
        else:
            string += "Code de sortie : Inconnu \n"

        if self.message != None:
            string += "Message : " + self.message + "\n"
        else:
            string += "Message : Aucun \n"
        return string;