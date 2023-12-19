import xml.etree.ElementTree as ET
from lista_doble import *
from multimedia import *


class CancionesXML:
    def __init__(self, ruta):
        self.datos_en_xml = ET.parse(ruta).getroot()
        self.lista_canciones = ListaDoble()

    def cargar_canciones(self):
        for cancion_elem in self.datos_en_xml.findall('cancion'):
            nombre = cancion_elem.get('nombre')
            artista = cancion_elem.findtext('artista')
            album = cancion_elem.findtext('album')
            imagen = cancion_elem.findtext('imagen')
            ruta = cancion_elem.findtext('ruta')

            nueva_cancion = Cancion(nombre, artista, album, imagen, ruta)

            self.lista_canciones.agregar_al_final(nueva_cancion)
        return self.lista_canciones


class ListasXML:
    def __init__(self, ruta):
        self.datos_en_xml = ET.parse(ruta).getroot()
        self.lista_listas = ListaDoble()

    def cargar_listas(self):
        for lista_elem in self.datos_en_xml.findall('lista'):
            nombre_et = lista_elem.get('nombre')
            reproduccion_et = lista_elem.get('reproduccion')
            for cancion_elem in lista_elem.findall('cancion'):
                nombre = cancion_elem.get('nombre')
                artista = cancion_elem.findtext('artista')
                album = cancion_elem.findtext('album')
                imagen = cancion_elem.findtext('imagen')
                ruta = cancion_elem.findtext('ruta')
                nueva_lista = Playlist(
                    nombre_et, reproduccion_et, nombre, artista, album, imagen, ruta)
                self.lista_listas.agregar_al_final(nueva_lista)
                tamano = self.lista_listas.size
                print("tamaño de la lista: ", tamano)
                print("-------------------------------------------------")
                print("LISTASSSSSSS")
                nodo = self.lista_listas.primero
                while nodo:
                    print(nodo.dato.lista)
                    nodo = nodo.siguiente

                print("REPRODUCCIONNN")
                nodo = self.lista_listas.primero
                while nodo:
                    print(nodo.dato.reproduccion)
                    nodo = nodo.siguiente

                print("canciones cargadas")
                nodo = self.lista_listas.primero
                while nodo:
                    print(nodo.dato.cancion)
                    nodo = nodo.siguiente

                print("artista")
                nodo = self.lista_listas.primero
                while nodo:
                    print(nodo.dato.artista)
                    nodo = nodo.siguiente
                print("album")
                nodo = self.lista_listas.primero
                while nodo:
                    print(nodo.dato.album)
                    nodo = nodo.siguiente
                print("imagen")
                nodo = self.lista_listas.primero
                while nodo:
                    print(nodo.dato.imagen)
                    nodo = nodo.siguiente
                print("ruta")
                nodo = self.lista_listas.primero
                while nodo:
                    print(nodo.dato.ruta)
                    nodo = nodo.siguiente
        return self.lista_listas
