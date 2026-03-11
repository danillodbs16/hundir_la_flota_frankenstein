import numpy as np

dirs = ["h", "v"]

class Tablero:
    def __init__(self, n=10):
        self.n = n
        self.tab = np.zeros((n, n), dtype=int)  # tablero real
        self.map = np.zeros((n, n), dtype=int)  # tablero visible al jugador
        self.status = {}  # info de barcos: coords + vidas
        self.barco_counter = 0
        self.coord_to_barco = {}  # para lookup rápido: coord -> barco_id
        self.total_vidas=0
        self.ganador=None
        self.historial=[]

    def add_barco(self, length, pos, dirr):
        i, j = pos

        if dirr == "h":
            if j + length > self.n:
                return False
            if np.sum(self.tab[i, j:j+length]) != 0:
                return False

            self.tab[i, j:j+length] = 1

            barco_id = self.barco_counter
            self.barco_counter += 1
            coords = [(i, j+k) for k in range(length)]
            self.status[barco_id] = {"coords": coords, "vidas": length}

            # actualizar mapa auxiliar
            for coord in coords:
                self.coord_to_barco[coord] = barco_id

            return True

        elif dirr == "v":
            if i + length > self.n:
                return False
            if np.sum(self.tab[i:i+length, j]) != 0:
                return False

            self.tab[i:i+length, j] = 1

            barco_id = self.barco_counter
            self.barco_counter += 1
            coords = [(i+k, j) for k in range(length)]
            self.status[barco_id] = {"coords": coords, "vidas": length}

            # actualizar mapa auxiliar
            for coord in coords:
                self.coord_to_barco[coord] = barco_id

            return True

        return False

   # def crear_flota_aleatoria(self):
    #    L = [5, 4, 3, 3, 2]

     #   for l in L:
     #       colocado = False
     #       intentos = 0

     #       while not colocado and intentos < 100:
     #           dirr = dirs[np.random.randint(0, 2)]

     #           if dirr == "h":
     #               i = np.random.randint(0, self.n)
     #               j = np.random.randint(0, self.n - l + 1)
     #           else:
     #               i = np.random.randint(0, self.n - l + 1)
     #               j = np.random.randint(0, self.n)

      #          colocado = self.add_barco(l, (i, j), dirr)
      #          intentos += 1
            
       #     if not colocado:
        #        print(f"No se pudo colocar el barco de tamaño {l}")
         #   self.total_vidas=sum([self.status[i]["vidas"] for i in self.status.keys()])

    def crear_flota_aleatoria(self):
        L = [5, 4, 3, 3, 2]

        for l in L:
            colocado = False
            intentos = 0

            while not colocado and intentos < 100:
                dirr = dirs[np.random.randint(0, 2)]

                if dirr == "h":
                    i = np.random.randint(0, self.n)
                    j = np.random.randint(0, self.n - l + 1)

                    # comprobar zona alrededor
                    libre = True
                    for x in range(max(0, i-1), min(self.n, i+2)):
                        for y in range(max(0, j-1), min(self.n, j+l+1)):
                            if self.tab[x][y] != 0:
                                libre = False

                else:
                    i = np.random.randint(0, self.n - l + 1)
                    j = np.random.randint(0, self.n)

                    # comprobar zona alrededor
                    libre = True
                    for x in range(max(0, i-1), min(self.n, i+l+1)):
                        for y in range(max(0, j-1), min(self.n, j+2)):
                            if self.tab[x][y] != 0:
                                libre = False

                if libre:
                    colocado = self.add_barco(l, (i, j), dirr)

                intentos += 1

            if not colocado:
                print(f"No se pudo colocar el barco de tamaño {l}")

        self.total_vidas = sum([self.status[i]["vidas"] for i in self.status.keys()])

    def tiro(self, i, j):
        if self.map[i, j] != 0:
            print("¡Ya disparaste aquí!")
            return

        if self.tab[i, j] == 1:
            self.historial.append((i,j))
            self.map[i, j] = 2
            self.total_vidas-=1
            return True
            print("¡Tocado!")

            # buscar barco tocado usando mapa auxiliar
            barco_id = self.coord_to_barco.get((i, j))
            if barco_id is not None:
                self.status[barco_id]["vidas"] -= 1
                #return False
                if self.status[barco_id]["vidas"] == 0:
                    print("¡Hundido!")
        else:
            self.map[i, j] = 1
            self.historial.append((i,j))
            print("Agua.")
            return False
        if self.total_vidas==0:
            self.ganador=False
