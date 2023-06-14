# Script copied from https://gist.github.com/HiroNakamura/4650385
# https://www.aboutespanol.com/kin-maya-201975


class Sello:
   def __init__(self,numero, color,simbolo, nombre):
      self.numero = numero 
      self.color = color 
      self.simbolo = simbolo
      self.nombre = nombre

   def __str__(self):
      return "Sello(numero: "+str(self.numero)+", nombre: "+self.nombre+", simbolo: "+self.simbolo+", color: "+self.color+")"


mapaAnyos = {"1910":62, "1962":62, "1911":167, "1963":167,"1912":12,"1964":12,"1913":117, "1965":117, "1914":222, "1966":222, "1915":67, "1967":67, "1916":172, "1968":172, "1917":17, "1969":17, "1918":122, "1970":122, "1919":227, "1971":227, "1920":72, "1972":72, "1921":177, "1973":177, "1922":22, "1974":22, "1923":127, "1975":127, "1924":232, "1976":232, "1925":77, "1977":77, "1926":182, "1978":182, "1927":27, "1979":27, "1928":132, "1980":132, "1929":237, "1981":237, "1930":82, "1982":82, "1931":187, "1983":187, "1932":32, "1984":32, "1933":137, "1985":137, "1934":242, "1986":242, "1935":87, "1987":87, "1961":217, "2013":217, "1960":112, "2012":112, "1959":7, "2011":7, "1958":162, "2010":162,"1957":57, "2009":57, "1956":212, "2008":212, "1955":107, "2007":107, "1954":2, "2006":2, "1953":157, "2005":157, "1952":52, "2004":52, "1951":207, "2003":207,"1950":102, "2002":102, "1949":257, "2001":257, "1948":152, "2000":152, "1947":47, "1999":47, "1946":202, "1998":202, "1945":97, "1997":97, "1944":252, "1996":252, "1943":147, "1995":147, "1942":42, "1994":42, "1941":197, "1993":197, "1940":92, "1992":92, "1939":247, "1991":247,"1938":142, "1990":142, "1937":37, "1989":37,"1936":192, "1988":192 }
mapaMeses = {"enero":0, "febrero":31, "marzo":59, "abril":90, "mayo":120,"junio":151,"julio":181,"agosto":212,"septiembre":243,"octubre":13,"noviembre":44,"diciembre":74}
mapaColores = {0:Sello(0,"amarillo","Sol","Ilumina el Fuego Universal"), 1: Sello(1,"rojo","Dragon","Nutre el Nacimiento"),2:Sello(2,"blanco","Viento","Comunica el Espíritu"),3:Sello(3,"Azul","Noche","Sueña la Abundancia"),4:Sello(4,"amarillo","Semilla","Atina el Florecimiento"), 5: Sello(5,"rojo","Serpiente","Sobrevive la Fuerza Vital"),6:Sello(6,"blanco","Enlazador del Mundo","Iguala la Muerte"), 7:Sello(7,"azul","Mano","Conoce la Realización"),8:Sello(8,"amarillo","Estrella","Embellece la Elegancia"),9:Sello(9,"rojo","Luna","Purifica el Agua Universal"),10:Sello(10,"blanco","Perro","Ama el Corazón"), 11:Sello(11,"azul","Mono","Juega la Magia"), 12: Sello(12,"amarillo","Humano","Influencia la Libre Voluntad"),13: Sello(13,"rojo","Caminante del Cielo","Explora el Espacio"), 14:Sello(14,"blanco","Mago","Encanta la Atemporalidad"),15:Sello(15,"azul","Aguila","Crea la Vision"),16:Sello(16,"amarillo","Guerrero","Cuestiona la Inteligencia"),17: Sello(17,"rojo","Tierra","Evoluciona la Navegacion"),18:Sello(18,"blanco","Espejo","Refleja el Sinfin"),19:Sello(19,"azul","Tormenta","Cataliza la Autogeneracion")}
mapaTonos = {1:"Magnético",2:"Lunar",3:"Eléctrico",4:"Autoexistente",5:"Entonado",6:"Rítmico",7:"Resonante",8:"Galáctico",9:"Solar",10:"Planetario",11:"Espectral",12:"Cristal",13:"Cósmico"}


def getNomKin(num_color_sello, num_tono_galactico):
   return str(num_color_sello) +" "+str(num_tono_galactico)

def getTonoGalactico(num_tono_cosmico):
   return mapaTonos[num_tono_cosmico]

def getNomColorSello(num_sello_solar):
   return mapaColores[num_sello_solar]

def getNumTonoCosmico(num_kin):
   operacion = num_kin/13.0
   operacion = round(operacion)
   if operacion == 0.0:
      return 13.0
   return num_kin - (13.0 * operacion)

def getSelloSolar(num_kin):
   operacion = num_kin/20.0
   operacion = round(operacion)
   if operacion == 0.0:
      return 20.0
   return num_kin - (20.0 * operacion)

def getNumKin(anyo, mes, dia):
   suma = anyo+mes+dia
   if suma > 260:
      return suma - 260
   return suma

def getMesValor(mes):
   return mapaMeses[mes]

def getAnyoValor(anyo):
   return mapaAnyos[anyo]


def main():
   print("\t [Tzolkin]")
   anyo = getAnyoValor(input("Año de nacimiento:"))
   mes = getMesValor(input("Mes de nacimiento:"))
   num_kin = getNumKin(anyo,mes,int(input("Dia de nacimiento:")))
   if num_kin !=None:
      print(f"No. kin: {num_kin}")
      num_sello_solar = getSelloSolar(num_kin)
      print(f"No. sello solar: {num_sello_solar}")
      num_tono_cosmico = getNumTonoCosmico(num_kin)
      print(f"No. del tono galáctico: {num_tono_cosmico}")
      nom_color_sello = getNomColorSello(num_sello_solar)
      print(f"Nombre y color sello solar: {nom_color_sello}")
      nom_tono_galactico = getTonoGalactico(num_tono_cosmico)
      print(f"Nombre del tono galactico: {nom_tono_galactico}")
      nom_kin = getNomKin(nom_color_sello, nom_tono_galactico)
      print(f"Nombre Kin: {nom_kin}")


if __name__=='__main__':
   main()