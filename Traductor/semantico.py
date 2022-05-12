from cmath import exp
from valor import Valor
from nodo import Nodo
import random
import string  

class Semantico:
    raiz=Nodo(-1,[],[])

    def __init__(self,raiz):
        self.raiz = raiz

    def preAnalisis(self,t,c,a,lft,lfn,lcft,r,r2,rs):
        tabsim=t
        context=c
        assembler=a
        ter=self.raiz.getTerminales()
        noter=self.raiz.getNoTerminales()
        regla=self.raiz.getRegla()
        aux=""
        exception = ""
        lastFuncType=lft
        lastFuncName=lfn
        lastCallFType=lcft
        ran=r
        ran2=r2
        r21s=rs

        
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
                    if(len(assembler) > 0):
                        assembler.append("\tret")
                    assembler.append(p2+":")
                    lastFuncType=p1
                    lastFuncName=p2

                for var in tabsim:
                    removedTabs = var.split("\t")
                    if(p2 == removedTabs[1]):
                        if(p3 == removedTabs[2] or " " == removedTabs[2]):
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
                
                #Assembler
                written=True
                if(noter[0].getRegla() == 52):
                    if(type2 == "int" or type2 == "float" or type2 == "string"):
                        assembler.append("\tmov "+termino1.getLexema()+lastFuncName+","+termino2.getLexema())
                    elif(type2 == "bool"):
                        if(termino2.getLexema() == "true"):
                            assembler.append("\tmov "+termino1.getLexema()+lastFuncName+",1")
                        else:
                            assembler.append("\tmov "+termino1.getLexema()+lastFuncName+",0")
                    else:
                        written=False
                else:
                    r21s.append("\tmov "+termino1.getLexema()+lastFuncName+",ax")

               
                for var in tabsim:
                    removedTabs = var.split("\t")
                    if(termino1.getLexema() == removedTabs[1] and type1 =="t1"):
                        type1=removedTabs[0]
                        context1=removedTabs[2]
                        error1=0
                    if(termino2.getLexema() == removedTabs[1] and type2 =="t2"):
                        type2=removedTabs[0]
                        context2=removedTabs[2]
                        error2=0
                    
                if(not written):
                    if(noter[0].getRegla() == 52):
                        assembler.append("\tmov ax,"+termino2.getLexema()+lastFuncName)
                        assembler.append("\tmov "+termino1.getLexema()+lastFuncName+",ax")
                    else:
                        r21s.append("\tmov "+termino1.getLexema()+lastFuncName+",ax")
                        



                if(type1 != type2):
                    error1=2
                
                
                if(context1 != "1c" and context1 != " "):
                    if(context2 != "2c" and context2 != " "):
                        if(context1 != context2):
                            error1 = 3
                if(error2 == 1):
                    exception = "<"+termino2.getLexema() + "> Variable 2 no declarada Regla #" + str(regla)
                    return ["Error semantico en: ",exception],[],[]

                if(error1 > 0):
                    if(error1 == 1):
                        exception = "<"+termino1.getLexema() + "> Variable 1 no declarada Regla #" + str(regla)
                    if(error1 == 2):
                        exception="<"+termino1.getLexema()+"> <"+termino2.getLexema()+"> Variable y termino de asignacion son de diferente tipo de dato Regla #" + str(regla)
                    if(error1 == 3):
                        exception="<"+termino1.getLexema()+"> <"+termino2.getLexema()+"> Variables definidas en diferentes contextos Regla #" + str(regla)
                    return ["Error semantico en: ",exception],[],[]
                
            elif(regla == 22 or regla == 23):
                nodoRoot = noter[0]
                expresion = nodoRoot.getTerminales()[0].getLexema()
                while(expresion == "&&" or expresion == "||"):
                    nodoEmp = noter[0]
                    nodoSig = noter[1]
                    expresionInt = noter[0].getTerminales()[0].getLexema()
                    while(expresionInt == "&&" or expresionInt == "||"):
                        nodoEmp = nodoEmp.getNoTerminales()[0]
                        nodoSig = nodoEmp.getNoTerminales()[1]
                        expresionInt = nodoEmp.getTerminales()[0].getLexema()
                        
                    nodoaux = nodoEmp
                    r1=nodoaux.getRegla()
                    while(r1 != 52):
                        nodoaux=nodoaux.getNoTerminales()[0]
                        r1=nodoaux.getRegla()
                    try:    
                        termino1=nodoaux.getNoTerminales()[0].getTerminales()[0]
                    except: 
                        termino1=self.obtFType(lastCallFType)
                    
                    reg1=termino1.getLexema()

                    nodoaux = nodoSig
                    r1=nodoaux.getRegla()
                    while(r1 != 52):
                        nodoaux=nodoaux.getNoTerminales()[0]
                        r1=nodoaux.getRegla()
                    try:    
                        termino2=nodoaux.getNoTerminales()[0].getTerminales()[0]
                    except: 
                        termino2=self.obtFType(lastCallFType)
                    reg2=termino2.getLexema()
                    
                    

                    if(regla == 22):
                        if(termino1.getNum() == 0):
                            assembler.append("\tmov ax,"+reg1+lastFuncName)
                        else:
                            assembler.append("\tmov ax,"+reg1)
                        if(termino2.getNum() == 0):
                            assembler.append("\tmov bx,"+reg2+lastFuncName)
                        else:
                            assembler.append("\tmov bx,"+reg2)
                        assembler.append("\tcmp ax,bx")
                        ran.append("endif"+str(''.join(random.choices(string.ascii_lowercase, k = 8))))
                        if(expresion == "=="):
                            assembler.append("\tjne "+ran[-1])
                        elif(expresion == "!="):
                            assembler.append("\tje "+ran[-1])
                        elif(expresion == "<"):
                            assembler.append("\tjnb "+ran[-1])
                        elif(expresion == "<="):
                            assembler.append("\tjnbe "+ran[-1])
                        elif(expresion == ">"):
                            assembler.append("\tjna "+ran[-1])
                        elif(expresion == ">="):
                            assembler.append("\tjnae "+ran[-1])
                    else:
                        ran3=str(''.join(random.choices(string.ascii_lowercase, k = 8)))
                        assembler.append("\t"+ran3+":")
                        if(termino1.getNum() == 0):
                            assembler.append("\tmov ax,"+reg1+lastFuncName)
                        else:
                            assembler.append("\tmov ax,"+reg1)
                        if(termino2.getNum() == 0):
                            assembler.append("\tmov bx,"+reg2+lastFuncName)
                        else:
                            assembler.append("\tmov bx,"+reg2)
                        assembler.append("\tcmp ax,bx")
                        ran2.append("endwhile"+str(''.join(random.choices(string.ascii_lowercase, k = 8))))
                        if(expresion == "=="):
                            assembler.append("\tjne "+ran2[-1])
                        elif(expresion == "!="):
                            assembler.append("\tje "+ran2[-1])
                        elif(expresion == "<"):
                            assembler.append("\tjnb "+ran2[-1])
                        elif(expresion == "<="):
                            assembler.append("\tjnbe "+ran2[-1])
                        elif(expresion == ">"):
                            assembler.append("\tjna "+ran2[-1])
                        elif(expresion == ">="):
                            assembler.append("\tjnae "+ran2[-1])
                        ran2.append("nolabel"+str(''.join(random.choices(string.ascii_lowercase, k = 8))))
                        ran2.append("jmp "+ran3)

                    nodoRoot = nodoRoot.getNoTerminales()[0]
                    expresion = nodoRoot.getTerminales()[0].getLexema()
                
                nodoaux = noter[0].getNoTerminales()[0]
                r1 = nodoaux.getRegla()
                while(r1 != 52):
                    nodoaux = nodoaux.getNoTerminales()[0]
                    r1 = nodoaux.getRegla()
                try:    
                    termino1=nodoaux.getNoTerminales()[0].getTerminales()[0]
                except: 
                    termino1=self.obtFType(lastCallFType)
                    
                reg1=termino1.getLexema()

                nodoaux = noter[0].getNoTerminales()[1]
                r1=nodoaux.getRegla()
                while(r1 != 52):
                    nodoaux=nodoaux.getNoTerminales()[0]
                    r1=nodoaux.getRegla()
                try:    
                    termino2=nodoaux.getNoTerminales()[0].getTerminales()[0]
                except: 
                    termino2=self.obtFType(lastCallFType)
                reg2=termino2.getLexema()
                
                
                if(regla == 22):
                    if(termino1.getNum() == 0):
                        assembler.append("\tmov ax,"+reg1+lastFuncName)
                    else:
                        assembler.append("\tmov ax,"+reg1)
                    if(termino2.getNum() == 0):
                        assembler.append("\tmov bx,"+reg2+lastFuncName)
                    else:
                        assembler.append("\tmov bx,"+reg2)
                    assembler.append("\tcmp ax,bx")
                    ran.append("endif"+str(''.join(random.choices(string.ascii_lowercase, k = 8))))
                    if(expresion == "=="):
                        assembler.append("\tjne "+ran[-1])
                    elif(expresion == "!="):
                        assembler.append("\tje "+ran[-1])
                    elif(expresion == "<"):
                        assembler.append("\tjnb "+ran[-1])
                    elif(expresion == "<="):
                        assembler.append("\tjnbe "+ran[-1])
                    elif(expresion == ">"):
                        assembler.append("\tjna "+ran[-1])
                    elif(expresion == ">="):
                        assembler.append("\tjnae "+ran[-1])
                else:
                    ran3=str(''.join(random.choices(string.ascii_lowercase, k = 8)))
                    assembler.append("\t"+ran3+":")
                    if(termino1.getNum() == 0):
                        assembler.append("\tmov ax,"+reg1+lastFuncName)
                    else:
                        assembler.append("\tmov ax,"+reg1)
                    if(termino2.getNum() == 0):
                        assembler.append("\tmov bx,"+reg2+lastFuncName)
                    else:
                        assembler.append("\tmov bx,"+reg2)
                    assembler.append("\tcmp ax,bx")
                    ran2.append("endwhile"+str(''.join(random.choices(string.ascii_lowercase, k = 8))))
                    if(expresion == "=="):
                        assembler.append("\tjne "+ran2[-1])
                    elif(expresion == "!="):
                        assembler.append("\tje "+ran2[-1])
                    elif(expresion == "<"):
                        assembler.append("\tjnb "+ran2[-1])
                    elif(expresion == "<="):
                        assembler.append("\tjnbe "+ran2[-1])
                    elif(expresion == ">"):
                        assembler.append("\tjna "+ran2[-1])
                    elif(expresion == ">="):
                        assembler.append("\tjnae "+ran2[-1])
                    ran2.append("nolabel"+str(''.join(random.choices(string.ascii_lowercase, k = 8))))
                    ran2.append("jmp "+ran3)
                

            
                
            elif(regla == 26):
                assembler.append("\t"+ran.pop(-1)+":")
            elif(regla == 27):
                ran2.append("endelse"+str(''.join(random.choices(string.ascii_lowercase, k = 8))))
                ran2.append("nolabel"+str(''.join(random.choices(string.ascii_lowercase, k = 8))))
                ran2.append("nolabel"+str(''.join(random.choices(string.ascii_lowercase, k = 8))))
                assembler.append("\tjmp "+ran2[-1])
                assembler.append("\t"+ran.pop(-1)+":")
            elif(regla == 19 and len(ran2) > 0):
                if(len(ran) == 0):
                    assembler.append("\t"+ran2.pop(-1)+":")
                    assembler.append("\t"+ran2.pop(-1)+":")
                    assembler.append("\t"+ran2.pop(-1)+":")
                else:
                    assembler.append("\t"+ran2.pop(-1)+":")
                    assembler.append("\t"+ran2.pop(-1)+":")
            
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
                    return ["Error semantico en: ",exception],[],[]
                
                #Assembler
                if(termino1.getNum() == 0):
                    assembler.append("\tmov ax,"+termino1.getLexema()+lastFuncName)
                else:
                    assembler.append("\tmov ax,"+termino1.getLexema())
                
                
                

            elif (regla == 40):
                error=1
                id=ter[0].getLexema()
                #Assembler
                if(id == "print"):
                    try:
                        msg = noter[0].getNoTerminales()[0].getNoTerminales()[0].getTerminales()[0].getLexema()
                    except:
                        aux='" "'
                    
                    

                    if('"' in msg):
                        assembler.append("\tlea dx,"+msg.replace('"','').replace('-',''))
                        assembler.append("\tmov ah,9")
                        assembler.append("\tint 21h")
                        msg=msg.replace('"','')
                        msg='"'+msg+'$"'
                        aux=msg+'\tprint\t'+lastFuncName+"\t0"
                    else:
                        assembler.append("\tadd "+msg.replace('"','').replace('-','')+lastFuncName+",30h")
                        assembler.append("\tlea dx,"+msg.replace('"','').replace('-','')+lastFuncName)
                        assembler.append("\tmov ah,9")
                        assembler.append("\tint 21h")
                        assembler.append("\tsub "+msg.replace('"','').replace('-','')+lastFuncName+",30h")

                        aux=msg+'\tprint\t'+lastFuncName+"\t1"
                    assembler.append(aux)
                else:    
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
                        return ["Error semantico en: ",exception],[],[]
                    
                    #Assembler
                    assembler.append("\tjmp "+id)
                    

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
                                            return ["Error semantico en: ",exception],[],[]
                                        
                                        error=3
                                        if(lastFuncName == aux):
                                            error=0

                                        if(error == 3):
                                            exception="<"+id+"> Variable en el argumento no definida Regla #" + str(regla)
                                            return ["Error semantico en: ",exception],[],[]
                    
                    

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
                        exception="<"+termino1.getLexema()+"> Variable no es tipo int o float Regla #" + str(regla)
                    return ["Error semantico en: ",exception],[],[]
                
                #Assembler
                if(termino1.getNum() == 0):
                    assembler.append("\tadd "+termino1.getLexema()+lastFuncName+",1")

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
                
                try:
                    int(termino1.getLexema())
                    error=0
                except:
                    if(termino1.getLexema() == "true" or termino1.getLexema() == "false"):
                        error=0
                    else:
                        for var in tabsim:
                            removedTabs = var.split("\t")
                            if(termino1.getLexema() == removedTabs[1]):#Verifica que en la R45 se haya declarado variable
                                error=0
                                aux1=removedTabs[0] #Obtiene el tipo
                        if(error == 0 and aux1 != "bool" and aux1 != "int"):
                            error = 4
                    
                    if(error > 0):
                        if(error == 1):
                            exception="<"+termino1.getLexema()+"> Variable no definida Regla #" + str(regla)
                        elif(error == 4):
                            exception="<"+termino1.getLexema()+"> Variable no es tipo int o bool Regla #" + str(regla)
                        return ["Error semantico en: ",exception+" Regla #"+str(regla)],[],[]

                #Assembler
                if(termino1.getNum() == 0):
                    assembler.append("\tnot "+termino1.getLexema()+lastFuncName)

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
                    return ["Error semantico en: ",exception],[],[]
                
                #Assembler
                if(ter[0].getLexema() == "+"):
                    if(termino2.getNum() == 0):
                        assembler.append("\tmov ax,"+termino2.getLexema()+lastFuncName)
                    else:
                        assembler.append("\tmov ax,"+termino2.getLexema())
                    if(termino1.getNum() == 0):
                        assembler.append("\tadd ax,"+termino1.getLexema()+lastFuncName)
                    else:
                        assembler.append("\tadd ax,"+termino1.getLexema())
                
                if(ter[0].getLexema() == "-"):
                    if(termino2.getNum() == 0):
                        assembler.append("\tmov ax,"+termino2.getLexema()+lastFuncName)
                    else:
                        assembler.append("\tmov ax,"+termino2.getLexema())
                    if(termino1.getNum() == 0):
                        assembler.append("\tsub ax,"+termino1.getLexema()+lastFuncName)
                    else:
                        assembler.append("\tsub ax,"+termino1.getLexema())

                if(ter[0].getLexema() == "*"):
                    if(termino2.getNum() == 0):
                        assembler.append("\tmov ax,"+termino2.getLexema()+lastFuncName)
                    else:
                        assembler.append("\tmov ax,"+termino2.getLexema())
                    if(termino1.getNum() == 0):
                        assembler.append("\timul "+termino1.getLexema()+lastFuncName)
                    else:
                        assembler.append("\timul "+termino1.getLexema())
                
                if(ter[0].getLexema() == "/"):
                    if(termino2.getNum() == 0):
                        assembler.append("\tmov ax,"+termino2.getLexema()+lastFuncName)
                    else:
                        assembler.append("\tmov ax,"+termino2.getLexema())
                    if(termino1.getNum() == 0):
                        assembler.append("\tidiv "+termino1.getLexema()+lastFuncName)
                    else:
                        assembler.append("\tidiv "+termino1.getLexema())
            
            elif(regla == 52):
                if(len(r21s) > 0):
                    assembler.append(r21s.pop(-1))




            for i in noter:
                provis = Semantico(i)
                tabsim,context,assembler = provis.preAnalisis(tabsim,context,assembler,lastFuncType,lastFuncName,lastCallFType,ran,ran2,r21s)
        except:
            pass

        return tabsim,context,assembler

    def analisis(self):
        tabsim,context,assembler = self.preAnalisis([],[" "],[]," "," "," ",[],[],[])
        return tabsim,assembler
    
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


