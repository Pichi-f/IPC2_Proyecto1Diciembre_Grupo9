class Cancion:
    def __init__(self, cancion, artista, album, imagen, ruta):
        self.cancion = cancion
        self.artista = artista
        self.album = album
        self.imagen = imagen
        self.ruta = ruta
        self.primer_dato = None


class Playlist:
    def __init__(self, lista, cancion, artista, album, imagen, ruta):
        self.lista = lista
        self.cancion = cancion
        self.artista = artista
        self.album = album
        self.imagen = imagen
        self.ruta = ruta
        self.primer_dato = None
