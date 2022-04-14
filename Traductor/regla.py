class Regla:
    id=-1
    lon=-1
    nombre=""

    def __init__(self,id,l,n):
        self.id=id
        self.lon=l
        self.nombre=n
    
    def getId(self):
        return self.id

    def getLon(self):
        return self.lon
    
    def getNombre(self):
        return self.nombre