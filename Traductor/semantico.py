from valor import Valor
from nodo import Nodo

class Semantico:
    raiz=Nodo(-1,[],[])

    def __init__(self,raiz):
        self.raiz = raiz

    def analisis(self,t,c):
        tabsim=t
        context=c
        ter=self.raiz.getTerminales()
        noter=self.raiz.getNoTerminales()
        cont=0
        aux=""
        for i in ter:
            if(i.getNum() == 4):
                aux=i.getLexema()+"\t"+ter[cont+1].getLexema()+"\t"+context[-1]
                tabsim.append(aux)
                print()
                if(ter[-1].getLexema() == ")"):
                    context.append(ter[cont+1].getLexema())

            cont+=1

        for i in noter:
            provis = Semantico(i)
            tabsim,context = provis.analisis(tabsim,context)


        return tabsim,context
