#!/usr/bin/python
# -*- coding: utf-8 -*-

class jobResult(object):

    def __init__ (self, command, result, execTime):
        self.command = command
        self.execTime = execTime
        self.result = result

    
    def toXML(self):


        str = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n"
        str += "    <jobResult xmlns=\"http://www.w3.org/2001/XMLSchema-instance\" noNamespaceSchemaLocation=\"jobresult.xsd\">\n"
        str += "        <command>"+ self.command + "</command>\n"
        str += "        <execTime>" + self.execTime[:-2] + "</execTime>\n"
        str += "        <result>" + self.result + "</result>\n"
        str += "    </jobResult>" 


        return str
