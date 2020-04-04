#import BUSCADOR_DE_LISTA
from bs4 import BeautifulSoup
import requests
import time
import json
from os import makedirs
from datetime import date, timedelta
from io import open 
import os


class Informacion:

    def _init_(self):
        pass
######
###### Obtiene los datos de un producto en concreto
######
    def datos(self, NewUrl):

        # blnDevelopment habilito chivatos de dev
        blnDevelopment = 1
        
        # List of saved image file names
        imagesFileNames = []

        # Format the url depending on the Manufacterer
        url = NewUrl # "https://www.sp-recambios.es/es/p/rcsmb3-4-65-ina"  # "https://www.sp-recambios.es/es/p/mrw65-a-g2-v1-schneeberger?_q=Schneeberger"

        #Requesting the url
        req = requests.get(url)
        time.sleep(0.1)
        req.raise_for_status()

        if (blnDevelopment == 1):
            print("\tRequesting: ", url)
            print("\tHTML result = ", req.status_code)


        soup = BeautifulSoup(req.text, 'html.parser')
        # print("\t\tHTML soup: = ", soup)
        # Obteniendo el json
        jsonElem = soup.find('script', {'type': 'application/ld+json'})
         
        # print("\t\tHTML jsonElem = ", jsonElem)
        # Obteniendo el data del json
        referencia      = json.loads(jsonElem.text)["mpn"]
        marca           = json.loads(jsonElem.text)["name"].replace(referencia+" ", "", 1)   
        identificador   = referencia + "-"+  marca
        categoria       = json.loads(jsonElem.text)["category"]
        description     = json.loads(jsonElem.text)["description"]  ## quiero el peso
        imageUrl        = json.loads(jsonElem.text)["image"] 

        # Obteniendo el data "price" en €
        offers = json.loads(jsonElem.text)["offers"][0]
        price = offers["price"]
        priceCurrency = offers["priceCurrency"]
        availability = offers["availability"]
        priceValidUntil = offers["priceValidUntil"]
        # Obteniendo el data "price" en  $
        offers = json.loads(jsonElem.text)["offers"][1]
        price1 = offers["price"]
        priceCurrency1 = offers["priceCurrency"]
        availability1 = offers["availability"]
        priceValidUntil1 = offers["priceValidUntil"]
        # Obteniendo el data "price" en libra
        offers = json.loads(jsonElem.text)["offers"][2]
        price2 = offers["price"]
        priceCurrency2 = offers["priceCurrency"]
        availability2 = offers["availability"]
        priceValidUntil2 = offers["priceValidUntil"]

        print("#############################")
        print("url Producto =", url)
        print("Referencia =", referencia)
        print("Description =", description )
        print("Marca =", marca)
        print("Price =", price, priceCurrency)
        print("Availability =", availability.split("/",3)[3])
        
        categoria1 = categoria.split(">")
        for num in range(len(categoria1)):    
            subcatgoria = categoria1[num].lstrip()
            print("subcatgoria: %d=", subcatgoria, num)

        #### creamos el CSV
        path = "C:\\Users\\rpr\\Desktop\\WebScrapingMudular\\Datos\\" + marca + "\\"
    
        os.makedirs(path, exist_ok = True) # store image in ./nombreCarpeta

        ## Caso raro 
        subcatgoria = subcatgoria.replace('\xa0', "")
        ###
        ##imageFileName = imageFileName.replace("'\'", "_")
        subcatgoria = subcatgoria.replace("/", "_")
        subcatgoria = subcatgoria.replace("*", "_")
        subcatgoria = subcatgoria.replace('"', "_")
        subcatgoria = subcatgoria.replace(":", "_")
        subcatgoria = subcatgoria.replace("<", "_")
        subcatgoria = subcatgoria.replace(">", "_")
        subcatgoria = subcatgoria.replace("|", "_")

        archivo = open(path  + subcatgoria + ".csv",  "a")
        time.sleep(0.1)
        archivo.write(referencia)
        archivo.write("@") #cambio de columna

        archivo.write(marca)
        archivo.write("@") #cambio de columna
  
        archivo.write(identificador)
        archivo.write("@") #cambio de columna

        categoria1 = categoria.split(">")

        for num in range(len(categoria1)):    
            subcatgoria = categoria1[num].lstrip()
            archivo.write(subcatgoria)
            archivo.write("@") #cambio de columna

        for num2 in range(10-num):  # simpre reservo 10 plazas para las categorias
            archivo.write("@") #cambio de columna

        archivo.write(availability.split("/",3)[3])
        archivo.write("@") #cambio de columna

        archivo.write(str(price))
        archivo.write("@") #cambio de columna
        archivo.write(priceCurrency)
        archivo.write("@") #cambio de columna
        archivo.write(str(price1))
        archivo.write("@") #cambio de columna
        archivo.write(priceCurrency1)
        archivo.write("@") #cambio de columna
        archivo.write(str(price2))
        archivo.write("@") #cambio de columna
        archivo.write(priceCurrency2)
        archivo.write("@") #cambio de columna

        description1 = description.split(".")
        description2 = description1[1].split(", ")
        description2[0]= description1[1].split(", ")[0].lstrip()

        for num in range(len(description2)):    
            archivo.write(description2[num])
            archivo.write("@") #cambio de columna
    
        archivo.write("\n") #cambio de fila (salto)

        archivo.close()

        time.sleep(0.3)

        # Download the image...
        print('\tDownloading image %s...' % imageUrl)
        res = requests.get(imageUrl)
        time.sleep(0.1)
        res.raise_for_status()

        nombreCarpeta = marca + "-" + subcatgoria
       
        carpetaPath = "C:\\Users\\rpr\\Desktop\\WebScrapingMudular\\Datos\\Imagenes\\"
       
        carpetaPathTemp = os.path.join(marca, nombreCarpeta)     

        ## Caso raro 
        carpetaPathTemp = carpetaPathTemp.replace('\xa0', "")
        ###
        ##imageFileName = imageFileName.replace("'\'", "_")
        carpetaPathTemp = carpetaPathTemp.replace("/", "_")
        carpetaPathTemp = carpetaPathTemp.replace("*", "_")
        carpetaPathTemp = carpetaPathTemp.replace('"', "_")
        carpetaPathTemp = carpetaPathTemp.replace(":", "_")
        carpetaPathTemp = carpetaPathTemp.replace("<", "_")
        carpetaPathTemp = carpetaPathTemp.replace(">", "_")
        carpetaPathTemp = carpetaPathTemp.replace("|", "_")
        #path final de la carpeta 
        carpetaPath = os.path.join(carpetaPath, carpetaPathTemp)

        nombreImagen =  referencia + "-" + marca + ".jpg"

        ### Caso raro 
        nombreImagen = nombreImagen.replace('\xa0', "")
        ###
        ##imageFileName = imageFileName.replace("'\'", "_")
        nombreImagen = nombreImagen.replace("/", "_")
        nombreImagen = nombreImagen.replace("*", "_")
        nombreImagen = nombreImagen.replace('"', "_")
        nombreImagen = nombreImagen.replace(":", "_")
        nombreImagen = nombreImagen.replace("<", "_")
        nombreImagen = nombreImagen.replace(">", "_")
        nombreImagen = nombreImagen.replace("|", "_")

        # Save the image to disk..., exist_ok=Truezz        
        os.makedirs(carpetaPath, exist_ok = True) # store image in ./nombreCarpeta
        time.sleep(0.1)
        # Build the file name path...
        imageFileName = os.path.join(carpetaPath , nombreImagen)
        imagesFileNames.append(imageFileName)

        print("\tSaving image to %s..." % imageFileName)

        imageFile = open(imageFileName, 'wb')
        time.sleep(0.2)
        for chunk in res.iter_content(100000):
            imageFile.write(chunk)
        time.sleep(0.1)
        imageFile.close()
