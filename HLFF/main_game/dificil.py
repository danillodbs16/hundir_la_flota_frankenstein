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

class JuegoGUI_dificil:
    def __init__(self, master):
        self.master = master
        self.master.title("Batalla Naval - Nivel: Dificil")
        
        # Pedimos el nombre del jugador
        self.user = simpledialog.askstring("Nombre del jugador", "Introduce tu nombre:")
        
        if not self.user:
            self.user = "Jugador"
        
        # Inicializamos tableros
        self.Jugador = Tablero()
        self.Jugador.crear_flota_aleatoria()
        
        self.Computador = Tablero()
        self.Computador.crear_flota_aleatoria()
        
        self.n = self.Computador.n
        
        self.tab_Computador=self.Computador.tab
        self.tab_Jugador=self.Jugador.tab
        
        self.turno_jugador = True
        
        # Mensajes
        self.frame_msg = tk.Frame(master)
        self.frame_msg.grid(row=0, column=0, columnspan=2, pady=10)
        
        self.msg = tk.Label(self.frame_msg,
                            text=f"Hola {self.user} ¡Bienvenido al juego!",
                            font=("Arial",font))
        self.msg.pack()
        
        self.vidas_lbl = tk.Label(self.frame_msg,
                                  text=f"Vidas Oponente: {self.Computador.total_vidas}",
                                  font=("Arial",font))
        self.vidas_lbl.pack()
        
        # TABLERO COMPUTADOR
        self.frame_comp = tk.Frame(master)
        self.frame_comp.grid(row=1, column=0, padx=20)
        
        tk.Label(self.frame_comp,
                 text="Tablero del Computador",
                 font=("Arial",font)).grid(row=0, column=0, columnspan=self.n)
        
        self.botones_comp = []
        
        for i in range(self.n):
            fila = []
            for j in range(self.n):
                
                b = tk.Button(self.frame_comp,
                              width=3,
                              height=1,
                              bg="light blue",
                              command=lambda x=i, y=j: self.disparo_jugador(x,y))
                
                b.grid(row=i+1, column=j)
                fila.append(b)
            
            self.botones_comp.append(fila)
        
        # TABLERO JUGADOR
        self.frame_jug = tk.Frame(master)
        self.frame_jug.grid(row=1, column=1, padx=20)
        
        tk.Label(self.frame_jug,
                 text="Tu tablero",
                 font=("Arial",font)).grid(row=0, column=0, columnspan=self.n)
        
        self.botones_jug = []
        
        for i in range(self.n):
            fila = []
            for j in range(self.n):
                
                if self.tab_Jugador[i][j]==1:
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
    
    # DISPARO JUGADOR
    
    def disparo_jugador(self, i, j):
        
        if not self.turno_jugador:
            return
        
        if (i,j) in self.Computador.historial:
            self.msg.config(text="Ya disparaste ahí, intenta otra coordenada")
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
        
        self.vidas_lbl.config(text=f"Vidas Oponente: {self.Computador.total_vidas}")
        
        if self.Computador.total_vidas == 0:
            
            self.msg.config(text=f"¡Enhorabuena {self.user}! Has ganado!")
            messagebox.showinfo("Enhorabuena", f"Enhorabuena {self.user}! ¡Has ganado!")
            
            self.desactivar_tablero()
    
    # TURNO COMPUTADOR
    
    def turno_computador(self):
        
        coords_jugador = list(self.Jugador.coord_to_barco.keys())
        repetir = True
        
        while repetir and self.Jugador.total_vidas > 0:
            
            i,j = randint(0,self.n-1), randint(0,self.n-1)
            count = 0
            
            while (i,j) in self.Jugador.historial and count < 10:
                
                count += 1
                
                val = np.random.randint(0,2)
                delta = [-2,2][np.random.randint(0,2)]
                
                i,j = coords_jugador[np.random.randint(0,len(coords_jugador))]
                
                if val == 0:
                    i,j = (abs(i+delta)%self.n , j)
                else:
                    i,j = (i , abs(j+delta)%self.n)
            
            resultado = self.Jugador.tiro(i,j)
            self.Jugador.historial.append((i,j))
            
            # DETECTAR DERROTA INMEDIATA
            if self.Jugador.total_vidas == 0:
                
                self.botones_jug[i][j].config(bg="red", text="X")
                
                self.msg.config(text=f"¡Qué pena {self.user}! Has perdido :'(")
                messagebox.showinfo("Fin del juego", "Has perdido :'(")
                
                self.desactivar_tablero()
                return
            
            if resultado:
                
                self.botones_jug[i][j].config(bg="red", text="X")
                self.msg.config(text="Oponente acertó y vuelve a tirar")
                
                repetir = True
                shot_sound()
            
            else:
                
                self.botones_jug[i][j].config(bg="light blue", text="O")
                self.msg.config(text=f"Oponente falló. {self.user}, es tu turno")
                
                repetir = False
                water_splash_sound()
        
        self.turno_jugador = True
    
    # DESACTIVAR TABLERO
    
    def desactivar_tablero(self):
        for fila in self.botones_comp:
            for b in fila:
                b.config(state="disabled")
