import tkinter as tk
font=16
root = tk.Tk()
root.title("Dificultad")
#from GUI import *
from main_game.normal import *
from main_game.facil import *
from main_game.dificil import *
from Functions import *
from Sounds import *
dificultad = None

label = tk.Label(root, text=f"¡Hola ! Elija la dificultad del juego:",font=("Arial",font))
label.pack(padx=20, pady=10)

facil_btn = tk.Button(root, text="Fácil",font=("Arial",font), width=10,
                      command=lambda: [globals().update(dificultad="Facil"), root.destroy()])
facil_btn.pack(pady=5)

dificil_btn = tk.Button(root, text="Medio",font=("Arial",font), width=10,
                        command=lambda: [globals().update(dificultad="Medio"), root.destroy()])
dificil_btn.pack(pady=5)


dificil_btn = tk.Button(root, text="Difícil",font=("Arial",font), width=10,
                        command=lambda: [globals().update(dificultad="Dificil"), root.destroy()])
dificil_btn.pack(pady=5)

root.mainloop()

print("Dificultad elegida:", dificultad)

root = tk.Tk()
#root.state("zoomed")
if dificultad=="Facil":
    app = JuegoGUI_facil(root)
    root.mainloop()
    

elif dificultad=="Medio":
    app = JuegoGUI_medio(root)
    root.mainloop()

else:
    app = JuegoGUI_dificil(root)
    root.mainloop()

# playHLF.py
def main():
    # your existing code to start the game
    print("Que empiece el juego!")
    # e.g., launch GUI, run the game loop, etc.

if __name__ == "__main__":
    main()
