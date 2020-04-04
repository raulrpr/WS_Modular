import requests
import aInformacionProducto
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
from os import makedirs
from datetime import date, timedelta
import aProductosRelacionados

class Informacion:
    def _init_(self):
        pass

    def datos(self, newUrlCategoria, numDeCategoria, numProductosDeCategoria, marca):
        # blnDevelopment habilito chivatos de dev
        blnDev = 1
        MAX_PAGES = 20
        counter = 0
        intNumePagNext = 1
        NewUrlNext = ""

        url = newUrlCategoria #"https://www.sp-recambios.es/es/b/ina/bearing-thrust-ball-bearing" #URL_BASE + Marca  
        blnProductos = 1  # 1- hay productos 0- No hay productos
        intNumUrlProductosTOTALES  = 0
        intNumlProductosDeCategoria  = 0
        intprevious = 0

        lstventanaDeListado = []
        numDeVentanasDelst = (numProductosDeCategoria / 15)
        iteradorDeVentanasDelst = 0

        while (blnProductos == 1) and (numDeVentanasDelst > iteradorDeVentanasDelst):
            iteradorDeVentanasDelst = iteradorDeVentanasDelst + 1
            # Realizamos la petición a la web
            req = requests.get(url)
            # Comprobamos que la petición nos devuelve un Status Code = 200
            statusCode = req.status_code
            if statusCode == 200:
                # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
                html = BeautifulSoup(req.content, "html.parser")
                ###############
                links2 = html.find_all('td', {'class': 'nowrap-cell'})
                ##Recorro todos los productos de la pagina (aprx. hay 15 por pantalla)
                for num in range(len(links2)):    
                    if num%2 == 0: 
                        urlProducto = links2[num].contents[1].attrs['href']
                        
                        intNumUrlProductosTOTALES = intNumUrlProductosTOTALES + 1
                        #caso de algunas listas de categorias con un formato diferente
                        if (urlProducto == "javascript:void(0);"):
                            urlProducto = links2[num].contents[1].attrs['data-url']
                            inst2 = aProductosRelacionados.Informacion()
                            inst2.datos(url, num, urlProducto, marca) #urlCategoria, Num de la lista de productos,
                            print("**** Producto relacionado ****") 
                        else:
                            # llamada para procesar cada producto, WrappingProduct(urlProducto)
                            inst = aInformacionProducto.Informacion()
                            inst.datos(urlProducto)
                            print("\tLlamo a aInformacionProducto ")

                        if (blnDev == 1):
                            print("------------------------------------------------------------------ ")
                            print("1º numDeCategoria= %i, numDeVentanasDelst: %i, newUrlCategoria= %s" % (numDeCategoria, numDeVentanasDelst, newUrlCategoria))
                            print("2º Producto Num: %i, Pagina de lista de producto= %s" % (num ,url))
                            print("3º NumProducto Totales de la categoria: %i, urlProducto= %s" % (intNumUrlProductosTOTALES ,urlProducto))
                            print("------------------------------------------------------------------ ")
                            time.sleep(0.1)
                ##############
                links3 = html.find_all('div', {'class': 'col-md-12 col-sm-12'})
                ## Busco la url del boton "Siguiente" para obtener el resto 
                if (len(links3[0].contents[3].contents) == 1 ): # cuando no hay nada hay un: /t
                    estatushiddenBotonNext = "Solo hay una pagina en la lista"
                else:   
                    estatushiddenBotonNext = links3[0].contents[3].contents[len(links3[0].contents[3].contents) - 2].attrs['class'][0]

                if (estatushiddenBotonNext == "next"):
                    NewUrlNext = links3[0].contents[3].contents[len(links3[0].contents[3].contents) - 2].contents[1].attrs['href']
                    ## Añado a la lista la url del lisdado de los productos
                    lstventanaDeListado.append(url) 
                    
                    if NewUrlNext in lstventanaDeListado:
                        blnProductos = 0
                        print("\t\t **No hay más productos en el buscador.   TOTAL DE PRODUCTOS:", intNumUrlProductosTOTALES)
                        print("\t\t **Pag numero:", intNumePagNext)
                    else:
                        intNumePagNext = intNumePagNext + 1
                        url = NewUrlNext

                    if (blnDev == 1):
                        print("\t\t **********************")
                        print("\t\t Nueva Url 'Siguiente'= ", NewUrlNext)
                        print("\t\t Pag numero:", intNumePagNext)
                        print("\t\t **********************")                    
                    
                else:
                    blnProductos = 0
                    if (blnDev == 1):
                        print("\t\t No hay más productos en el buscador.   TOTAL DE PRODUCTOS:", intNumUrlProductosTOTALES)
                        print("\t\t Pag numero:", intNumePagNext)
                ##############