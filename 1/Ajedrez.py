import random
from collections import deque
import tkinter as tk
from tkinter import messagebox, simpledialog

#se define el tablero para conocer todas las coordenadas y poder converir las fichas 
n = 5
tablero = [[(i * n + j + 1) for j in range(n)] for i in range(n)]

size = 100  #tamano de las celdas del tablero

#movimientos ortogonales y diagonales basados en la matriz del tablero
movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1),
               (-1, -1), (-1, 1), (1, -1), (1, 1)]

def posicion_valida(x, y):
    return 0 <= x < n and 0 <= y < n

#funcion bfs para encontrar la ruta mas optima/corta dada la posicion actual de la ficha
def bfs(inicio, meta):
    cola = deque([(inicio, [inicio])])  
    visitado = set([inicio])            

    while cola:
        posicion_actual, camino = cola.popleft()
        if posicion_actual == meta:
            return camino

        x_actual, y_actual = posicion_actual

        for movimiento in movimientos:
            nuevo_x, nuevo_y = x_actual + movimiento[0], y_actual + movimiento[1]
            if posicion_valida(nuevo_x, nuevo_y):
                nueva_posicion = (nuevo_x, nuevo_y)
                if nueva_posicion not in visitado:
                    visitado.add(nueva_posicion)
                    cola.append((nueva_posicion, camino + [nueva_posicion]))

    return None

#funcion que transforma las coordenadas a la casilla (por ejemplo las coordenadas 1,1 es la casilla 7 porque se basa en la matriz)
def coordenadas_a_casilla(coordenadas):
    x, y = coordenadas
    return tablero[x][y]

#funcion que guarda la ruta de cada ficha 
def guardar_ruta_en_txt(ruta, nombre_fichero):
    with open(nombre_fichero, 'w') as archivo:
        for posicion in ruta:
            casilla = coordenadas_a_casilla(posicion)
            archivo.write(f"Casilla {casilla} (posicion {posicion[0]+1},{posicion[1]+1})\n")

def avanzar_ficha(ficha, ruta, paso):
    if paso < len(ruta):
        return ruta[paso]
    return ficha #si la ficha gano ya no actualiza su posicion

#imprimir el tablero en consola
def imprimir_tablero(ficha_1, ficha_2):
    for i in range(n):
        fila = []
        for j in range(n):
            if (i, j) == ficha_1:
                fila.append("1")  #ficha 1
            elif (i, j) == ficha_2:
                fila.append("2")  #ficha 2
            else:
                fila.append(".")
        print(" ".join(fila))
    print("\n")

def imprimir_ruta_ficha(ficha_numero, ruta, turno_actual):
    print(f"ruta restante de la ficha {ficha_numero}:")
    for i in range(turno_actual, len(ruta)):
        posicion = ruta[i]
        casilla = coordenadas_a_casilla(posicion)
        print(f"casilla {casilla} (posicion {posicion[0]+1},{posicion[1]+1})")
    print("\n")

#funcion que actualiza el tablero grafico, recibe el tablero anterior y la tupla de la primera y la segunda ficha
def actualizar_tablero(canvas, ficha_1, ficha_2):
    canvas.delete("all")
    # Dibujar tablero tipo ajedrez
    for i in range(n):
        for j in range(n):
            color = "white" if (i + j) % 2 == 0 else "gray"
            canvas.create_rectangle(j * size, i * size, (j + 1) * size,
                                    (i + 1) * size, fill=color)

    #ciruclos que representan las fichas
    x1, y1 = ficha_1[1] * size + 10, ficha_1[0] * size + 10
    x2, y2 = ficha_2[1] * size + 10, ficha_2[0] * size + 10
    canvas.create_oval(x1, y1, x1 + size - 20, y1 + size -
                       20, fill="red") #la ficha 1 esta pintada de rojo y la 2 en azul
    canvas.create_oval(x2, y2, x2 + size - 20, y2 + size -
                       20, fill="blue")

#funcion para imrpimir la ruta/linea de razonamiento de la ficha usando circulos que representan las casillas y lineas que las unen
def dibujar_ruta(movimientos):
    root = tk.Tk()
    root.title("ruta de la ficha ganadora")

    canvas_width = 600
    canvas_height = 600
    margin = 50
    cell_size = (canvas_width - 2 * margin) / n

    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
    canvas.pack()

    for idx, pos in enumerate(movimientos):
        x, y = pos
        center_x = margin + (y + 0.5) * cell_size
        center_y = margin + (x + 0.5) * cell_size

        #ciruclos que represantan las casillas
        r = cell_size * 0.2
        canvas.create_oval(center_x - r, center_y - r, center_x +
                           r, center_y + r, fill='white', outline='black')

        casilla = coordenadas_a_casilla(pos)
        canvas.create_text(center_x, center_y, text=str(casilla))

        #flecha hacia la siguiente casilla
        if idx < len(movimientos) - 1:
            next_pos = movimientos[idx + 1]
            next_x, next_y = next_pos
            next_center_x = margin + (next_y + 0.5) * cell_size
            next_center_y = margin + (next_x + 0.5) * cell_size

            
            canvas.create_line(center_x, center_y,
                               next_center_x, next_center_y, arrow=tk.LAST)

    root.mainloop()

#logica que lleva a la busqueda de las fichas
def simulacion_fichas():
    ventana = tk.Tk()
    ventana.title("Simulación de Fichas")
    canvas = tk.Canvas(ventana, width=n * size, height=n * size)
    canvas.pack()

    # Función para seleccionar el modo de juego
    def seleccionar_modo():
        modo_window = tk.Toplevel()
        modo_window.title("Seleccione el modo de juego")

        modo_var = tk.StringVar() #modo que ha sido selccionado

        def set_manual():
            modo_var.set('manual')
            modo_window.destroy()

        def set_automatico():
            modo_var.set('automatico')
            modo_window.destroy()

        tk.Label(modo_window, text="Seleccionar el modo de juego:").pack(pady=10)
        tk.Button(modo_window, text="Manual", command=set_manual, width=20).pack(pady=5)
        tk.Button(modo_window, text="Automatico", command=set_automatico, width=20).pack(pady=5)

        modo_window.wait_window()

        return modo_var.get()

    modo = seleccionar_modo()

    #establecer las posiciones iniciales de cada ficha y los objetivos a los cuales deben ir
    ficha_1 = (0, 0)  #casilla 1
    ficha_2 = (0, 4)  #casilla 5 
    objetivo_1 = (4, 4)  #casilla 25 
    objetivo_2 = (4, 0)  #casilla 21 

    turno_ficha_1 = random.choice([True, False])
    print(f"Ficha {'1' if turno_ficha_1 else '2'} comienza primero.\n")

    #mostrar por primera vez el tablero grafico
    actualizar_tablero(canvas, ficha_1, ficha_2)

    #variables que almacenan el camino de las fichas para mostrar graficamente
    casillas_ficha_1 = [ficha_1]  
    casillas_ficha_2 = [ficha_2]  

    archivo_rutas = open("rutas_fichas.txt", "w")

    turno = 0

    def movimiento_aleatorio(ficha):
        #genera movimientos posibles (ortogonales y diagonales)
        movimientos_posibles = [
            (ficha[0] + dx, ficha[1] + dy)
            for dx, dy in movimientos
        ]

        #compara si el mov es valido, y si regresa hasta que lo sea
        movimientos_validos = [
            m for m in movimientos_posibles
            if posicion_valida(m[0], m[1]) and m != ficha_1 and m != ficha_2
        ]
        return random.choice(movimientos_validos) if movimientos_validos else ficha

    def guardar_rutas_en_archivo(ruta_1, ruta_2, turno):

        #guarda las rutas que van a seguir cada uno de los jugadores en el txt 
        ruta_1_str = " -> ".join([str(coordenadas_a_casilla(pos)) for pos in ruta_1])
        ruta_2_str = " -> ".join([str(coordenadas_a_casilla(pos)) for pos in ruta_2])
        archivo_rutas.write(f"Turno {turno}:\n")
        archivo_rutas.write(f"Ruta Ficha 1: {ruta_1_str}\n")
        archivo_rutas.write(f"Ruta Ficha 2: {ruta_2_str}\n\n")

    def obtener_movimiento_usuario(ficha_actual, otra_ficha):
        while True:
            casilla_str = simpledialog.askstring("Movimiento",
                                                 f"casilla a la que se quiere mover? (Actual: {coordenadas_a_casilla(ficha_actual)}):")
            if casilla_str is None:
                return ficha_actual
            try:
                casilla = int(casilla_str)
                x, y = None, None
                for i in range(n):
                    for j in range(n):
                        if tablero[i][j] == casilla:
                            x, y = i, j
                            break
                    if x is not None:
                        break
                if x is None:
                    messagebox.showerror("Error", "casilla invalida")
                    continue
                nueva_posicion = (x, y)

                #verifica si el movimiento es valido
                if nueva_posicion == ficha_actual:
                    messagebox.showerror("Error", "casilla invalida")
                    continue
                if not posicion_valida(x, y):
                    messagebox.showerror("Error", "casilla invalida")
                    continue
                dx = x - ficha_actual[0]
                dy = y - ficha_actual[1]
                if (dx, dy) not in movimientos:
                    messagebox.showerror("Error", "Movimiento inválido. casilla invalida")
                    continue
                # Verificar si la posición está ocupada por la otra ficha
                if nueva_posicion == otra_ficha:
                    messagebox.showerror("Error", "ccasilla invalida")
                    continue
                # Movimiento válido
                return nueva_posicion
            except ValueError:
                messagebox.showerror("Error", "casilla invalida")

    def ejecutar_turno():
        nonlocal ficha_1, ficha_2, turno_ficha_1, turno

        if ficha_1 == objetivo_1:
            print("ficha 1 ganadora")
            print("Ruta final de la ficha 1:")
            imprimir_ruta_ficha(1, casillas_ficha_1, 0)#imprime toda la ruta recorrida
            dibujar_ruta(casillas_ficha_1)
            archivo_rutas.close()  
            return
        if ficha_2 == objetivo_2:
            print("Ficha 2 ha llegado a la casilla 21. ¡Ganó!")
            print("Ruta final de la ficha 2:")
            imprimir_ruta_ficha(2, casillas_ficha_2, 0) #imprime toda la ruta recorrida
            dibujar_ruta(casillas_ficha_2)
            archivo_rutas.close() 
            return

        #recalcula la ruta mas optima para que la ficha la siga
        ruta_1 = bfs(ficha_1, objetivo_1)
        ruta_2 = bfs(ficha_2, objetivo_2)
        
        guardar_rutas_en_archivo(ruta_1, ruta_2, turno)

        if turno_ficha_1:
            if modo == 'manual':
                nueva_posicion = obtener_movimiento_usuario(ficha_1, ficha_2)
                ficha_1 = nueva_posicion
                casillas_ficha_1.append(ficha_1) 
                print(f"Ficha 1 avanza a la casilla {coordenadas_a_casilla(ficha_1)}.")
            else:
                #modo automatico
                if random.random() < 0.1: #valor que define la probabilidad de que la ficha ejecute un movimiento aleatorio o siga la ruta mas optima
                    nueva_posicion = avanzar_ficha(ficha_1, ruta_1, 1)
                    if nueva_posicion == ficha_2:
                        print(f"Ficha 1 cede el turno porque la ficha 2 está en la casilla {coordenadas_a_casilla(ficha_2)}.")
                    else:
                        ficha_1 = nueva_posicion
                        casillas_ficha_1.append(ficha_1)  
                        print(f"Ficha 1 avanza a la casilla {coordenadas_a_casilla(ficha_1)}.")
                else:
                    ficha_1 = movimiento_aleatorio(ficha_1)
                    casillas_ficha_1.append(ficha_1)
                    print(f"Ficha 1 se mueve aleatoriamente a la casilla {coordenadas_a_casilla(ficha_1)}.")
        else:
            if modo == 'manual':
                nueva_posicion = obtener_movimiento_usuario(ficha_2, ficha_1)
                ficha_2 = nueva_posicion
                casillas_ficha_2.append(ficha_2)  
                print(f"Ficha 2 avanza a la casilla {coordenadas_a_casilla(ficha_2)}.")
            else:
                if random.random() < 0.1: 
                    nueva_posicion = avanzar_ficha(ficha_2, ruta_2, 1)
                    if nueva_posicion == ficha_1:
                        print(f"Ficha 2 cede el turno porque la ficha 1 está en la casilla {coordenadas_a_casilla(ficha_1)}.")
                    else:
                        ficha_2 = nueva_posicion
                        casillas_ficha_2.append(ficha_2) 
                        print(f"Ficha 2 avanza a la casilla {coordenadas_a_casilla(ficha_2)}.")
                else:
                    ficha_2 = movimiento_aleatorio(ficha_2)
                    casillas_ficha_2.append(ficha_2)
                    print(f"Ficha 2 se mueve aleatoriamente a la casilla {coordenadas_a_casilla(ficha_2)}.")

        turno_ficha_1 = not turno_ficha_1
        turno += 1

        actualizar_tablero(canvas, ficha_1, ficha_2)

        ventana.after(1000, ejecutar_turno)

    ventana.after(1000, ejecutar_turno)

    ventana.mainloop()

#ejecutar la funcion que contiene la simulacion/animacion
simulacion_fichas()