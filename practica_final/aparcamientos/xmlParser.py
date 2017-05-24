from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from urllib.request import urlopen
import sys
import os.path
import string


def normalize_whitespace(texto):
    return str.join(' ',str.split(texto))

class myContentHandler(ContentHandler):

    def __init__ (self):
        #NOMBRE DESCRIPCION ACCESIBILIDAD CONTENT-URL
        #NOMBRE-VIA CLASE-VIAL NUM CODIGO-POSTAL BARRIO DISTRITO LATITUD LONGITUD
        self.inContent = False 
        self.theContent = ""
        self.atributo = ""
        self.nombre = ""
        self.descripcion = ""
        self.access = ""
        self.url = ""
        self.nombreVia = ""
        self.num = ""
        self.codigo = ""
        self.barrio = ""
        self.distrito = ""
        self.latitud = ""
        self.longitud = ""
        self.email = ""
        self.telefono = ""
        self.listDic = [] #Lista de diccionarios, uno por cada aparcamiento
        self.dic = {}


    def startElement (self, name, attrs):
        if name == "atributo":
            self.atributo = normalize_whitespace(attrs.get('nombre'))
        if self.atributo in ['NOMBRE','DESCRIPCION','ACCESIBILIDAD','CONTENT-URL','NOMBRE-VIA','NUM','CODIGO-POSTAL','BARRIO','DISTRITO','LATITUD','LONGITUD','TELEFONO','EMAIL']:
            self.inContent = True

    def endElement (self, name):
        if self.inContent:
            self.theContent = normalize_whitespace(self.theContent)

        if self.atributo == 'NOMBRE':
            self.nombre = self.theContent
            self.dic[self.atributo] = self.nombre

        elif self.atributo == 'DESCRIPCION':
            self.descripcion = self.theContent
            self.dic[self.atributo] = self.descripcion

        elif self.atributo == 'ACCESIBILIDAD':
            if self.theContent == '1':
                self.access = 'SI'
            else:
                self.access = 'NO'

            self.dic[self.atributo] = self.access

        elif self.atributo == 'CONTENT-URL':
            self.url = self.theContent
            self.dic[self.atributo] = self.url

        elif self.atributo == 'NOMBRE-VIA':
            self.nombreVia = self.theContent
            self.dic[self.atributo] = self.nombreVia

        elif self.atributo == 'NUM':
            self.num = self.theContent
            self.dic[self.atributo] = self.num

        elif self.atributo == 'CODIGO-POSTAL':
            self.codigo = self.theContent
            self.dic[self.atributo] = self.codigo

        elif self.atributo == 'BARRIO':
            self.barrio = self.theContent
            self.dic[self.atributo] = self.barrio

        elif self.atributo == 'DISTRITO':
            self.distrito = self.theContent
            self.dic[self.atributo] = self.distrito

        elif self.atributo == 'LATITUD':
            self.latitud = self.theContent
            self.dic[self.atributo] = self.latitud

        elif self.atributo == 'LONGITUD':
            #self.longitud = self.theContent
            self.dic[self.atributo] = self.theContent

        elif self.atributo == 'TELEFONO':
            #self.telefono = self.theContent
            self.dic[self.atributo] = self.theContent
        elif self.atributo == 'EMAIL':
            #self.email = self.theContent
            self.dic[self.atributo] = self.theContent
            
        elif name == 'contenido':            
            self.listDic.append(self.dic)
            self.dic = {}
            self.nombre = ""
            self.descripcion = ""
            self.access = ""
            self.url = ""
            self.nombreVia = ""
            self.num = ""
            self.codigo = ""
            self.barrio = ""
            self.distrito = ""            
            self.latitud = ""
            self.longitud = ""  
            self.telefono = ""
            self.email = ""
        self.inContent = False
        self.theContent = ""

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars


    def getLista(self):
        return self.listDic

      
# Load parser and driver

"""
theParser = make_parser()
theHandler = myContentHandler()
theParser.setContentHandler(theHandler)

# Ready, set, go!

xmlFile = urlopen('http://datos.munimadrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=202584-0-aparcamientos-residentes&mgmtid=e84276ac109d3410VgnVCM2000000c205a0aRCRD&preview=full')
theParser.parse(xmlFile)

lista = theHandler.getLista()
print(lista)
print ("Parse complete")

"""