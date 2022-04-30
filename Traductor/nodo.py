class Nodo:
    noTerminales=[]
    regla=-1
    terminales=[]

    def __init__(self,regla,noTer,Ter):
        self.regla=regla
        self.noTerminales=noTer
        self.terminales=Ter

    def terIsEmpty(self):
        for i in self.terminales:
            return False
        return True
    
    def noTerIsEmpty(self):
        for i in self.noTerminales:
            return False
        return True

    def revTerminales(self):
        self.terminales.reverse()
    
    def recorrer(self):
        print("")
        print("")
        print("Inicio R"+str(self.regla))
        print("↓")
        print("Terminales:")
        for i in self.terminales:
            print(str(i)+"\t",end="")    
        print("")
        print("No Terminales:")
        for i in self.noTerminales:
            print("R"+str(i.getRegla())+"\t",end="")

        for i in self.noTerminales:
            i.recorrer()

    
    def addNoTerminal(self,x):
        self.noTerminales.append(x)
    
    def getNoTerminales(self):
        return self.noTerminales
    
    def addTerminal(self,t):
        self.terminales.append(t)
    
    def getTerminales(self):
        return self.terminales
    
    def getRegla(self):
        return self.regla
    
    def setRegla(self,r):
        self.regla=r
    
