#!/usr/bin/python
# -*- coding: utf-8 -*-


import xml.etree.ElementTree as ET


class jobRequest(object):


    def __init__ (self):
        self.command = ''
        self.args = ''
        self.url = ''
        self.path = ''
        self.login = ''
        self.password = ''
        self.sender = ''

    
    def XmlToObject(self, XMLString):
        root = ET.fromstring(XMLString)




        for command in root.iter("{http://www.w3.org/2001/XMLSchema-instance}command"):
            
            self.command = command.text

        for args in root.iter("{http://www.w3.org/2001/XMLSchema-instance}args"):
            
            self.args = args.text
  
        for datasource in root.iter("{http://www.w3.org/2001/XMLSchema-instance}datasource"):
            
            for url in datasource.iter("{http://www.w3.org/2001/XMLSchema-instance}url"):
                self.url = url.text

            for path in datasource.iter("{http://www.w3.org/2001/XMLSchema-instance}path"):
                self.path = path.text

            for login in datasource.iter("{http://www.w3.org/2001/XMLSchema-instance}login"):
                self.login = login.text

            for password in datasource.iter("{http://www.w3.org/2001/XMLSchema-instance}password"):
                self.password = password.text
        
        for sender in root.iter("{http://www.w3.org/2001/XMLSchema-instance}from"):
            
            self.sender = sender.text
        

    def toString(self):
        str = "";
        if self.command != None :
            str += "Commande : " + self.command + "\n"
        else:
            str += "Commande : Aucune \n"

        if self.args != None :
            str += "Arguments : " + self.args + "\n"
        else:
            str += "Arguments : Aucuns \n"

        if self.url != None:
            str += "Datasource : " + self.url + "\n"
        else:
            str += "Datasource : Aucune \n"

        if self.url != None:
            str += "Chemin : " + self.path + "\n"
        else:
            str += "Chemin : Aucun \n"

        if self.login != None:
            str += "login : " + self.login + "\n"
        else:
            str += "login : Aucune \n"

        if self.password != None:
            str += "password : " + self.password + "\n"
        else:
            str += "password : Aucune \n"

        str += "Emmiteur : " + self.sender + "\n"

        return str;


        

        
            
        
        


