import imp
from valor import Valor

class Lexico:
    _fuente = ""
    _ind = 0
    _estado = 0
    _lista=[]

    def __init__(self):
        self._ind=0

    def getLista(self):
        return self._lista


    def addFuente(self,f):
        self._ind=0
        self._fuente=self._fuente+f

    def obtLexico(self):
        auxcad="Lexema\tToken\t\tTipo\n"
        auxcad+="-----------------------------------\n"
        for i in self._lista:
            auxcad+=i.toString()+"\n"
        return auxcad

    def analisis(self):
        self._fuente=self._fuente+"$"
        while(self._estado == 0 and self._ind < len(self._fuente)):
            lexema=""
            token="Error"
            aux=""
            num=-1
            while(self._ind < len(self._fuente) and self._estado != 20):
                if(self._estado == 0):
                    if(self._fuente[self._ind] == ";"):
                        self._estado = 20
                        lexema=self._fuente[self._ind]
                        token="PuntoComa"
                        num=12
                        self._ind = self._ind + 1
                    elif(self._fuente[self._ind] == ","):
                        self._estado = 20
                        lexema=self._fuente[self._ind]
                        token="Coma"
                        num=13
                        self._ind = self._ind + 1
                    elif(self._fuente[self._ind] == "("):
                        self._estado = 20
                        lexema=self._fuente[self._ind]
                        token="ParentesisIzq"
                        num=14
                        self._ind = self._ind + 1
                    elif(self._fuente[self._ind] == ")"):
                        self._estado = 20
                        lexema=self._fuente[self._ind]
                        token="ParentesisDer"
                        num=15
                        self._ind = self._ind + 1
                    elif(self._fuente[self._ind] == "{"):
                        self._estado = 20
                        lexema=self._fuente[self._ind]
                        token="CorcheteIzq"
                        num=16
                        self._ind = self._ind + 1
                    elif(self._fuente[self._ind] == "}"):
                        self._estado = 20
                        lexema=self._fuente[self._ind]
                        token="CorcheteDer"
                        num=17
                        self._ind = self._ind + 1
                    elif(self._fuente[self._ind] == "="):
                        self._estado = 18
                        aux=self._fuente[self._ind]
                        self._ind = self._ind + 1
                    elif(self._fuente[self._ind] == "!"):
                        self._estado = 10
                        aux=self._fuente[self._ind]
                        self._ind = self._ind + 1
                    elif(self._fuente[self._ind] == "$"):
                        self._estado = 20
                        lexema=self._fuente[self._ind]
                        token="Delimitador"
                        self._ind = self._ind + 1
                        num=23
                    elif(self.__verLetra(self._fuente[self._ind]) or self.__verNum(self._fuente[self._ind])):
                        self._estado=4
                        token="ID"
                    elif(self._fuente[self._ind] == "+" or self._fuente[self._ind] == "-"):
                        self._estado = 20
                        lexema=self._fuente[self._ind]
                        token="OpSuma"
                        self._ind = self._ind + 1
                        num=5
                    elif(self._fuente[self._ind] == "*" or self._fuente[self._ind] == "/"):
                        self._estado = 20
                        lexema=self._fuente[self._ind]
                        token="OpMul"
                        self._ind = self._ind + 1
                        num=6
                    elif(self._fuente[self._ind] == "<" or self._fuente[self._ind] == ">"):
                        self._estado = 7
                        aux=self._fuente[self._ind]
                        token="OpRelacional"
                        self._ind = self._ind + 1
                        num=7
                    elif(self._fuente[self._ind] == "|"):
                        self._estado = 8
                        aux=self._fuente[self._ind]
                        token="OpOr"
                        self._ind = self._ind + 1
                    elif(self._fuente[self._ind] == "&"):
                        self._estado = 9
                        aux=self._fuente[self._ind]
                        token="OpAnd"
                        self._ind = self._ind + 1
                    else:
                        self._ind = self._ind + 1
                elif(self._estado == 18 or self._estado == 10):
                    if(self._fuente[self._ind] == "="):
                        self._estado = 20
                        lexema=aux+self._fuente[self._ind]
                        token="OpIgualdad"
                        self._ind = self._ind + 1
                        num=11
                    elif(self._estado==18):
                        lexema=aux
                        token="Igual"
                        self._estado=20
                        num=18
                    else:
                        lexema=aux
                        token="OpNot"
                        self._estado=20
                        num=10
                elif(self._estado == 4):
                    if(self.__verLetra(self._fuente[self._ind]) or self.__verNum(self._fuente[self._ind]) or self._fuente[self._ind] == "."):
                        aux=aux+self._fuente[self._ind]
                        self._ind = self._ind + 1
                    else:
                        lexema=aux
                        self._estado=20
                elif(self._estado == 7):
                    if(self._fuente[self._ind] == "="):
                        lexema=aux+self._fuente[self._ind]
                        self._ind = self._ind + 1
                    else:
                        lexema=aux
                    self._estado=20

                elif(self._estado == 8):
                    if(self._fuente[self._ind] == "|"):
                        lexema=aux+self._fuente[self._ind]
                        self._ind = self._ind + 1
                        num=8
                    else:
                        lexema=aux
                        token="Error"
                    self._estado=20
                
                elif(self._estado == 8):
                    if(self._fuente[self._ind] == "|"):
                        lexema=aux+self._fuente[self._ind]
                        self._ind = self._ind + 1
                        num=8
                    else:
                        lexema=aux
                        token="Error"
                    self._estado=20
                
                elif(self._estado == 9):
                    if(self._fuente[self._ind] == "&"):
                        lexema=aux+self._fuente[self._ind]
                        self._ind = self._ind + 1
                        num=9
                    else:
                        lexema=aux
                        token="Error"
                    self._estado=20
                
            self._estado=0
            self._lista.append(Valor(lexema,token,num))
        lex=""
        for v in self._lista:
            if(v.getToken() == "ID"):
                lex=v.getLexema()
                if(lex == "int" or lex == "float" or lex=="void" or lex == "string" or lex == "bool"):
                    v.setToken("Tipo de dato")
                    v.setNum(4)
                elif(lex == "if"):
                    v.setToken("if")
                    v.setNum(19)
				
                elif(lex == "while"):
                    v.setToken("while")
                    v.setNum(20)
                
                elif(lex == "return"):
                    v.setToken("return")
                    v.setNum(21)
				
                elif(lex == "else"):
                    v.setToken("else")
                    v.setNum(22)
                    
                else:
                    try:
                        int(lex)
                        v.setToken("int")
                        v.setNum(1)
                    except:
                        try:
                            float(lex)
                            v.setToken("float")
                            v.setNum(2)
                        except:	
                            if(self.__verNum(lex[0])):
                                v.setToken("string")
                                v.setNum(3)
                                continue
                            
                            v.setToken("Identificador")
                            v.setNum(0)

    
    def __verLetra(self,i):
        if (ord(i) >= 65 and ord(i) <= 122) or ord(i) == 45 or ord(i) == 34 or ord(i) == 39:
            return True
        else:
            return False
    
    def __verNum(self,i):
        if ord(i) >= 48 and ord(i) <= 57:
            return True
        else:
            return False
    




