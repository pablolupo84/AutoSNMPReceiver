#!/usr/bin/env python

import configparser,os

"""
Descripcion: Modulo que permite manipular archivos de configuracion.
Autor: Autotrol PL - Sistemas
Version: 0.1
"""

class config:
    """Modulo que permite manejar archivo de configuracion"""    
    def __init__(self,config_file):
        self.__config_file = config_file
        self.__config = configparser.ConfigParser()
        self.__config.read(self.__config_file)  
        
    def ShowItemSection(self,section):
        return self.__config.items(section)
    
    def ShowValueItem(self,section,key_word):
        return self.__config.get(section,key_word)
    
    def change(self,section,key_word,value):
        self.__config.set(section,key_word,value)

    def write(self):
        self.__config.write(open(self.__config_file,'w'))

# TEST clase_config.py
#configuracion=config('../config.ini')
#items=configuracion.ShowItemSection('TRANSPORT_SETUP')
#print (items)
# print (configuracion.ShowValueItem('TESTING','DB_NAME'))
# configuracion.change('TESTING','DB_NAME','Peloncho')
# print (configuracion.ShowValueItem('TESTING','DB_NAME'))
# configuracion.write()