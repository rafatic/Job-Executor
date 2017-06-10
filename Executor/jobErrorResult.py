#!/usr/bin/python
# -*- coding: utf-8 -*-

class jobErrorResult(object):

    def __init__ (self, type, code, message):
        self.type = type
        self.code = code
        self.message = message

    
    def toXML(self):


        str = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n"
        str += "    <error xmlns=\"http://www.w3.org/2001/XMLSchema-instance\" noNamespaceSchemaLocation=\"jobErrorResult.xsd\">\n"
        str += "        <type>"+ self.type + "</type>\n"
        str += "        <code>" + self.code + "</code>\n"
        str += "        <message>" + self.message + "</message>\n"
        str += "    </error>" 


        return str

        

        
            
        
        


