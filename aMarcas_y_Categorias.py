import requests
from bs4 import BeautifulSoup
import aListadoDeCategoria
import time
import re 


numUrlMarcas = 20 

#RODAMIENTOS

UrlMarcas = ["https://www.sp-recambios.es/es/b/zen"]

            #"https://www.sp-recambios.es/es/b/fag"]
            #"https://www.sp-recambios.es/es/b/ina"]
            #"https://www.sp-recambios.es/es/b/skf"
"""
            "https://www.sp-recambios.es/es/b/zen",
            "https://www.sp-recambios.es/es/b/snr",
            "https://www.sp-recambios.es/es/b/ntn",
            "https://www.sp-recambios.es/es/b/timken",
            "https://www.sp-recambios.es/es/b/generic"]
            """

"""
#LINEAR MOTION
UrlMarcas = ["https://www.sp-recambios.es/es/b/bosch-rexroth",
            "https://www.sp-recambios.es/es/b/thk",
            "https://www.sp-recambios.es/es/b/iko-nippon-thompson-co-ltd-j",
            "https://www.sp-recambios.es/es/b/schneeberger"]
            """
"""
#OTROS PRODUCTOS
            "https://www.sp-recambios.es/es/b/swr",
            "https://www.sp-recambios.es/es/b/permaglide",
            "https://www.sp-recambios.es/es/b/nice",
            "https://www.sp-recambios.es/es/b/torrington",
            "https://www.sp-recambios.es/es/b/durbal-metallwarenfabrik-gmbh-oehringen-d",
            "https://www.sp-recambios.es/es/b/nad",
            "https://www.sp-recambios.es/es/b/dichtomatik",
            "https://www.sp-recambios.es/es/b/dunlop"]
            """

for num in range(len(UrlMarcas)):    
    url = UrlMarcas[num]
    print("\t Paginas de Marcas = ", num, url)
    # Realizamos la petición a la web
    req = requests.get(url)
    # Comprobamos que la petición nos devuelve un Status Code = 200
    statusCode = req.status_code
    if statusCode == 200:
        # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
        html = BeautifulSoup(req.content, "html.parser")
        ###############
        links2 = html.find_all('div', {'class': 'catlistings-container'})
        
        numUrlCategoria = 0

        for num in range(len(links2[0].contents)):    
            if (num%2 != 0):
                urlCategoria = links2[0].contents[num].attrs['href']
                numUrlCategoria = numUrlCategoria + 1
                strTextoNumProductos =  links2[0].contents[num].contents[1].contents[5].contents[0]
                strTextoNumProductos = strTextoNumProductos.replace(".", "")
                numProductosDeCategoria = int(re.findall(r'\d+[.0-9]*', strTextoNumProductos)[0])

                print("\t %i #############################################", numUrlCategoria)
                print("\t NumCategoria: %i, NumFor: %i, numProductosDeCategoria: %i, Pag de Categorias: %s" % (numUrlCategoria, num, numProductosDeCategoria, urlCategoria))

                marca = UrlMarcas[0].split("/",5)[5]

                if (num > 0):  #posiciond e la categoria * 2              

                     time.sleep(0.1)
                     inst = aListadoDeCategoria.Informacion()
                     inst.datos(urlCategoria, num, numProductosDeCategoria, marca)

        print("\t %i ----------------------------------------------", numUrlCategoria)
        print("\t TERMINAMOS LA MARCA ")
        print("\t %i ----------------------------------------------", numUrlCategoria)

