from nodo import Nodo


class Cancion:
    def __init__(self, cancion, artista, album, imagen, ruta):
        self.cancion = cancion
        self.artista = artista
        self.album = album
        self.imagen = imagen
        self.ruta = ruta
        self.primer_dato = None


class Playlist:
    def __init__(self, lista, reproduccion, cancion, artista, album, imagen, ruta):
        self.lista = lista
        self.reproduccion = reproduccion
        self.cancion = cancion
        self.artista = artista
        self.album = album
        self.imagen = imagen
        self.ruta = ruta
        self.primer_dato = None

    def agregar_cancion(self, cancion):
        nuevo_nodo = Nodo(cancion)
        if not self.primer_dato:
            self.primer_dato = nuevo_nodo
            self.ultimo_dato = nuevo_nodo
        else:
            nuevo_nodo.anterior = self.ultimo_dato
            self.ultimo_dato.siguiente = nuevo_nodo
            self.ultimo_dato = nuevo_nodo


class ListaLista:
    def __init__(self, lista):
        self.lista = lista
        self.primer_dato = None
