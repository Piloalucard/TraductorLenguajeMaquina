from lexico import Lexico
from sintactico import Sintactico
from semantico import Semantico
from nodo import Nodo
import os
import time


def openFiles(msg, mode):
    if os.name == "ce" or os.name == "nt" or os.name == "dos":
        import easygui
        band = 0
        err = 0
        print("Elige tu archivo "+msg)
        while band == 0:
            nombre = ""
            try:
                if(mode == 1):
                    nombre = str(easygui.fileopenbox(msg="Selecciona archivo .den", title=None,
                                 default="*", filetypes=['*.den', "Denisse Files"], multiple=False))
                elif(mode == 2):
                    nombre = str(easygui.fileopenbox(
                        msg=None, title=None, default="*", filetypes=['*.lr'], multiple=False))
                if nombre == "None":
                    print("ERROR, No abriste un archivo\nSaliendo...")
                    time.sleep(1.5)
                    band = 1
                    err = 1
                else:
                    print("Buena eleccion de archivo")
                    band = 1
            except:
                print("ERROR")
                input()
                band = 0
        if err == 1:
            exit()
        else:
            return nombre

    nombre = input("Ingrese la ruta "+msg+": ")
    return str(nombre)


def clear():
    if os.name == "posix":
       os.system("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
       os.system("cls")


def main():
    print("")
    print("  /Traductor/")
    print("")

    # Lee los archivos
    codigo = []
    reglas = []
    nom = openFiles("de codigo", 1)
    try:
        archivo = open(nom, mode="r", encoding="utf-8")
    except:
        return
    nomSinExt = nom.replace(".den", "")
    while(True):
        linea = archivo.readline()
        if not linea:
            break
        codigo.append(linea)
    archivo.close()
    print("")
    try:
        archivo = open("compilador.lr", mode="r", encoding="utf-8")
    except:
        archivo = open("./Traductor/compilador.lr", mode="r", encoding="utf-8")
    
    while(True):
        linea = archivo.readline()
        if not linea:
            break
        reglas.append(linea)
    archivo.close()

    lex = Lexico()
    for i in codigo:
        lex.addFuente(i)
    lex.analisis()

    band = False
    lista = lex.getLista()
    for i in lista:
        if(i.getNum() == -1):
            band = True
            print(i.toString())

    if(band):
        print("Tiene errores lexicos, porfavor corrija su archivo!")
    else:
        print("---------------------------------------------------")
        print("Lexico correcto")
        print("---------------------------------------------------")
        print(lex.obtLexico())
        sin = Sintactico(lista, reglas)

        resultado, raiz = sin.analisis()
        if(resultado != ""):
            cont = 1
            for i in codigo:
                if(resultado in i):
                    print("Se encontro un error de sintaxis en la linea: "+str(cont))
                    print(i)
                    return
                cont += 1
        print("---------------------------------------------------")
        print("Sintactico correcto")
        print("---------------------------------------------------")
        raiz.recorrer()
        print("")
        sem = Semantico(raiz)
        tabsim = sem.analisis()
        if(tabsim[0] == "Error semantico en: "):
            print(tabsim[0]+tabsim[1], end="")
            return
        print("")
        print("---------------------------------------------------")
        print("Semantico correcto")
        print("---------------------------------------------------")
        tb = open(nomSinExt+".tabsim", mode="w", encoding="utf-8")

        for line in tabsim:
            print(line)

        for x in tabsim:
            tb.write(x+"\n")
        tb.close

        print("")
        print("")
        print("    [T]raduccion realizada con exito! ", end="")
            

main()
input()
clear()