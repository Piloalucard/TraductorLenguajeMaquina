from lexico import  Lexico
from sintactico import Sintactico
from nodo import Nodo
import os
import easygui
import time

def leer(msg,mode):
    band=0
    err=0
    print("Elige tu archivo "+msg)
    while band==0:
        nombre=""
        try:
            if(mode==1):
                nombre=str(easygui.fileopenbox(msg="Selecciona archivo .den",title=None,default="*",filetypes=['*.den',"Denisse Files"],multiple=False))
            elif(mode==2):
                nombre=str(easygui.fileopenbox(msg=None,title=None,default="*",filetypes=['*.lr'],multiple=False))
            if nombre == "None":
                print("ERROR, No abriste un archivo\nSaliendo...")
                time.sleep(1.5)
                band=1
                err=1
            else:
                print("Buena eleccion de archivo")
                band=1
        except:
            print("ERROR")
            input()
            band=0
    if err==1:
        exit()
    else:
        return nombre

def clear():
    if os.name == "posix":
       os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
       os.system ("cls")

def main():
    sal=0
    while(sal==0):
        print("")
        print("  /Traductor/")
        print("")
        

        #Lee los archivos
        codigo=[]
        reglas=[]
        archivo=open(leer("de codigo",1),mode="r",encoding="utf-8")
        while(True):
            linea=archivo.readline()
            if not linea: 
                break
            codigo.append(linea)
        archivo.close()
        print("")
        archivo=open(leer("de reglas",2),mode="r",encoding="utf-8")
        while(True):
            linea=archivo.readline()
            if not linea: 
                break
            reglas.append(linea)
        archivo.close()


        lex = Lexico()
        for i in codigo:
            lex.addFuente(i)
        lex.analisis()


        band=False
        lista=lex.getLista()
        for i in lista:
            if(i.getNum() == -1):
                band=True
                print(i.toString())

        if(band):
            print("Tiene errores lexicos, porfavor corrija su archivo!")
        else:
            print(lex.obtLexico())
            sin = Sintactico(lista,reglas)

            resultado,raiz=sin.analisis()
            if(resultado != ""):
                cont=1
                for i in codigo:
                    if(resultado in i):
                        print("Se encontro un error de sintaxis en la linea: "+str(cont))
                        print(i)
                        break
                    cont+=1
            else:
                print("Sintactico correcto")
                
                raiz.recorrer()
                

        print("")
        print("")
        sal = int(input("    [D]igite 0 para repetir el programa si lo desea: "))
        clear()

main()