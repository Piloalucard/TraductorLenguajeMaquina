from valor import Valor
from nodo import Nodo

class Semantico:
    raiz=Nodo(-1,[],[])

    def __init__(self,raiz):
        self.raiz = raiz

    def preAnalisis(self,t,c,e,lft,lfn):
        tabsim=t
        context=c
        errorToComp=e
        ter=self.raiz.getTerminales()
        noter=self.raiz.getNoTerminales()
        regla=self.raiz.getRegla()
        aux=""
        lastFuncType=lft
        lastFuncName=lfn

        
        try:
            if(regla == 6 or regla == 9 or regla == 11): #Llenadores de tabsim
                if(ter[-1].getLexema() == ")"):
                    try:
                        context.pop(-1)
                        context.append(ter[1].getLexema())
                    except:
                        context.append(ter[1].getLexema())
                p1=ter[0].getLexema()
                p2=ter[1].getLexema()
                try:
                    p3=context[-1]
                except:
                    context.append(" ")
                    p3=context[-1]
                if(p2==p3):
                    aux=p1+"\t"+p2+"\t "
                else:
                    aux=p1+"\t"+p2+"\t"+p3
                if(regla==9):
                    lastFuncType=p1
                    lastFuncName=p2
                for var in tabsim:
                    removedTabs = var.split("\t")
                    if(p2 == removedTabs[1]):
                        if(p3 == removedTabs[2]):
                            exception = p1 + " "+ p2 + " En " + p3 + " Ya esta declarado " + " Regla #" + str(regla)
                            return ["Error semantico en: ",exception],[],[]
                tabsim.append(aux)
            elif(regla == 8):
                splittb = tabsim[-1].split("\t")
                p1=splittb[0]
                p2=ter[1].getLexema()
                p3=context[-1]
                aux=p1+"\t"+p2+"\t"+p3
                for var in tabsim:
                    removedTabs = var.split("\t")
                    if(p2 == removedTabs[1]):
                        if(p3 == removedTabs[2]):
                            exception = p1 + " "+ p2 + " En " + p3 + " Ya esta declarado " + " Regla #" + str(regla)
                            return ["Error semantico en: ",exception],[],[]
                tabsim.append(aux)
            elif(regla == 13):
                p1=ter[1].getLexema()
                p2=ter[2].getLexema()
                p3=context[-1]
                aux=p1+"\t"+p2+"\t"+p3
                for var in tabsim:
                    removedTabs = var.split("\t")
                    if(p2 == removedTabs[1]):
                        if(p3 == removedTabs[2]):
                            exception = p1 + " "+ p2 + " En " + p3 + " Ya esta declarado " + " Regla #" + str(regla)
                            return ["Error semantico en: ",exception],[],[]
                tabsim.append(aux)

            #Aqui empieza redesign
            elif(regla == 21):
                error1=1
                error2=1
                termino1=ter[0].getLexema()
                
                nodoaux=noter[0]
                r1=nodoaux.getRegla()

                while(r1 != 52):
                    nodoaux=nodoaux.getNoTerminales()[0]
                    r1=nodoaux.getRegla()
                try:    
                    termino2=nodoaux.getNoTerminales()[0].getTerminales()[0]
                except: #No se puede obtener el valor en la regla 40
                    termino2=termino1

                for var in tabsim:
                    removedTabs = var.split("\t")
                    if(termino1 == removedTabs[1]):
                        error1=0
                    if(termino2.getLexema() == removedTabs[1]):
                        error2=0
                if(error1 == 1):
                    exception = termino1 + ter[1].getLexema() + " Variable no declarada Regla #" + str(regla)
                    return ["Error semantico en: ",exception],[],[]
                if(error2 == 1)
                    exception = termino2.getLexema() + ter[2].getLexema() + " Variable no declarada Regla #" + str(regla)
                    return ["Error semantico en: ",exception],[],[]

            elif(regla == 24 or regla == 44 or regla == 45):
                band=False
                nodoaux=noter[0]
                r1=nodoaux.getRegla()
                while(r1 != 52):
                    nodoaux=nodoaux.getNoTerminales()[0]
                    r1=nodoaux.getRegla()
                
                try:
                    termino1=nodoaux.getNoTerminales()[0].getTerminales()[0]
                except: #No se puede obtener el valor en la regla 40
                    termino1=Valor(lastFuncType,lastFuncName,regla)

                errorToComp.append(Valor("","",regla))
                errorToComp.append(termino1)
                errorToComp.append(Valor(lastFuncType,lastFuncName,regla))
                for var in tabsim:
                    removedTabs = var.split("\t")
                    if(termino1 == removedTabs[1]):
                        band=True
                        break

                if(band):
                    exception = termino1.getLexema() + ter[1].getLexema() + " Regla #" + str(regla)
                    return ["Error semantico en: ",exception],[],[]

            elif(regla >= 46 and regla <=51):
                band=False
                nodoaux=noter[0]
                r1=nodoaux.getRegla()
                while(r1 != 52):
                    nodoaux=nodoaux.getNoTerminales()[0]
                    r1=nodoaux.getRegla()
                try:
                    termino1=nodoaux.getNoTerminales()[0].getTerminales()[0]
                except: #No se puede obtener el valor en la regla 40
                    termino1=Valor("int","Identificador",0)

                nodoaux=noter[1]
                r2=nodoaux.getRegla()
                while(r2 != 52):
                    nodoaux=nodoaux.getNoTerminales()[0]
                    r2=nodoaux.getRegla()
                try:
                    termino2=nodoaux.getNoTerminales()[0].getTerminales()[0]
                except:#REGLA40
                    termino2=termino1
                
                errorToComp.append(Valor("","",regla))
                errorToComp.append(termino1)
                errorToComp.append(termino2)
                
                for var in tabsim:
                    removedTabs = var.split("\t")
                    if(termino1.getLexema() == removedTabs[1]):
                        band=True
                        break
                    if(termino2.getLexema() == removedTabs[1]):
                        band=True
                        break
                if(band):
                    exception = termino1.getLexema() + ter[1].getLexema() + termino2.getLexema() + ter[2].getLexema() + " Regla #" + str(regla)
                    return ["Error semantico en: ",exception],[],[]

            for i in noter:
                provis = Semantico(i)
                tabsim,context,errorToComp = provis.preAnalisis(tabsim,context,errorToComp,lastFuncType,lastFuncName)
        except:
            pass

        return tabsim,context,errorToComp

    def analisis(self):
        tabsim,context,errorToComp = self.preAnalisis([],[" "],[]," "," ")
        while(len(errorToComp) > 0):
            regla = errorToComp.pop(0).getNum()
            termino1 = errorToComp.pop(0)
            termino2 = errorToComp.pop(0)
            exception = ""
            error=1
            aux1="aux1"
            aux2="aux2"
            if(regla >= 46 and regla <=51):
                try:
                    int(termino1.getLexema())
                    aux1="int"
                    error=0
                except:
                    try:
                        float(termino1.getLexema())
                        aux1="float"
                        error=0
                    except:
                        if(regla != 46 and regla != 47):#Las demas reglas
                            try:
                                bool(termino1.getLexema())
                                aux1="bool"
                                error=0
                            except:
                                if(termino1.getLexema()[0] == '"'):
                                    aux1="string"
                                    error=0
                                else:
                                    for var in tabsim:
                                        removedTabs = var.split("\t")
                                        if(termino1.getLexema() == removedTabs[1]):#Verifica que en la R45 se haya declarado variable
                                            error=0
                                            aux1=removedTabs[0] #Obtiene el tipo
                        else: #Regla 46 y 47
                            for var in tabsim:
                                removedTabs = var.split("\t")
                                if(termino1.getLexema() == removedTabs[1]):#Verifica que en la R45 se haya declarado variable
                                    error=0
                                    aux1=removedTabs[0] #Obtiene el tipo
                            if(error == 0 and aux1 != "int" and aux1 != "float"):
                                error = 4
                
                try:
                    int(termino2.getLexema())
                    aux2="int"
                    error=0
                except:
                    try:
                        float(termino2.getLexema())
                        aux2="float"
                        error=0
                    except:
                        if(regla != 46 and regla != 47):#Las demas reglas
                            try:
                                bool(termino2.getLexema())
                                aux2="bool"
                                error=0
                            except:
                                if(termino2.getLexema()[0] == '"'):
                                    aux2="string"
                                    error=0
                                else:
                                    for var in tabsim:
                                        removedTabs = var.split("\t")
                                        if(termino2.getLexema() == removedTabs[1]):#Verifica que en la R45 se haya declarado variable
                                            error=0
                                            aux2=removedTabs[0] #Obtiene el tipo
                        else: #Regla 46 y 47
                            for var in tabsim:
                                removedTabs = var.split("\t")
                                if(termino2.getLexema() == removedTabs[1]):#Verifica que en la R45 se haya declarado variable
                                    error=0
                                    aux2=removedTabs[0] #Obtiene el tipo
                            if(error == 0 and aux1 != "int" and aux1 != "float"):
                                error = 4

                if(aux1 != aux2):
                    error=2          
                            
                if(error > 0):
                    if(error == 1):
                        exception="<"+termino1.getLexema()+"> Variable no definida"
                    elif(error == 2):
                        exception="<"+termino1.getLexema()+"> <"+termino2.getLexema()+"> Variables son de diferente tipo de dato o no estan definidas"
                    elif(error == 4):
                        exception="<"+termino1.getLexema()+"> Variable no es tipo int o float"
                    return ["Error semantico en: ",exception+" Regla #"+str(regla)],[],[]

            elif(regla == 45):
                try:
                    bool(termino1.getLexema())
                    error=0
                except:
                    for var in tabsim:
                        removedTabs = var.split("\t")
                        if(termino1.getLexema() == removedTabs[1]):#Verifica que en la R45 se haya declarado variable
                            error=0
                            aux1=removedTabs[0] #Obtiene el tipo
                    if(error == 0 and aux1 != "bool"):
                        error = 4
                if(error > 0):
                    if(error == 1):
                        exception="<"+termino1.getLexema()+"> Variable no definida"
                    elif(error == 4):
                        exception="<"+termino1.getLexema()+"> Variable no es tipo bool"
                    return ["Error semantico en: ",exception+" Regla #"+str(regla)],[],[]

            if(regla == 44):
                try:
                    int(termino1.getLexema())
                    error=0
                except:
                    try:
                        float(termino1.getLexema())
                        error=0
                    except:
                        for var in tabsim:
                            removedTabs = var.split("\t")
                            if(termino1.getLexema() == removedTabs[1]):#Verifica que en la R45 se haya declarado variable
                                error=0
                                aux1=removedTabs[0] #Obtiene el tipo

                        if(error == 0 and aux1 != "int" and aux1 != "float"):
                            error = 4

                if(error > 0):
                    if(error == 1):
                        exception="<"+termino1.getLexema()+"> Variable no definida"
                    elif(error == 4):
                        exception="<"+termino1.getLexema()+"> Variable no es tipo int o float"
                    return ["Error semantico en: ",exception+" Regla #"+str(regla)],[],[]

            elif(regla == 24):
                try:
                    bool(termino1.getLexema())
                    if("bool" != termino2.getLexema()): #Lo compara con el tipo de la funcion
                            error = 2
                except:
                    try:
                        int(termino1.getLexema())
                        if("int" != termino2.getLexema()): #Lo compara con el tipo de la funcion
                            error = 2
                    except:
                        try: 
                            float(termino1.getLexema())
                            if("float" != termino2.getLexema()): #Lo compara con el tipo de la funcion
                                error = 2
                        except:
                            if(termino1.getLexema()[0] == '"'):
                                if("string" != termino2.getLexema()): #Lo compara con el tipo de la funcion
                                    error = 2
                            else:
                                for var in tabsim:
                                    removedTabs = var.split("\t")
                                    if(termino1.getLexema() == removedTabs[1]):#Verifica que en la R24 se haya declarado variable
                                        error=0
                                        aux1=removedTabs[0] #Obtiene el tipo
                                        aux2=removedTabs[2] #Obtiene el contexto

                                if(aux1 != termino2.getLexema()): #Lo compara con el tipo de la funcion
                                    error = 2
                                if(aux2 != termino2.getToken()): #Lo compara con el contexto de la funcion
                                    error = 3
                    
                if(error > 0):
                    if(error == 1):
                        exception="<"+termino1.getLexema()+"> Variable no definida"
                    elif(error == 2):
                        exception="<"+termino1.getLexema()+"> <"+termino2.getLexema()+"> Variable del return y Funcion no son del mismo tipo de dato o no estan definidas"
                    elif(error == 3):
                        exception="<"+termino1.getLexema()+"> <"+termino2.getLexema()+"> Variable del return definida en diferente contextos"
                    return ["Error semantico en: ",exception+" Regla #"+str(regla)],[],[]

            elif(regla == 21):
                for var in tabsim:#Verifica que en la R21 se haya declarado la primera variable
                    removedTabs = var.split("\t")
                    if(termino1.getLexema() == removedTabs[1]):
                        aux1=removedTabs[0]
                    if(termino2.getLexema() == removedTabs[1]):
                        aux2=removedTabs[0]
                
                if(aux1 == aux2): #Verifica que las dos partes de la R21 sean del mismo tipo
                    error=0
                else:
                    if(aux1 == termino2.getToken()):
                        error = 0
                    else:
                        error=2

                if(error == 0): #Verifica que la segunda variable este declarada o un int/float/string
                    aux1="aux1"
                    aux2="aux2"
                    try:
                        bool(termino1.getLexema())
                    except:
                        try:
                            int(termino2.getLexema())
                        except:
                            try: 
                                float(termino2.getLexema())
                            except:
                                if(termino2.getLexema()[0] != '"'):
                                    error = 0
                                    for var in tabsim:
                                        removedTabs = var.split("\t")
                                        if(termino1.getLexema() == removedTabs[1]):
                                            aux1=removedTabs[2]
                                        if(termino2.getLexema() == removedTabs[1]):
                                            aux2=removedTabs[2]

                                    if(aux1 != aux2):
                                        error = 3

                if(error > 0):
                    if(error == 1):
                        exception="<"+termino1.getLexema()+"> Variable no definida"
                    elif(error == 2):
                        exception="<"+termino1.getLexema()+"> <"+termino2.getLexema()+"> Variable y termino de asignacion son de diferente tipo de dato o no estan definidas"
                    elif(error == 3):
                        exception="<"+termino1.getLexema()+"> <"+termino2.getLexema()+"> Variables definidas en diferentes contextos"
                
                    return ["Error semantico en: ",exception+" Regla #"+str(regla)],[],[]



        return tabsim,context,errorToComp





