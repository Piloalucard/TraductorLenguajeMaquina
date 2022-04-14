class Valor:
    lexema=""
    token=""
    tipo=-1

    def __init__(self,l,token,t):
        self.lexema=l
        self.token=token
        self.tipo=t
    
    def toString(self):
        aux=self.lexema+"\t"+self.token+"\t\t"+str(self.tipo)
        return aux
    
    def getLexema(self):
        return self.lexema
    
    def getToken(self):
        return self.token
    
    def getNum(self):
        return self.tipo
    
    
    def setLexema(self,c):
        self.lexema=c

    def setToken(self,s):
        self.token=s

    def setNum(self,t):
        self.tipo=t
    