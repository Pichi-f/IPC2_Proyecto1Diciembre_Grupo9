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
        return self.lista_listas

    def generar_archivo_xml(self):
        ruta = "prueba_lista6.xml"
        with open(ruta, "w") as salida:
            salida.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            salida.write("<listaReproduccion>\n")
            lista_actual = self.lista_listas.primero
            current_lista = None
            while lista_actual:
                lista_en = lista_actual.dato
                if current_lista != lista_en.lista:
                    if current_lista:
                        salida.write("\t</lista>\n")
                    salida.write("\t<lista nombre=\"" + lista_en.lista +
                                 "\" reproduccion=\"" + lista_en.reproduccion + "\">\n")
                    current_lista = lista_en.lista

                salida.write("\t\t<cancion nombre=\"" +
                             lista_en.cancion + "\">\n")
                salida.write("\t\t\t<artista>" +
                             lista_en.artista + "</artista>\n")
                salida.write("\t\t\t<album>" + lista_en.album + "</album>\n")
                salida.write("\t\t\t<imagen>" +
                             lista_en.imagen + "</imagen>\n")
                salida.write("\t\t\t<ruta>" + lista_en.ruta + "</ruta>\n")
                salida.write("\t\t</cancion>\n")

                lista_actual = lista_actual.siguiente

            # Close the last list
            if current_lista:
                salida.write("\t</lista>\n")

            salida.write("</listaReproduccion>\n")

    # def graficar_
