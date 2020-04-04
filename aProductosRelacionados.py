#import BUSCADOR_DE_LISTA
from bs4 import BeautifulSoup
import requests
import time
import json
from os import makedirs
from datetime import date, timedelta
from io import open 
import os
#import xlsxwriter

class Informacion:
    def _init_(self):
        pass
######
###### Obtiene los datos de un producto en concreto
######
    def datos(self, urlCategoria, numDeLaLista, urlProducto, marca):
        # blnDevelopment habilito chivatos de dev
        blnDevelopment = 1
        
        #### exportar datos al excel. creamos el CSV
        path = "C:\\Users\\rpr\\Desktop\\WebScrapingMudular\\Datos\\Errores\\"
    
        os.makedirs(path, exist_ok = True) # store image in ./nombreCarpeta

        archivo = open(path  + "Productos_Relacionados_" + str(marca) + ".csv",  "a")

        archivo.write(marca)
        archivo.write("@") #cambio de columna
        archivo.write(urlCategoria)
        archivo.write("@") #cambio de columna
        archivo.write(str(numDeLaLista))
        archivo.write("@") #cambio de columna
        archivo.write(urlProducto)
        archivo.write("@") #cambio de columna
        archivo.write("\n") #cambio de fila (salto)

        archivo.close()