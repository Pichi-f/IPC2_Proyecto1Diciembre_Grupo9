class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.anterior = None
        self.siguiente = None

    def getDato(self):
        return self.dato

    def getAnterior(self):
        return self.anterior

    def getSiguiente(self):
        return self.siguiente

    def setDato(self, dato):
        self.dato = dato

    def setAnterior(self, anterior):
        self.anterior = anterior

    def setSiguiente(self, siguiente):
        self.siguiente = siguiente

