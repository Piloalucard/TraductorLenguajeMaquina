from valor import Valor
from regla import Regla
from nodo import Nodo

class Sintactico:
    lista=[]
    lr=[]
    reglas=[]
    tabla=[[]]
    pila=[]

    def __init__(self,l,archivo):
        self.lista=l
        self.lr=archivo
        self.reglas=[]
        self.tabla=[[]]
        self.pila=[]
        self.pila.append(Valor("D","D",0))
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
        arbol=[]
        while(True):
            if(modo==1): #Si fue un desplazamiento toma la fila del desplazamiento y la columna del siguiente token de la lista
                fila=self.pila[-1].getNum()
                columna=self.lista[0].getNum()
            else: #Si fue una regla, toma el ultimo desplazamiento y la regla
                fila=self.pila[-2].getNum()
                columna=self.pila[-1].getNum()
            
            actual=int(self.tabla[fila][columna])

            if(actual >= 1): #Los numeros positivos en la matriz son desplazamientos
                if(modo == 1): #Si lo ultimo fue un desplazamiento, se mete a la pila el token actual primero de la lista 
                    self.pila.append(self.lista.pop(0))

                self.pila.append(Valor("D","D",actual))
                modo=1
                
            elif(actual <= -1): #Las reglas son negativas
                r=abs(actual) #Se cambia a positiva y se obtiene su posicion en la lista de reglas
                r=r-2
                reglaActual=self.reglas[r]
                lon=reglaActual.getLon()*2
                id=reglaActual.getId()


                #Crea el nodo y anade los terminales
                myNodo=Nodo(-1,[],[])
                for i in range(lon):
                    aux = self.pila.pop()
                    if(aux.getToken() != "R" and aux.getToken() != "D"):
                        myNodo.addTerminal(aux)
                

                num=r+1
                #NoTerminales
                #Reglas sin nada:
                #2,7,10,12,15,19,26,29,31,33 (10)

                #Con uno (24)
                anadidos=False
                reglasUno=[1,4,5,6,8,11,13,14,17,18,21,24,25,27,28,30,35,40,41,42,43,44,45,52]
                #Con Dos (13)
                reglasDos=[3,9,16,20,23,32,34,46,47,48,49,50,51]
                if(num in reglasUno):
                    myNodo.addNoTerminal(arbol.pop(-1))
                elif(num in reglasDos):
                    myNodo.addNoTerminal(arbol.pop(-1))
                    myNodo.addNoTerminal(arbol.pop(-1))
                elif(num==22): #El unico de 3
                    myNodo.addNoTerminal(arbol.pop(-1))
                    myNodo.addNoTerminal(arbol.pop(-1))
                    myNodo.addNoTerminal(arbol.pop(-1))

                myNodo.setRegla(num)
                myNodo.revTerminales()
                arbol.append(myNodo)
                if(r==0):
                    break

                
                self.pila.append(Valor(str(r+1),"R",id))
                modo=2
            else:
                return self.lista[0].getLexema(),None


        return "",arbol[0]
        

        
        
        

        
        




