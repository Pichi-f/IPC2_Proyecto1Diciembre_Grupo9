import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename

import sys
import os

from procesador import *


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

        btn_visualizar = Button(self.ventana, text="Mostrar listas", command=self.inicializar,
                                width=17, height=1, font=("Lucida Sans", 10), bg="gray", fg="#e8e8e8")
        btn_visualizar.place(x=570, y=10)

        # botones sobre visualizador Añadir

        # items top
        self.entry_buscar = Entry(
            self.ventana, width=30, justify="center", font=("Lucida Sans", 10))
        self.entry_buscar.place(x=25, y=14)

        btn_seleccionar = Button(self.ventana, text="Buscar lista", command=self.inicializar,
                                 width=17, height=1, font=("Lucida Sans", 10), bg="#232526", fg="#e8e8e8")
        btn_seleccionar.place(x=300, y=10)

        # items izquierda
        self.image = tk.PhotoImage(file="Album.png")
        # Insertarla en una etiqueta.
        self.label = tk.Label(
            self.ventana, image=self.image, width=200, height=200)
        self.label.place(x=25, y=60)

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

        self.entry_cancion = Entry(
            self.ventana, width=25, justify="center", font=("Lucida Sans", 10))
        self.entry_cancion.place(x=260, y=90)
        self.entry_artista = Entry(
            self.ventana, width=25, justify="center", font=("Lucida Sans", 10))
        self.entry_artista.place(x=260, y=135)
        self.entry_album = Entry(
            self.ventana, width=25, justify="center", font=("Lucida Sans", 10))
        self.entry_album.place(x=260, y=180)

        self.entry_album.insert(0, "ejemplo de Album")  # ejemplo de entrada

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

        # boton aleatorio normal
        Button(self.ventana, text="A", command=self.inicializar,
               width=4, height=1, font=("Lucida Sans", 10), bg="#232526", fg="#e8e8e8").place(x=100, y=307)

        Button(self.ventana, text="<", command=self.inicializar,
               width=4, height=1, font=("Lucida Sans", 10), bg="#232526", fg="#e8e8e8").place(x=150, y=307)

        Button(self.ventana, text="⏸", command=self.inicializar,
               width=4, height=1, font=("Lucida Sans", 10), bg="#232526", fg="#e8e8e8").place(x=200, y=307)

        Button(self.ventana, text="▶", command=self.inicializar,
               width=4, height=1, font=("Lucida Sans", 10), bg="#232526", fg="#e8e8e8").place(x=250, y=307)

        Button(self.ventana, text=">", command=self.inicializar,
               width=4, height=1, font=("Lucida Sans", 10), bg="#232526", fg="#e8e8e8").place(x=300, y=307)

        Button(self.ventana, text="N", command=self.inicializar,
               width=4, height=1, font=("Lucida Sans", 10), bg="#232526", fg="#e8e8e8").place(x=350, y=307)

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
        self.carga.cargar_canciones()
        self.cargar_archivo_defecto()

    # segunda ventana Playlist
    def cargar_archivo_defecto(self):
        filepath = "listas.xml"
        self.carga_lista = ListasXML(filepath)
        self.carga_lista.cargar_listas()

    def pestana_anadir(self):
        self.ventana.destroy()
        self.anadir()

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

        Button(self.ventana_anadir, text="Añadir", command=self.anadirA,
               width=12, height=1, font=("Lucida Sans", 10), bg="#232526", fg="#e8e8e8").place(x=275, y=80)
        Button(self.ventana_anadir, text="Añadir", command=self.anadirB,
               width=12, height=1, font=("Lucida Sans", 10), bg="#232526", fg="#e8e8e8").place(x=275, y=130)

        # eliminar lista
        Label(self.ventana_anadir, text="¿Desea eliminar una lista?", bg=(
            "#f0f0f0"), fg=("gray"), font=("Lucida Sans", 10)).place(x=100, y=190)

        self.entry_elimina_lista = Entry(
            self.ventana_anadir, width=14, justify="center", font=("Lucida Sans", 10))
        self.entry_elimina_lista.place(x=25, y=234)

        Button(self.ventana_anadir, text="Eliminar", command=self.anadirB,
               width=12, height=1, font=("Lucida Sans", 10), bg="#232526", fg="#e8e8e8").place(x=160, y=230)

        Button(self.ventana_anadir, text="Ver listas", command=self.anadirB,
               width=12, height=1, font=("Lucida Sans", 10), bg="#232526", fg="#e8e8e8").place(x=275, y=230)

        Button(self.ventana_anadir, text="Volver a Menu", command=self.volver,
               width=12, height=1, font=("Lucida Sans", 10), bg="gray", fg="#e8e8e8").place(x=140, y=294)

    def mostrar_canciones(self):
        pass

    def mostrar_artistas(self):
        pass

    def anadirA(self):
        pass

    def anadirB(self):
        pass

    def volver(self):
        self.ventana_anadir.destroy()
        self.principal()


Sistema()
