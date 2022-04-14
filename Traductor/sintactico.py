from valor import Valor
from regla import Regla

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
        self.pila.append(0)
        self.decodeLR()
    
    def decodeLR(self):
        nreglas=int(self.lr[0])+1
        for i in range(1,nreglas):
            aux=self.lr[i].replace('\n', '').split('\t')
            newRegla=Regla(int(aux[0]),int(aux[1]),aux[2])
            self.reglas.append(newRegla)
        
        
        aux1=self.lr[nreglas].replace('\n', '').split('\t')
        filas=int(aux1[0])
        columnas=int(aux1[1])
        self.tabla = [[0 for x in range(columnas)] for y in range(filas)] 
        inicio=nreglas+1

        fila=0
        for i in range(inicio,len(self.lr)):
            aux2=self.lr[i].replace('\n', '').split('\t')
            for columna in range(0,columnas):
                self.tabla[fila][columna] = aux2[columna] 
            fila+=1
    
    def analisis(self):
        aceptado=False

        modo=1
        while(True):
            print(self.pila)
            if(modo==1):
                fila=self.pila[-1]
                columna=self.lista[0].getNum()
            else:
                fila=self.pila[-2]
                columna=self.pila[-1]
            
            actual=int(self.tabla[fila][columna])

            if(actual >= 1):
                if(modo == 1):
                    self.pila.append(self.lista.pop(0).getNum())
                    self.pila.append(actual)
                else:
                    self.pila.append(actual)

                modo=1
                
            elif(actual <= -1):
                r=abs(actual)
                r=r-2
                if(r==0):
                    aceptado=True
                    break
                reglaActual=self.reglas[r]
                lon=reglaActual.getLon()*2
                id=reglaActual.getId()
                for i in range(lon):
                    self.pila.pop()
                self.pila.append(id)

                modo=2


            else:
                print("Se encontro un NULL en " + self.lista[0].getLexema())

                break
    
        
        return aceptado
        

        
        
        

        
        




