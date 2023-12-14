import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename

import sys
import os

from procesador import Procesador


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

    def principal(self):
        self.ventana = Tk()
        self.ventana.title("IPCmusic")
        self.ventana.geometry("810x380")
        self.ventana.config(bg="#f0f0f0")
        self.ventana.resizable(0, 0)
        self.centrar(self.ventana, 810, 380)
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
        self.label.place(x=25, y=70)

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
        self.filemenu.add_command(label="Cargar biblioteca", command=self.inicializar, background='#2b2b2b',
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
        self.filemenu3.add_command(label="Añadir", command=self.inicializar, background='#2b2b2b',
                                   foreground='white', activeforeground='black', activebackground='gray52')

        # boton normal aleatorio

        btn_normal = Button(self.ventana, text="Normal", command=self.inicializar,
                            width=10, height=1, font=("Lucida Sans", 10), bg="#232526", fg="#e8e8e8")
        btn_normal.place(x=25, y=300)

        btn_aleatorio = Button(self.ventana, text="Aleatorio", command=self.inicializar,
                               width=10, height=1, font=("Lucida Sans", 10), bg="#232526", fg="#e8e8e8")
        btn_aleatorio.place(x=140, y=300)

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


Sistema()
