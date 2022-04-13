from lexico import  Lexico
from sintactico import Sintactico
import os

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
        lex = Lexico("if while return else")
        lex.analisis()
        print(lex.obtLexico())

        
        print("")
        print("")
        sal = int(input("    [D]igite 0 para repetir el programa si lo desea: "))
        clear()

main()