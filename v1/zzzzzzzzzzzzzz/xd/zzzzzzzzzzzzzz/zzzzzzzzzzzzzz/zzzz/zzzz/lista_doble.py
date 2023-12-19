from nodo import Nodo
import random
import tkinter as tk


class ListaDoble:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.size = 0
        self.size = 0
        self.indice_actual = 0  # Agregar el atributo indice_actual
        self.reproduccion_aleatoria = False

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

    def reproducir_siguiente(self):
        if not self.reproduccion_aleatoria:
            if self.indice_actual < self.size - 1:
                current = self.primero
                for _ in range(self.indice_actual):
                    current = current.siguiente

                current = current.siguiente
                self.indice_actual += 1

                return current.dato
            else:
                self.indice_actual = 0
                return self.primero.dato
        else:
            return self.reproducir_aleatorio()

    # Agrega un método para actualizar la imagen en la etiqueta
    def actualizar_imagen(self, imagen):
        self.image = tk.PhotoImage(file=imagen)
        self.label.config(image=self.image)

    def reproducir_anterior(self):
        if not self.reproduccion_aleatoria:
            if self.indice_actual > 0:
                current = self.primero
                for _ in range(self.indice_actual):
                    current = current.siguiente

                current = current.anterior
                self.indice_actual -= 1

                return current.dato
            else:
                current = self.primero
                while current.siguiente:
                    current = current.siguiente

                self.indice_actual = self.size - 1
                return current.dato
        else:
            return self.reproducir_aleatorio()

    def reproducir_aleatorio(self):
        if not self.vacia():
            self.reproduccion_activa = True

            # Generar un nuevo índice aleatorio
            nuevo_indice = random.randint(0, self.size - 1)
            while nuevo_indice == (self.indice_actual + 1) % self.size:
                nuevo_indice = random.randint(0, self.size - 1)

            self.indice_actual = nuevo_indice
            current = self.primero
            for _ in range(self.indice_actual):
                current = current.siguiente

            return current.dato
        else:
            return None
