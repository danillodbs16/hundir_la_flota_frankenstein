import tkinter as tk
from tkinter import simpledialog
from random import randint
#from main_game import *
from Functions import *
from time import sleep
from Sounds import *

from tkinter import messagebox
import pyfxr
import pygame
import time

font=16
class JuegoGUI_facil:

    def __init__(self, master):

        self.master = master
        self.master.title("Batalla Naval - Dificultad: Facil")
        self.user = simpledialog.askstring("Nombre del jugador", "Introduce tu nombre:")

        if not self.user:
            self.user = "Jugador"

        self.Jugador = Tablero()
        self.Jugador.crear_flota_aleatoria()
        self.Computador = Tablero()
        self.Computador.crear_flota_aleatoria()
        self.n = self.Computador.n
        self.tab_Computador = self.Computador.tab
        self.tab_Jugador = self.Jugador.tab
        self.turno_jugador = True

        # NUEVO: lista de objetivos cercanos a impactos (Para el Computador)
        self.targets = []

        #

        self.frame_msg = tk.Frame(master)
        self.frame_msg.grid(row=0, column=0, columnspan=2, pady=30)
        self.msg = tk.Label(self.frame_msg, text=f"Hola{self.user} ¡Bienvenido al juego!",font=("Arial",font))
        self.msg.pack()
        self.vidas_lbl = tk.Label(self.frame_msg,
        text=f"Vidas Oponente: {self.Computador.total_vidas}",font=("Arial",font))
        self.vidas_lbl.pack()

        #TABLERO COMPUTADOR

        self.frame_comp = tk.Frame(master)
        self.frame_comp.grid(row=1, column=0, padx=50)
        tk.Label(self.frame_comp,
        text="Tablero del Oponente",font=("Arial",font)).grid(row=0, column=0, columnspan=self.n)

        self.botones_comp = []

        for i in range(self.n):
            fila = []
            for j in range(self.n):

                b = tk.Button(self.frame_comp,
                              width=3,
                              height=1,
                              bg="light blue",
                              command=lambda x=i, y=j: self.disparo_jugador(x, y))

                b.grid(row=i+1, column=j)
                fila.append(b)

            self.botones_comp.append(fila)

        #TABLERO JUGADOR
        self.frame_jug = tk.Frame(master)
        self.frame_jug.grid(row=1, column=1, padx=50)
        tk.Label(self.frame_jug,
        text="Tu tablero",font=("Arial",font)).grid(row=0, column=0, columnspan=self.n)

        self.botones_jug = []

        for i in range(self.n):
            fila = []
            for j in range(self.n):

                if self.tab_Jugador[i][j] == 1:
                    b = tk.Button(self.frame_jug,
                                  width=3,
                                  height=1,
                                  state="disabled",
                                  bg="dark gray")
                else:
                    b = tk.Button(self.frame_jug,
                                  width=3,
                                  height=1,
                                  state="disabled",
                                  bg="light blue")

                b.grid(row=i+1, column=j)
                fila.append(b)

            self.botones_jug.append(fila)

    #FUNCION NUEVA-

    def vecinos(self, i, j):

        posibles = [(i+1,j),(i-1,j),(i,j+1),(i,j-1)]
        vecinos_validos = []

        for x,y in posibles:
            if 0 <= x < self.n and 0 <= y < self.n:
                if (x,y) not in self.Jugador.historial:
                    vecinos_validos.append((x,y))

        return vecinos_validos

    #DISPARO JUGADOR

    def disparo_jugador(self, i, j):

        if not self.turno_jugador:
            return

        if (i,j) in self.Computador.historial:
            self.msg.config(text="Ya disparaste ahí, intenta otra coordenada",font=("Arial",14))
            return

        resultado = self.Computador.tiro(i,j)
        self.Computador.historial.append((i,j))

        if resultado:

            self.botones_comp[i][j].config(bg="red", text="X", state="disabled")
            self.msg.config(text=f"¡{self.user} ha acertado! Vuelve a tirar")
            shot_sound()

        else:

            self.botones_comp[i][j].config(bg="blue", text="O", state="disabled")
            self.msg.config(text="Agua. Turno del Oponente")
            self.turno_jugador = False

            water_splash_sound()

            self.master.after(500, self.turno_computador)

        self.vidas_lbl.config(
        text=f"Vidas Oponente: {self.Computador.total_vidas}",font=("Arial",12))

        if self.Computador.total_vidas == 0:
            self.msg.config(text=f"¡Enhorabuena {self.user}! Has ganado!",font=("Arial",font))
            messagebox.showinfo("Enhorabuena",
            f"Enhorabuena, {self.user}¡Has ganado!")

            self.desactivar_tablero()

    #TURNO COMPUTADOR

    def turno_computador(self):

        repetir = True

        while repetir and self.Jugador.total_vidas > 0:

            # Facil: juego aleatorio
            i,j = randint(0,self.n-1), randint(0,self.n-1)

            while (i,j) in self.Jugador.historial:
                i,j = randint(0,self.n-1), randint(0,self.n-1)

            resultado = self.Jugador.tiro(i,j)

            self.Jugador.historial.append((i,j))

            if resultado:

                self.botones_jug[i][j].config(bg="red", text="X")
                self.msg.config(
                text=f"El oponente acertó! Vuelve a tirar")

                # AÑADIR VECINOS
                nuevos = self.vecinos(i,j)
                self.targets.extend(nuevos)
                repetir = True
                shot_sound()
                sleep(0.5)

            else:

                self.botones_jug[i][j].config(bg="light blue", text="O")
                self.msg.config(
                text=f"¡Oponente falló!. {self.user}, es tu turno!")
                repetir = False
                water_splash_sound()
                sleep(0.5)

        if self.Jugador.total_vidas == 0:

            self.msg.config(text=f"¡Qué pena {self.user}! Has perdido :'(",font=("Arial",font))
            messagebox.showinfo("Fin del juego", f"Has perdido. :'(",font=("Arial",font))
            self.desactivar_tablero()

        self.turno_jugador = True

    # DESACTIVAR TABLERO

    def desactivar_tablero(self):
        for fila in self.botones_comp:
            for b in fila:
                b.config(state="disabled")
