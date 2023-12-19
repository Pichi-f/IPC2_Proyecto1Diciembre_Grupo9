import xml.etree.ElementTree as ET
from lista_doble import *
from multimedia import *

import graphviz


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
        ruta = "listas.xml"
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

    def graficar(self):
        g = graphviz.Digraph('G', filename='biblioteca.gv')
        g.attr(rankdir='TB', size='8,5')

        g.node('biblioteca', shape='egg', color='blue')

        lista_actual = self.lista_listas.primero
        nodos_creados = set()

        while lista_actual:
            lista_en = lista_actual.dato

            if lista_en.lista not in nodos_creados:
                g.node(lista_en.lista, shape='egg', color='green')
                g.edge('biblioteca', lista_en.lista)
                nodos_creados.add(lista_en.lista)

            cancion_node = lista_en.cancion + lista_en.lista
            if cancion_node not in nodos_creados:
                g.node(cancion_node, label=lista_en.cancion,
                       shape='egg', color='gray')
                g.edge(lista_en.lista, cancion_node)
                nodos_creados.add(cancion_node)

            lista_actual = lista_actual.siguiente

        dot_path = 'biblioteca.dot'
        g.save(dot_path)

        print(f"El archivo .dot se ha guardado en: {dot_path}")
        g.view()

    def ordenar_lista(self):
        if self.lista_listas.size < 2:
            return

        current = self.lista_listas.primero

        while current:
            inner_current = current.siguiente

            while inner_current:
                if current.dato.reproduccion < inner_current.dato.reproduccion:
                    current.dato, inner_current.dato = inner_current.dato, current.dato

                inner_current = inner_current.siguiente

            current = current.siguiente

    def generar_html(self):
        self.ordenar_lista()

        listas_ordenadas = self.lista_listas.primero

        ruta = "listas_mas_reproducidas.html"
        with open(ruta, "w") as salida:
            salida.write("<!DOCTYPE html>\n")
            salida.write("<html lang=\"es\">\n")
            salida.write("<head>\n")
            salida.write("\t<meta charset=\"UTF-8\">\n")
            salida.write(
                "\t<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n")
            salida.write("\t<title>Listas más reproducidas</title>\n")
            salida.write("\t<link rel=\"stylesheet\" href=\"style.css\">\n")
            salida.write("</head>\n")
            salida.write("<body>\n")
            salida.write("\t<h1>Listas más reproducidas</h1>\n")
            salida.write("\t<table>\n")
            salida.write("\t\t<tr>\n")
            salida.write("\t\t\t<th>Lista</th>\n")
            salida.write("\t\t\t<th>Reproducciones</th>\n")
            salida.write("\t\t</tr>\n")

            listas_procesadas = set()

            while listas_ordenadas:
                valor_guardado = listas_ordenadas.dato
                if valor_guardado.lista not in listas_procesadas:
                    salida.write("\t\t<tr>\n")
                    salida.write("\t\t\t<td>" +
                                 valor_guardado.lista + "</td>\n")
                    salida.write("\t\t\t<td>" +
                                 str(valor_guardado.reproduccion) + "</td>\n")
                    salida.write("\t\t</tr>\n")
                    listas_procesadas.add(valor_guardado.lista)
                listas_ordenadas = listas_ordenadas.siguiente

            salida.write("\t</table>\n")
            salida.write("</body>\n")
            salida.write("</html>\n")
