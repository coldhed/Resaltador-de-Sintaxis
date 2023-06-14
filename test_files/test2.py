# Script copied from https://gist.github.com/HiroNakamura/4650385
#!/bin/python
# coding=utf-8


from bs4 import BeautifulSoup
import requests
import pandas as pd

URL = "https://resultados.as.com/resultados/futbol/primera/clasificacion/"
pagina = requests.get(URL)

if pagina != None and pagina.ok:
    print(f"Pagina: {pagina}")
    soup = BeautifulSoup(pagina.content,"html.parser")
    eq = soup.find_all('span',class_="nombre-equipo")
    print(f"Equipo: {eq}")
    equipos = []
    cont = 0
    for i in eq:
        if cont < 20:
            equipos.append(i.text)
        else:
            break
        cont+=1
    print(f"Equipos: {equipos}")
    cont = 0
    pt = soup.find_all('td',class_="destacado")
    puntos = list()
    for i in pt:
        if cont < 20:
            puntos.append(i.text)
        else:
            break
        cont+=1
    print(f"Puntos: {puntos}")
    df = pd.DataFrame({'Nombre':equipos,"Puntos":puntos},index=list(range(1,21)))
    df.to_csv('clasificacion.csv',index=False)
    print("Hecho")