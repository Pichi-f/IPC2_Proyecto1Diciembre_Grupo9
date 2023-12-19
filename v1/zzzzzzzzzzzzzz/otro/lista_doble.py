from nodo import Nodo


class ListaDoble:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.size = 0

    def vacia(self):
        return self.primero == None

    def agregar_al_final(self, cancion):  # agrega al final de la lista
        if self.vacia():
            self.primero = self.ultimo = Nodo(cancion)
        else:
            aux = self.ultimo
            self.ultimo = aux.siguiente = Nodo(cancion)
            self.ultimo.anterior = aux
        self.size += 1

    def buscar_cancion(self, nombre):  # para crear listas de reproduccion
        actual = self.primero
        while actual:
            if actual.dato.nombre == nombre:
                return actual.dato
            actual = actual.siguiente
        return None

    def buscar_artista(self, nombre):
        actual = self.primero
        while actual:
            if actual.dato.nombre == nombre:
                return actual.dato
            actual = actual.siguiente
        return None

    def buscar_lista(self, lista):
        actual = self.primero
        while actual:
            if actual.dato.lista == lista:
                return actual.dato
            actual = actual.siguiente
        return None

    # solo eliminar playlist
    def eliminar(self, nombre):
        actual = self.primero
        while actual:
            if actual.nota.nombre == nombre:
                if actual.anterior:
                    if actual.siguiente:
                        actual.anterior.siguiente = actual.siguiente
                        actual.siguiente.anterior = actual.anterior
                        actual.siguiente = None
                        actual.anterior = None
                    else:
                        actual.anterior.siguiente = None
                        actual.anterior = None
                else:
                    if actual.siguiente:
                        self.primero = actual.siguiente
                        actual.siguiente.anterior = None
                    else:
                        self.primero = None
                return True
            else:
                actual = actual.siguiente
        return False
