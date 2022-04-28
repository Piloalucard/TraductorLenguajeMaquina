from asyncio.windows_events import NULL
from valor import Valor
from regla import Regla
from nodo import Nodo

class Sintactico:
    lista=[]
    lr=[]
    reglas=[]
    tabla=[[]]
    pila=[]
    declaraciones=[]

    def __init__(self,l,archivo):
        self.lista=l
        self.lr=archivo
        self.reglas=[]
        self.tabla=[[]]
        self.pila=[]
        self.declaraciones=[]
        self.pila.append(0)
        self.decodeLR()
    
    def decodeLR(self):
        nreglas=int(self.lr[0])+1 #Obtiene el primer renglon con el numero de reglas
        for i in range(1,nreglas): #Itera desde el segundo renglon hastatodas las reglas
            aux=self.lr[i].replace('\n', '').split('\t')
            newRegla=Regla(int(aux[0]),int(aux[1]),aux[2])
            self.reglas.append(newRegla)
        
        
        aux1=self.lr[nreglas].replace('\n', '').split('\t')
        filas=int(aux1[0])
        columnas=int(aux1[1]) #Obtiene las filas y columnas del siguiente renglon
        self.tabla = [[0 for x in range(columnas)] for y in range(filas)] #Con las filas y columnas rellena la matriz de 0
        inicio=nreglas+1

        fila=0
        for i in range(inicio,len(self.lr)): #Procede a rellenar la matriz desde los renglones restantes del archivo lr
            aux2=self.lr[i].replace('\n', '').split('\t')
            for columna in range(0,columnas):
                self.tabla[fila][columna] = aux2[columna] 
            fila+=1
    
    def analisis(self):
        modo=1 #Para saber si lo anterior fue una regla o un desplazamiento
        decaux=[]
        while(True):
            if(modo==1): #Si fue un desplazamiento toma la fila del desplazamiento y la columna del siguiente token de la lista
                fila=self.pila[-1]
                columna=self.lista[0].getNum()
            else: #Si fue una regla, toma el ultimo desplazamiento y la regla
                fila=self.pila[-2]
                columna=self.pila[-1]
            
            actual=int(self.tabla[fila][columna])

            if(actual >= 1): #Los numeros positivos en la matriz son desplazamientos
                if(modo == 1): #Si lo ultimo fue un desplazamiento, se mete a la pila el token actual primero de la lista 
                    #y el desplazamiento
                    decaux.append(self.lista[0])
                    self.pila.append(self.lista.pop(0).getNum())
                    self.pila.append(actual)
                    decaux.append(Valor("DESN","(D)",actual))
                else: #Si lo ultimo fue una regla, solo el desplazamiento
                    self.pila.append(actual)
                    decaux.append(Valor("DESN","(D)",actual))
                #Para simplicidad, la iteracion de la pila solo se hace con enteros
                #Sin embargo se necesita del valor completo de los token para lo semantico
                #Se crea una lista copia con los valores,y si encuentra una regla o desplazamiento, lo mete como clase Valor
                modo=1
                
            elif(actual <= -1): #Las reglas son negativas
                r=abs(actual) #Se cambia a positiva y se obtiene su posicion en la lista de reglas
                r=r-2
                reglaActual=self.reglas[r]
                lon=reglaActual.getLon()*2
                id=reglaActual.getId()

                
                #Crear arbol
                
                final=[]
                #Si encuentra una regla para el analisis semantico donde se declaren cosas
                #Se metera en una lista todos los tokens de esa regla y su regla 
                #Toda esa lista, se mete en otra lista, que seran las declaraciones
                for i in range(lon):
                    verificador=str(decaux[-1].getToken())
                    if(verificador != "(R)" and verificador != "(D)"):
                        final.append(Valor(decaux[-1].getLexema(),decaux[-1].getToken(),decaux[-1].getNum()))
                    decaux.pop()

                auxV=Valor("(REGLA "+str(r+1)+")","(R)",r+1)
                final.append(auxV)
                self.declaraciones.append(final)
                if(r==0):
                    break
                for i in range(lon):
                    self.pila.pop()
                self.pila.append(id)
                decaux.append(Valor("REGLAN","(R)",id))
                modo=2
            else:
                return self.lista[0].getLexema(),NULL

        antepenultimo=Nodo(-1,[],[])
        penultimo=Nodo(-1,[],[])
        ultimo=Nodo(-1,[],[])
        for i in self.declaraciones:
            for j in i:
                verificador=str(j.getToken())
                if(verificador == "(R)"):
                    num=int(j.getNum())
                    
                    #No contienen nada y no entran a ningun if
                    #Reglas:
                    #2,7,10,12,15,19,26,29,31,33 (10)
                    actual=Nodo(num,[],[])

                    #NoTerminales
                    #Con uno (24)
                    anadidos=False
                    reglasUno=[1,4,5,6,8,11,13,14,17,18,21,24,25,27,28,30,35,40,41,42,43,44,45,52]
                    for n in reglasUno:
                        if(num==n):
                            actual.addNoTerminal(Nodo(ultimo.getRegla(),ultimo.getNoTerminales(),ultimo.getTerminales()))
                            anadidos=True
                            break

                    #Con Dos (13)
                    reglasDos=[3,9,16,20,23,32,34,46,47,48,49,50,51]
                    if(not anadidos):
                        for n in reglasDos:
                            if(num==n):
                                actual.addNoTerminal(Nodo(ultimo.getRegla(),ultimo.getNoTerminales(),ultimo.getTerminales()))
                                actual.addNoTerminal(Nodo(penultimo.getRegla(),penultimo.getNoTerminales(),penultimo.getTerminales()))
                                anadidos=True
                                break
                    
                    #Con Tres
                    if(num==22):
                        actual.addNoTerminal(Nodo(ultimo.getRegla(),ultimo.getNoTerminales(),ultimo.getTerminales()))
                        actual.addNoTerminal(Nodo(penultimo.getRegla(),penultimo.getNoTerminales(),penultimo.getTerminales()))
                        actual.addNoTerminal(Nodo(antepenultimo.getRegla(),antepenultimo.getNoTerminales(),antepenultimo.getTerminales()))
                             

                    #Terminales                
                    for ter in i:
                        if(ter != i[-1]):
                            actual.addTerminal(ter.getLexema())
                    actual.revTerminales()

                    antepenultimo=penultimo
                    penultimo=ultimo
                    ultimo=actual


        
        return "",ultimo
        

        
        
        

        
        




