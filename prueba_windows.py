import array as arrayNum

q = 3.5
w = round(q)

q = 3.51
w = round(q)

q = 3.522
w = round(q)

q = 3.8
w = round(q)
q = 3.1
w = round(q)

#crear un excel con info
imageFileName = "q/wwqe*rdfdf/"
imageFileName = imageFileName.replace("/", "")

print("imageFileName : %s",imageFileName)


#crear una lista 
inic = 1
lista = []
for inic in range(10):  
    strtexto = "raul" + str(inic)
    lista.append(strtexto) 
var = "raul5"    
if var in lista:
    print("entro en el if")

print("lista %a " % (lista))

