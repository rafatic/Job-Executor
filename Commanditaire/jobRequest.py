#!/usr/bin/python
# -*- coding: utf-8 -*-

class jobRequest(object):
    def __init__ ( self, command, args, datasource, path, login, password, sender):
        self.command = command
        self.args = args
        self.datasource = datasource
        self.path = path
        self.login = login
        self.password = password
        self.sender = sender

    # Construction de la chaine XML à partir d'un objet JobRequest
    # le schéma "jobRequest.xsd" est disponible dans l'archive dans /schemas/
    def toXML(self):

        str = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n"
        str += "    <request xmlns=\"http://www.w3.org/2001/XMLSchema-instance\" noNamespaceSchemaLocation=\"jobrequest.xsd\">\n"
        str += "        <command>"+ self.command + "</command>\n"
        str += "        <args>" + self.args + "</args>\n"
        str += "        <datasource>\n"
        str += "            <url>" + self.datasource + "</url>\n"
        str += "            <path>" + self.path + "</path>\n"
        str += "            <login>" + self.login + "</login>\n"
        str += "            <password>" + self.password + "</password>\n"
        str += "        </datasource>\n"
        str += "        <from>" + self.sender + "</from>\n"
        str += "    </request>" 


        return str


