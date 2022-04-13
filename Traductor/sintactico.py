from valor import Valor

class Sintactico:
    lista=[]
    lineas=[]
    err=[]

    def __init__(self,l):
        self.lista=l

    def impLineas(self):
        for i in self.err:
            print(i)
        for i in self.lineas:
            print(i)
        
    
    def analisis(self):
        linea=[]
        nlineas=1
        error=False
        i=0
        for l in self.lista:
            tipo=l.getTipo()
            if tipo == 23:
                break
        
            elif tipo == 0 or tipo == 1 or tipo == 2 or tipo == 3:
                taux=self.lista[i+1].getTipo()
                if taux == 0 or taux == 1 or taux == 2 or taux == 3:
                    error=True
            
            elif tipo == 4:
                if linea:
                    error=True
                taux=self.lista[i+1].getTipo()
                if taux >= 4:
                    error=True
            
            elif tipo == 5 or tipo == 6:
                taux=self.lista[i-1].getTipo()
                if taux >= 3:
                    error=True
                taux=self.lista[i+1].getTipo()
                if taux >= 3:
                    error=True
            
            elif tipo == 7 or tipo == 8 or tipo == 9 or tipo == 11:
                taux=self.lista[i-1].getTipo()
                if taux >= 4:
                    error=True
                taux=self.lista[i+1].getTipo()
                if taux >= 4:
                    error=True
            
            elif tipo == 11:
                taux=self.lista[i+1].getTipo()
                if taux >= 4:
                    error=True
                taux=self.lista[i-1].getTipo()
                if taux <=18:
                    error=True

                



            elif  tipo== 12:
                taux=self.lista[i-1].getTipo()
                if taux >= 4:
                    error=True
                
                
                if not linea:
                    error=True
                
                if error:
                    self.err.append(nlineas)

                
                self.lineas.append(linea)
                linea=[]
                error=False
                nlineas+=1

            linea.append(l.getCadena())
            i+=1

                    
                








