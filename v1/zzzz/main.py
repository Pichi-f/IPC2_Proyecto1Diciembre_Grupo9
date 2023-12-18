import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import Button
from tkinter import Tk, Button

import sys
import os

from procesador import *
from lista_doble import *
from multimedia import *
from procesador import CancionesXML

class ScrollText(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.text = tk.Text(
            self,
            bg="#232526",
            foreground="#e8e8e8",
            insertbackground="#444546",
            selectbackground="#5b5d5d",
            width=27,
            height=17,
            font=("Courier New", 11),
        )

        self.scrollbar = tk.Scrollbar(
            self, orient=tk.VERTICAL, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scrollbar.set)

        self.numberLines = TextLineNumbers(self, width=30, bg="#2c2e2f")
        self.numberLines.attach(self.text)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.numberLines.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
        self.text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.text.bind("<Key>", self.onPressDelay)
        self.text.bind("<Button-1>", self.numberLines.redraw)
        self.scrollbar.bind("<Button-1>", self.onScrollPress)
        self.text.bind("<MouseWheel>", self.onPressDelay)

    def onScrollPress(self, *args):
        self.scrollbar.bind("<B1-Motion>", self.numberLines.redraw)

    def onScrollRelease(self, *args):
        self.scrollbar.unbind("<B1-Motion>", self.numberLines.redraw)

    def onPressDelay(self, *args):
        self.after(2, self.numberLines.redraw)

    def get(self, *args, **kwargs):
        return self.text.get(*args, **kwargs)

    def insert(self, *args, **kwargs):
        return self.text.insert(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.text.delete(*args, **kwargs)

    def index(self, *args, **kwargs):
        return self.text.index(*args, **kwargs)

    def redraw(self):
        self.numberLines.redraw()


class ScrollTextSnd(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.text = tk.Text(
            self,
            bg="#232526",
            foreground="#e8e8e8",
            insertbackground="#444546",
            selectbackground="#5b5d5d",
            width=27,
            height=16,
            font=("Courier New", 11),
        )

        self.scrollbar = tk.Scrollbar(
            self, orient=tk.VERTICAL, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scrollbar.set)

        self.numberLines = TextLineNumbers(self, width=30, bg="#2c2e2f")
        self.numberLines.attach(self.text)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.numberLines.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
        self.text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.text.bind("<Key>", self.onPressDelay)
        self.text.bind("<Button-1>", self.numberLines.redraw)
        self.scrollbar.bind("<Button-1>", self.onScrollPress)
        self.text.bind("<MouseWheel>", self.onPressDelay)

    def onScrollPress(self, *args):
        self.scrollbar.bind("<B1-Motion>", self.numberLines.redraw)

    def onScrollRelease(self, *args):
        self.scrollbar.unbind("<B1-Motion>", self.numberLines.redraw)

    def onPressDelay(self, *args):
        self.after(2, self.numberLines.redraw)

    def get(self, *args, **kwargs):
        return self.text.get(*args, **kwargs)

    def insert(self, *args, **kwargs):
        return self.text.insert(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.text.delete(*args, **kwargs)

    def index(self, *args, **kwargs):
        return self.text.index(*args, **kwargs)

    def redraw(self):
        self.numberLines.redraw()


class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs, highlightthickness=0)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        """redraw line numbers"""
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(
                2,
                y,
                anchor="nw",
                text=linenum,
                fill="gray",
                font=("Courier New", 11, "bold"),
            )
            i = self.textwidget.index("%s+1line" % i)

class Sistema():
    def __init__(self):
        self.principal()
        self.carga = None
        self.carga_lista = None
        self.lista_canciones = None  # Inicializa lista_canciones como None u otra valor por defecto
        self.indice_actual = 0  

    # primera ventana Principal
    def principal(self):
        self.ventana = Tk()
        self.ventana.title("IPCmusic")
        self.ventana.geometry("810x350")
        self.ventana.config(bg="#f0f0f0")
        self.ventana.resizable(0, 0)
        self.centrar(self.ventana, 810, 350)
        # self.ventana.overrideredirect(True)

        # visualizador de consola principal
        self.scroll_consola = ScrollText(self.ventana)
        self.scroll_consola.place(x=500, y=40)
        self.ventana.after(200, self.scroll_consola.redraw())

        btn_visualizar = Button(self.ventana, text="Mostrar listas", command=self.mostrar_listasA,
                                width=17, height=1, font=("Lucida Sans", 10), bg="gray", fg="#e8e8e8")
        btn_visualizar.place(x=570, y=10)

        # botones sobre visualizador Añadir

        btn_seleccionar = Button(self.ventana, text="Buscar lista", command=self.buscar_lista,
                                 width=17, height=1, font=("Lucida Sans", 10), bg="#232526", fg="#e8e8e8")
        btn_seleccionar.place(x=300, y=10)

        # items medio
        self.lbl_cancion = Label(self.ventana, text="Canción", bg=(
            "#f0f0f0"), fg=("gray"), font=("Lucida Sans", 10))
        self.lbl_cancion.place(x=260, y=70)
        self.lbl_artista = Label(self.ventana, text="Artista", bg=(
            "#f0f0f0"), fg=("gray"), font=("Lucida Sans", 10))
        self.lbl_artista.place(x=260, y=115)
        self.lbl_album = Label(self.ventana, text="Album", bg=(
            "#f0f0f0"), fg=("gray"), font=("Lucida Sans", 10))
        self.lbl_album.place(x=260, y=160)

        # ENTRY ALL
        self.entry_buscar = Entry(
            self.ventana, width=30, justify="center", font=("Lucida Sans", 10))
        self.entry_buscar.place(x=25, y=14)

        self.entry_cancion = Entry(
            self.ventana, width=25, justify="center", font=("Lucida Sans", 10))
        self.entry_cancion.place(x=260, y=90)
        self.entry_artista = Entry(
            self.ventana, width=25, justify="center", font=("Lucida Sans", 10))
        self.entry_artista.place(x=260, y=135)
        self.entry_album = Entry(
            self.ventana, width=25, justify="center", font=("Lucida Sans", 10))
        self.entry_album.place(x=260, y=180)

        self.image = tk.PhotoImage(file="no.png")
        # Insertarla en una etiqueta.
        self.label = tk.Label(
            self.ventana, image=self.image, width=200, height=200)
        self.label.place(x=25, y=60)

        # menu archivo reportes tus listas
        self.menu = Menu(self.ventana)
        self.ventana.config(menu=self.menu)
        self.filemenu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label=" Archivo ", menu=self.filemenu, background='#2b2b2b',
                              foreground='white', activeforeground='black', activebackground='gray52')
        self.filemenu.add_command(label="Cargar biblioteca", command=self.cargar_archivo, background='#2b2b2b',
                                  foreground='white', activeforeground='black', activebackground='gray52')
        self.filemenu.add_command(label="Salir", command=self.inicializar, background='#2b2b2b',
                                  foreground='white', activeforeground='black', activebackground='gray52')

        self.filemenu2 = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label=" Reportes ", menu=self.filemenu2, background='#2b2b2b',
                              foreground='white', activeforeground='black', activebackground='gray52')
        self.filemenu2.add_command(label="Top canciones/artistas [HTML]", command=self.inicializar, background='#2b2b2b',
                                   foreground='white', activeforeground='black', activebackground='gray52')
        self.filemenu2.add_command(label="Estructura de biblioteca [GRAPHVIZ]", command=self.inicializar, background='#2b2b2b',
                                   foreground='white', activeforeground='black', activebackground='gray52')

        self.filemenu3 = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label=" Tus listas ", menu=self.filemenu3, background='#2b2b2b',
                              foreground='white', activeforeground='black', activebackground='gray52', command=self.inicializar)
        self.filemenu3.add_command(label="Añadir o Eliminar", command=self.pestana_anadir, background='#2b2b2b',
                                   foreground='white', activeforeground='black', activebackground='gray52')

        self.filemenu3.add_command(label="Guardar sesión", command=self.guardar_sesion, background='#2b2b2b',
                                   foreground='white', activeforeground='black', activebackground='gray52')

        # boton aleatorio normal
        self.boton_reproduccion_aleatoria = Button(self.ventana, text="A", command=self.reproduccion_aleatoria_de_lista,
               width=4, height=1, font=("Lucida Sans", 10), bg="#232526", fg="#e8e8e8")
        self.boton_reproduccion_aleatoria.place(x=100, y=307)

        Button(self.ventana, text="<", command=self.reproducir_cancion_anterior,
               width=4, height=1, font=("Lucida Sans", 10), bg="#232526", fg="#e8e8e8").place(x=150, y=307)

        Button(self.ventana, text="⏸", command=self.pausar_cancion,
               width=4, height=1, font=("Lucida Sans", 10), bg="#232526", fg="#e8e8e8").place(x=200, y=307)

        Button(self.ventana, text="▶", command=self.continuar_cancion,
               width=4, height=1, font=("Lucida Sans", 10), bg="#232526", fg="#e8e8e8").place(x=250, y=307)

        Button(self.ventana, text=">", command=self.reproducir_cancion_siguiente,
               width=4, height=1, font=("Lucida Sans", 10), bg="#232526", fg="#e8e8e8").place(x=300, y=307)

        self.boton_reproduccion_normal = Button(self.ventana, text="N", command=self.reproduccion_normal_de_lista,
               width=4, height=1, font=("Lucida Sans", 10), bg="#232526", fg="#e8e8e8")
        self.boton_reproduccion_normal.place(x=350, y=307)

        self.label_tiempo_transcurrido = tk.Label(
            self.ventana, text="0:00", font=("Arial", 8), fg="black")
        self.label_tiempo_transcurrido.place(x=80, y=280)

        self.barra_progreso = tk.Scale(self.ventana, from_=0, to=100, orient=tk.HORIZONTAL,
                                       length=200, showvalue=0, command=self.inicializar)
        self.barra_progreso.place(
            x=110, y=290, anchor=tk.W, bordermode="outside", width=270
        )

        self.label_tiempo_total = tk.Label(
            self.ventana, text="0:00", font=("Arial", 8), fg="black")
        self.label_tiempo_total.place(x=380, y=280)

        self.ventana.mainloop()

    def centrar(self, ventana, ancho, alto):  # centra la ventana
        altura_pantalla = ventana.winfo_screenheight()
        ancho_pantalla = ventana.winfo_screenwidth()
        ancho_x = (ancho_pantalla//2) - (ancho//2)
        altura_y = (altura_pantalla//2) - (alto//2)
        ventana.geometry(f"+{ancho_x}+{altura_y}")

    def inicializar(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)

    def cargar_archivo(self):
        filepath = askopenfilename(
            filetypes=[("archivos XML", "*.xml"), ("Todos los archivos", "*.*")])
        if not filepath:
            return
        self.carga = CancionesXML(filepath)
        self.lista_canciones = self.carga.cargar_canciones()  # Almacena la lista de canciones cargadas

        self.cargar_archivo_defecto()  # Llama al método para cargar las listas por defecto

    # segunda ventana Playlist
    def cargar_archivo_defecto(self):
        filepath = "listas.xml"
        self.carga_lista = ListasXML(filepath)
        self.lista_listas = self.carga_lista.cargar_listas()  # Almacena la lista de listas cargadas

    def mostrar_listasA(self):
        try:
            print("Mostrando listas cargadas:")
            self.scroll_consola.delete("1.0", tk.END)
            listas_en = self.carga_lista.lista_listas.primero
            valores_mostrados = set()

            while listas_en:
                valor_guardado = listas_en.dato.lista
                if valor_guardado not in valores_mostrados:
                    self.scroll_consola.insert(
                        tk.END, f"{valor_guardado}" + "\n")
                    valores_mostrados.add(valor_guardado)

                listas_en = listas_en.siguiente

            print("Tamaño de lista:", len(valores_mostrados))
        except Exception as e:
            print("Error al ver listado:", e)

    def buscar_lista(self):
        valor_entrada = self.entry_buscar.get()

        listas_en = self.carga_lista.lista_listas.primero

        while listas_en:
            valor_comparado = listas_en.dato.lista
            if valor_entrada == valor_comparado:
                self.entry_cancion.insert(
                    tk.END, f"{listas_en.dato.cancion}\n")
                self.entry_artista.insert(
                    tk.END, f"{listas_en.dato.artista}\n")
                self.entry_album.insert(tk.END, f"{listas_en.dato.album}\n")
                imagen_path = listas_en.dato.imagen
                self.mostrar_imagen(imagen_path)
                break
            listas_en = listas_en.siguiente
        else:
            print("No se encontró la lista:", valor_entrada)
    
    def reproducir_cancion_siguiente(self):
        if self.boton_reproduccion_normal['state'] == 'normal' and self.boton_reproduccion_aleatoria['state'] == 'disabled':
            cancion_aleatoria = self.lista_canciones.reproducir_aleatorio()
            if cancion_aleatoria:
                # Actualiza los valores en los Entry con la información de la siguiente canción aleatoria
                self.entry_cancion.delete(0, END)
                self.entry_cancion.insert(0, cancion_aleatoria.cancion)

                self.entry_artista.delete(0, END)
                self.entry_artista.insert(0, cancion_aleatoria.artista)

                self.entry_album.delete(0, END)
                self.entry_album.insert(0, cancion_aleatoria.album)
            else:
                # Manejo si no hay siguiente canción disponible
                self.entry_cancion.delete(0, END)
                self.entry_cancion.insert(0, "No hay más canciones")

                self.entry_artista.delete(0, END)
                self.entry_artista.insert(0, "")

                self.entry_album.delete(0, END)
                self.entry_album.insert(0, "")
        elif self.boton_reproduccion_normal['state'] == 'disabled' and self.boton_reproduccion_aleatoria['state'] == 'normal':
            siguiente_cancion = self.lista_canciones.reproducir_siguiente()
            if siguiente_cancion:
                # Actualiza los valores en los Entry con la información de la siguiente canción en modo normal
                self.entry_cancion.delete(0, "end")
                self.entry_cancion.insert(0, siguiente_cancion.cancion)

                self.entry_artista.delete(0, "end")
                self.entry_artista.insert(0, siguiente_cancion.artista)

                self.entry_album.delete(0, "end")
                self.entry_album.insert(0, siguiente_cancion.album)
            else:
                # Manejo si no hay siguiente canción disponible
                self.entry_cancion.delete(0, END)
                self.entry_cancion.insert(0, "No hay más canciones")

                self.entry_artista.delete(0, END)
                self.entry_artista.insert(0, "")

                self.entry_album.delete(0, END)
                self.entry_album.insert(0, "")
        elif self.boton_reproduccion_normal['state'] == 'normal' and self.boton_reproduccion_aleatoria['state'] == 'normal':
            siguiente_cancion = self.lista_canciones.reproducir_siguiente()
            if siguiente_cancion:
                # Actualiza los valores en los Entry con la información de la siguiente canción
                self.entry_cancion.delete(0, END)
                self.entry_cancion.insert(0, siguiente_cancion.cancion)

                self.entry_artista.delete(0, END)
                self.entry_artista.insert(0, siguiente_cancion.artista)

                self.entry_album.delete(0, END)
                self.entry_album.insert(0, siguiente_cancion.album)
            else:
                # Manejo si no hay siguiente canción disponible
                self.entry_cancion.delete(0, END)
                self.entry_cancion.insert(0, "No hay más canciones")

                self.entry_artista.delete(0, END)
                self.entry_artista.insert(0, "")

                self.entry_album.delete(0, END)
                self.entry_album.insert(0, "")

    def reproduccion_normal_de_lista(self):
        if self.boton_reproduccion_aleatoria.cget("state") == "normal":
            # Deshabilitar botón aleatorio y habilitar botón normal
            self.boton_reproduccion_aleatoria.config(state="disabled")
            self.boton_reproduccion_normal.config(state="normal")
            self.reproducir_cancion_siguiente()
        elif self.boton_reproduccion_aleatoria.cget("state") == "disabled":
            # Habilitar botón aleatorio y deshabilitar botón normal
            self.boton_reproduccion_aleatoria.config(state="normal")
            self.boton_reproduccion_normal.config(state="disabled")

    def reproduccion_aleatoria_de_lista(self):
        if self.boton_reproduccion_aleatoria.cget("state") == "normal":  
            # Deshabilitar botón normal y habilitar botón aleatorio
            self.boton_reproduccion_aleatoria.config(state="disabled")
            self.boton_reproduccion_normal.config(state="normal")

    def reproducir_cancion_anterior(self):
        cancion_anterior = self.lista_canciones.reproducir_anterior()
        if cancion_anterior:
            self.entry_cancion.delete(0, END)
            self.entry_cancion.insert(0, cancion_anterior.cancion)

            self.entry_artista.delete(0, END)
            self.entry_artista.insert(0, cancion_anterior.artista)

            self.entry_album.delete(0, END)
            self.entry_album.insert(0, cancion_anterior.album)
        else:
            # Manejo si no hay canción anterior disponible
            self.entry_cancion.delete(0, END)
            self.entry_cancion.insert(0, "No hay más canciones")

            self.entry_artista.delete(0, END)
            self.entry_artista.insert(0, "")

            self.entry_album.delete(0, END)
            self.entry_album.insert(0, "")
            # Otra lógica o manejo para cuando no haya más canciones disponibles
        pass

    def pausar_cancion(self):
        pass

    def continuar_cancion(self):
        pass

   

    def mostrar_imagen(self, imagen_path):
        # Cargar la imagen
        nueva_imagen = tk.PhotoImage(file=imagen_path)

        # Actualizar la referencia de la imagen en el widget Label existente
        self.label.config(image=nueva_imagen)
        self.label.image = nueva_imagen  # Conservar la referencia a la nueva imagen
    
    def actualizar_imagen(self, imagen):
        self.image = tk.PhotoImage(file=imagen)
        self.label.config(image=self.image)

    def pestana_anadir(self):
        self.ventana.destroy()
        self.anadir()

    def guardar_sesion(self):
        self.carga_lista.generar_archivo_xml()

    def anadir(self):
        self.ventana_anadir = Tk()
        self.ventana_anadir.title("Playlist")
        self.ventana_anadir.geometry("710x340")
        self.ventana_anadir.config(bg="#f0f0f0")
        self.centrar(self.ventana_anadir, 710, 340)
        self.ventana_anadir.resizable(0, 0)

        self.scroll_consola_snd = ScrollTextSnd(self.ventana_anadir)
        self.scroll_consola_snd.place(x=400, y=47)
        self.ventana_anadir.after(200, self.scroll_consola_snd.redraw())

        # botones visualizar canciones, artistas
        btn_visualizar_canciones = Button(self.ventana_anadir, text="Ver canciones", command=self.mostrar_canciones,
                                          width=15, height=1, font=("Lucida Sans", 10), bg="gray", fg="#e8e8e8")
        btn_visualizar_canciones.place(x=410, y=17)

        btn_visualizar_artistas = Button(self.ventana_anadir, text="Ver artistas", command=self.mostrar_artistas,
                                         width=15, height=1, font=("Lucida Sans", 10), bg="gray", fg="#e8e8e8")
        btn_visualizar_artistas.place(x=545, y=17)

        # items izquierda
        Label(self.ventana_anadir, text="Crear playlist o añadir a existente", bg=(
            "#f0f0f0"), fg=("gray"), font=("Lucida Sans", 10)).place(x=70, y=20)
        Label(self.ventana_anadir, text="lista", bg=(
            "#f0f0f0"), fg=("gray"), font=("Lucida Sans", 10)).place(x=25, y=64)
        Label(self.ventana_anadir, text="cancion", bg=(
            "#f0f0f0"), fg=("gray"), font=("Lucida Sans", 10)).place(x=155, y=64)
        Label(self.ventana_anadir, text="lista", bg=(
            "#f0f0f0"), fg=("gray"), font=("Lucida Sans", 10)).place(x=25, y=114)
        Label(self.ventana_anadir, text="artista", bg=(
            "#f0f0f0"), fg=("gray"), font=("Lucida Sans", 10)).place(x=155, y=114)

        self.entry_lista = Entry(
            self.ventana_anadir, width=14, justify="center", font=("Lucida Sans", 10))
        self.entry_lista.place(x=25, y=84)

        self.entry_cancion = Entry(
            self.ventana_anadir, width=14, justify="center", font=("Lucida Sans", 10))
        self.entry_cancion.place(x=150, y=84)

        self.entry_lista2 = Entry(
            self.ventana_anadir, width=14, justify="center", font=("Lucida Sans", 10))
        self.entry_lista2.place(x=25, y=134)

        self.entry_artista = Entry(
            self.ventana_anadir, width=14, justify="center", font=("Lucida Sans", 10))
        self.entry_artista.place(x=150, y=134)

        Button(self.ventana_anadir, text="Añadir", command=self.anadir_lista_cancion,
               width=12, height=1, font=("Lucida Sans", 10), bg="#232526", fg="#e8e8e8").place(x=275, y=80)
        Button(self.ventana_anadir, text="Añadir", command=self.anadir_lista_artista,
               width=12, height=1, font=("Lucida Sans", 10), bg="#232526", fg="#e8e8e8").place(x=275, y=130)

        # eliminar lista
        Label(self.ventana_anadir, text="¿Desea eliminar una lista?", bg=(
            "#f0f0f0"), fg=("gray"), font=("Lucida Sans", 10)).place(x=100, y=190)

        self.entry_elimina_lista = Entry(
            self.ventana_anadir, width=14, justify="center", font=("Lucida Sans", 10))
        self.entry_elimina_lista.place(x=25, y=234)

        Button(self.ventana_anadir, text="Eliminar", command=self. eliminar_lista,
               width=12, height=1, font=("Lucida Sans", 10), bg="#232526", fg="#e8e8e8").place(x=160, y=230)

        Button(self.ventana_anadir, text="Ver listas", command=self.mostrar_listas_en_snd,
               width=12, height=1, font=("Lucida Sans", 10), bg="#232526", fg="#e8e8e8").place(x=275, y=230)

        Button(self.ventana_anadir, text="Volver a Menu", command=self.volver,
               width=12, height=1, font=("Lucida Sans", 10), bg="gray", fg="#e8e8e8").place(x=140, y=294)

    def mostrar_canciones(self):
        try:
            print("Mostrando canciones cargadas:")
            self.scroll_consola_snd.delete("1.0", tk.END)
            canciones_en = self.carga.lista_canciones.primero
            tamano = self.carga.lista_canciones.size
            while canciones_en:
                for i in range(tamano):
                    self.scroll_consola_snd.insert(
                        tk.END, f"{canciones_en.dato.cancion}" + "\n")
                    canciones_en = canciones_en.siguiente
                break
        except Exception as e:
            print("Error al ver listado:", e)

    def mostrar_artistas(self):
        try:
            print("Mostrando artistas cargados:")
            self.scroll_consola_snd.delete("1.0", tk.END)
            artistas_en = self.carga.lista_canciones.primero
            valores_mostrados = set()

            while artistas_en:
                valor_guardado = artistas_en.dato.artista
                if valor_guardado not in valores_mostrados:
                    self.scroll_consola_snd.insert(
                        tk.END, f"{valor_guardado}" + "\n")
                    valores_mostrados.add(valor_guardado)
                artistas_en = artistas_en.siguiente
        except Exception as e:
            print("Error al ver listado:", e)

    def anadir_lista_cancion(self):
        valor_entrada_lista = self.entry_lista.get()
        valor_entrada_cancion = self.entry_cancion.get()

        listas_en = self.carga_lista.lista_listas.primero
        canciones_en = self.carga.lista_canciones.primero

        while listas_en and canciones_en and valor_entrada_lista and valor_entrada_cancion:
            if valor_entrada_cancion == canciones_en.dato.cancion:
                valor_salida = Playlist(
                    valor_entrada_lista, listas_en.dato.reproduccion, canciones_en.dato.cancion, canciones_en.dato.artista, canciones_en.dato.album, canciones_en.dato.imagen, canciones_en.dato.ruta)
                agregando = self.carga_lista.lista_listas.agregar_al_final(
                    valor_salida)
                break
            listas_en = listas_en.siguiente
            canciones_en = canciones_en.siguiente
        else:
            print("No se encontró la lista:", valor_entrada_lista)

    # def anadir_lista_cancion(self):
    #     valor_entrada_lista = self.entry_lista.get()
    #     valor_entrada_cancion = self.entry_cancion.get()

    #     listas_en = self.carga_lista.lista_listas.primero
    #     canciones_en = self.carga.lista_canciones.primero

    #     while listas_en and valor_entrada_lista:
    #         valor_comparado_lista = listas_en.dato.lista
    #         if valor_entrada_lista == valor_comparado_lista:
    #             valor_comparado_cancion = canciones_en.dato.cancion
    #             while valor_comparado_cancion and valor_entrada_cancion:
    #                 if valor_entrada_cancion == valor_comparado_cancion:
    #                     nueva_cancion = Playlist(valor_entrada_lista, listas_en.dato.reproduccion, valor_entrada_cancion,
    #                                              canciones_en.dato.artista, canciones_en.dato.album, canciones_en.dato.imagen, canciones_en.dato.ruta)
    #                     self.carga_lista.lista_listas.agregar_al_final(
    #                         nueva_cancion)
    #                     return

    #                 canciones_en = canciones_en.siguiente
    #             listas_en = listas_en.siguiente
    #         elif valor_entrada_lista != valor_comparado_lista:
    #             valor_comparado_cancion = canciones_en.dato.cancion
    #             while valor_comparado_cancion and valor_entrada_cancion:
    #                 if valor_entrada_cancion == valor_comparado_cancion:
    #                     nueva_cancion = Playlist(valor_entrada_lista, listas_en.dato.reproduccion, valor_entrada_cancion,
    #                                              canciones_en.dato.artista, canciones_en.dato.album, canciones_en.dato.imagen, canciones_en.dato.ruta)
    #                     self.carga_lista.lista_listas.agregar_al_final(
    #                         nueva_cancion)

    #                 canciones_en = canciones_en.siguiente
    #             listas_en = listas_en.siguiente

    def anadir_lista_cancion(self):
        try:
            valor_entrada_lista = self.entry_lista.get()
            valor_entrada_cancion = self.entry_cancion.get()

            listas_en = self.carga_lista.lista_listas.primero
            canciones_en = self.carga.lista_canciones.primero

            valor_comparado_cancion = canciones_en.dato.cancion
            while valor_comparado_cancion and valor_entrada_cancion:
                if valor_entrada_cancion == valor_comparado_cancion:
                    nueva_cancion = Playlist(valor_entrada_lista, listas_en.dato.reproduccion, valor_entrada_cancion,
                                             canciones_en.dato.artista, canciones_en.dato.album, canciones_en.dato.imagen, canciones_en.dato.ruta)
                    self.carga_lista.lista_listas.agregar_al_final(
                        nueva_cancion)
                    break
                canciones_en = canciones_en.siguiente
            else:
                print("No se encontro la cancion:", valor_entrada_cancion)
        except Exception as e:
            print("Error", e)

    def anadir_lista_artista(self):
        pass

    def eliminar_lista(self):
        pass

    def mostrar_listas_en_snd(self):
        try:
            print("Mostrando listas cargadas:")
            self.scroll_consola_snd.delete("1.0", tk.END)
            listas_en = self.carga_lista.lista_listas.primero
            valores_mostrados = set()

            while listas_en:
                valor_guardado = listas_en.dato.lista
                if valor_guardado not in valores_mostrados:
                    self.scroll_consola_snd.insert(
                        tk.END, f"{valor_guardado}" + "\n")
                    valores_mostrados.add(valor_guardado)

                listas_en = listas_en.siguiente

            print("Tamaño de lista:", len(valores_mostrados))
        except Exception as e:
            print("Error al ver listado:", e)

    def volver(self):
        self.ventana_anadir.destroy()
        self.principal()


Sistema()
