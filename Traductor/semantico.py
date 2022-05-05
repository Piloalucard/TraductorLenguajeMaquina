from valor import Valor
from nodo import Nodo

class Semantico:
    raiz=Nodo(-1,[],[])

    def __init__(self,raiz):
        self.raiz = raiz

    def preAnalisis(self,t,c,lft,lfn,lcft):
        tabsim=t
        context=c
        ter=self.raiz.getTerminales()
        noter=self.raiz.getNoTerminales()
        regla=self.raiz.getRegla()
        aux=""
        exception = ""
        lastFuncType=lft
        lastFuncName=lfn
        lastCallFType=lcft

        
        try:
            if(regla == 6 or regla == 9 or regla == 11): #Llenadores de tabsim
                if(ter[-1].getLexema() == ")"):
                    context.pop(-1)
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
                            return ["Error semantico en: ",exception],[]
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
                            return ["Error semantico en: ",exception],[]
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
                            return ["Error semantico en: ",exception],[]
                tabsim.append(aux)

            #Aqui empieza redesign
            elif(regla == 21):
                error1=1
                error2=1
                termino1=ter[0]
                type1="t1"
                type2="t2"
                context1="1c"
                context2="2c"
                
                nodoaux=noter[0]
                r1=nodoaux.getRegla()

                while(r1 != 52):
                    nodoaux=nodoaux.getNoTerminales()[0]
                    r1=nodoaux.getRegla()
                try:    
                    termino2=nodoaux.getNoTerminales()[0].getTerminales()[0]
                except: 
                    termino2=self.obtFType(lastCallFType)


                if(termino2.getLexema() == "true" or termino2.getLexema() == "false"):
                    type1="bool"
                    error2=0
                else:
                    try:
                        int(termino2.getLexema())
                        type2="int"
                        error2=0
                    except:
                        try: 
                            float(termino2.getLexema())
                            type2="float"
                            error2=0
                        except:
                            if(termino2.getLexema()[0] == '"'):
                                type2="string"
                                error2=0
               
                for var in tabsim:
                    removedTabs = var.split("\t")
                    if(termino1.getLexema() == removedTabs[1] and type1 =="t1"):
                        type1=removedTabs[0]
                        context1=removedTabs[2]
                        error1=0
                    elif(termino2.getLexema() == removedTabs[1] and type2 =="t2"):
                        type2=removedTabs[0]
                        context2=removedTabs[2]
                        error2=0

                if(type1 != type2):
                    error1=2
                
                
                if(context1 != "1c"):
                    if(context2 != "2c"):
                        if(context1 != context2):
                            error1 = 3
                if(error2 == 1):
                    exception = "<"+termino2.getLexema() + "> Variable no declarada Regla #" + str(regla)
                    return ["Error semantico en: ",exception],[]

                if(error1 > 0):
                    if(error1 == 1):
                        exception = "<"+termino1.getLexema() + "> Variable no declarada Regla #" + str(regla)
                    if(error1 == 2):
                        exception="<"+termino1.getLexema()+"> <"+termino2.getLexema()+"> Variable y termino de asignacion son de diferente tipo de dato Regla #" + str(regla)
                    if(error1 == 3):
                        exception="<"+termino1.getLexema()+"> <"+termino2.getLexema()+"> Variables definidas en diferentes contextos Regla #" + str(regla)
                    return ["Error semantico en: ",exception],[]
                
            elif(regla == 24):
                error1=1
                nodoaux=noter[0]
                r1=nodoaux.getRegla()
                while(r1 != 52):
                    nodoaux=nodoaux.getNoTerminales()[0]
                    r1=nodoaux.getRegla()
                
                termino2=Valor(lastFuncType,lastFuncName,regla)
                try:
                    termino1=nodoaux.getNoTerminales()[0].getTerminales()[0]
                except: 
                    termino1=self.obtFType(lastCallFType)

                
                
                if(termino1.getLexema() == "true" or termino1.getLexema() == "false"):
                    if("bool" != lastFuncType): #Lo compara con el tipo de la funcion
                        error1 = 2
                    else:
                        error1 = 0
                else:
                    try:
                        int(termino1.getLexema())
                        if("int" != lastFuncType): #Lo compara con el tipo de la funcion
                            error1 = 2
                        else:
                            error1 = 0
                    except:
                        try: 
                            float(termino1.getLexema())
                            if("float" != lastFuncType): #Lo compara con el tipo de la funcion
                                error1 = 2
                        except:
                            if(termino1.getLexema()[0] == '"'):
                                if("string" != lastFuncType): #Lo compara con el tipo de la funcion
                                    error1 = 2
                                else:
                                    error1 = 0
                            else:
                                for var in tabsim:
                                    removedTabs = var.split("\t")
                                    if(termino1.getLexema() == removedTabs[1]):#Verifica que en la R24 se haya declarado variable
                                        error1=0
                                        if(removedTabs[0] != lastFuncType): #Lo compara con el tipo de la funcion
                                            error1 = 2
                                        if(removedTabs[2] != lastFuncName): #Lo compara con el contexto de la funcion
                                            error1 = 3
                                        break

                if(error > 0):
                    if(error1 == 1):
                        exception = "<"+termino1.getLexema() + "> Variable no declarada Regla #" + str(regla)
                    if(error1 == 2):
                        exception="<"+termino1.getLexema()+"> <"+lastFuncType+"> Variable del return y Funcion no son del mismo tipo de dato o no estan definidas Regla #" + str(regla)
                    if(error1 == 3):
                        exception="<"+termino1.getLexema()+"> <"+lastFuncName+"> Variable del return definida en diferente contexto Regla #" + str(regla)
                return ["Error semantico en: ",exception],[]

            elif (regla == 40):
                error=1
                id=ter[0].getLexema()

                args=[]
                for nodoaux in noter:
                    r1=nodoaux.getRegla()
                    while(r1 != 52):
                        nodoaux=nodoaux.getNoTerminales()[0]
                        r1=nodoaux.getRegla()
                    try:
                        args.append(nodoaux.getNoTerminales()[0].getTerminales()[0])
                    except: 
                        args.append(self.obtFType(lastCallFType))
                for var in tabsim:
                    removedTabs = var.split("\t")
                    if(id == removedTabs[1]):
                        lastCallFType=removedTabs[0]
                        error=0
                if(error == 1):
                    exception="<"+id+"> Funcion no definida Regla #" + str(regla)
                    return ["Error semantico en: ",exception],[]
                

                for arg in args:
                    try:
                        int(id)
                    except:
                        try:
                            float(id)
                        except:
                            if(id != "true" and id != "false"):
                                if(id != '"'):
                                    id=arg.getLexema()
                                    error=5
                                    for var in tabsim:
                                        removedTabs = var.split("\t")
                                        if(id == removedTabs[1]):
                                            error=0
                                            aux=removedTabs[2]
                                    if(error == 5):
                                        exception="<"+id+"> Atributo no existe Regla #" + str(regla)
                                        return ["Error semantico en: ",exception],[]
                                    
                                    error=3
                                    if(lastFuncName == aux):
                                        error=0

                                    if(error == 3):
                                        exception="<"+id+"> Variable en el argumento no definida Regla #" + str(regla)
                                        return ["Error semantico en: ",exception],[]
                

            elif (regla == 44):
                error=1
                nodoaux=noter[0]
                r1=nodoaux.getRegla()
                while(r1 != 52):
                    nodoaux=nodoaux.getNoTerminales()[0]
                    r1=nodoaux.getRegla()
                
                try:
                    termino1=nodoaux.getNoTerminales()[0].getTerminales()[0]
                except: 
                    termino1=self.obtFType(lastCallFType)

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
                        exception="<"+termino1.getLexema()+"> Variable no definida Regla #" + str(regla)
                    elif(error == 4):
                        exception="<"+termino1.getLexema()+"> Variable no es tipo bool Regla #" + str(regla)
                    return ["Error semantico en: ",exception],[]

            elif (regla == 45):
                error=1
                nodoaux=noter[0]
                r1=nodoaux.getRegla()
                while(r1 != 52):
                    nodoaux=nodoaux.getNoTerminales()[0]
                    r1=nodoaux.getRegla()
                
                try:
                    termino1=nodoaux.getNoTerminales()[0].getTerminales()[0]
                except: 
                    termino1=self.obtFType(lastCallFType)

                if(termino1.getLexema() == "true" or termino1.getLexema() == "false"):
                    error=0
                else:
                    for var in tabsim:
                        removedTabs = var.split("\t")
                        if(termino1.getLexema() == removedTabs[1]):#Verifica que en la R45 se haya declarado variable
                            error=0
                            aux1=removedTabs[0] #Obtiene el tipo
                    if(error == 0 and aux1 != "bool"):
                        error = 4
                
                if(error > 0):
                    if(error == 1):
                        exception="<"+termino1.getLexema()+"> Variable no definida Regla #" + str(regla)
                    elif(error == 4):
                        exception="<"+termino1.getLexema()+"> Variable no es tipo int o float Regla #" + str(regla)
                    return ["Error semantico en: ",exception+" Regla #"+str(regla)],[]

            elif(regla >= 46 and regla <=51):
                error=1
                aux1="aux1"
                aux2="aux2"
                nodoaux=noter[0]
                r1=nodoaux.getRegla()
                while(r1 != 52):
                    nodoaux=nodoaux.getNoTerminales()[0]
                    r1=nodoaux.getRegla()
                try:
                    termino1=nodoaux.getNoTerminales()[0].getTerminales()[0]
                except: 
                    termino1=self.obtFType(lastCallFType)

                nodoaux=noter[1]
                r2=nodoaux.getRegla()
                while(r2 != 52):
                    nodoaux=nodoaux.getNoTerminales()[0]
                    r2=nodoaux.getRegla()
                try:
                    termino2=nodoaux.getNoTerminales()[0].getTerminales()[0]
                except: 
                    termino2=self.obtFType(lastCallFType)
                
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
                            if(termino1.getLexema() == "true" or termino1.getLexema() == "false"):
                                aux1="bool"
                                error=0
                            else:
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
                            if(termino2.getLexema() == "true" or termino2.getLexema() == "false"):
                                aux2="bool"
                                error=0
                            else:
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
                        exception="<"+termino1.getLexema()+"> o <"+termino2.getLexema()+"> Variable no definida Regla #" + str(regla)
                    elif(error == 2):
                        exception="<"+termino1.getLexema()+"> <"+termino2.getLexema()+"> Variables son de diferente tipo de dato o no estan definidas Regla #" + str(regla)
                    elif(error == 4):
                        exception="<"+termino1.getLexema()+"> Variable no es tipo int o float Regla #" + str(regla)
                    return ["Error semantico en: ",exception],[],


            for i in noter:
                provis = Semantico(i)
                tabsim,context = provis.preAnalisis(tabsim,context,lastFuncType,lastFuncName,lastCallFType)
        except:
            pass

        return tabsim,context

    def analisis(self):
        tabsim,context = self.preAnalisis([],[" "]," "," "," ")
        return tabsim
    
    def obtFType(self,cadena):
        if(cadena == "int"):
            return Valor("0",cadena,1)
        if(cadena == "float"):
            return Valor("0.0",cadena,2)
        if(cadena == "string"):
            return Valor("string",cadena,3)
        if(cadena == "bool"):
            return Valor("false",cadena,-1)
        return("void",cadena,-1)


