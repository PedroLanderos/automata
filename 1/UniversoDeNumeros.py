#landeros cortes pedro jonas practica 1 teoria de la computacion

import random
import time
import matplotlib.pyplot as plt
import math

#variables globales 
nsimbolos = [] #guarda el numero total de simbolos
ntotal = []
unos = [] #guarda todos los unos

def binarios(opcion):
    global nsimbolos, unos

    nsimbolos = []  #lista para guardar el numero total de simbolos de cada cadena
    unos = []       #lista para guardar el numero total de unos de cada cadena
    
    with open("UniversoCadenas.txt", "w", encoding="utf-8") as f:
        f.write('Σ^* = {' + 'ε' + ',\n')

        for i in range(1, opcion + 1):

            #se inicializan contadores para el numero total de simbolos y unos en la cadena actual
            contador_simbolos = 0
            contador_unos = 0

            #se generan todas las combinaciones binarias de longitud i
            for j in range(0, 2 ** i):
                #se convierte el numero j a una cadena binaria, se quita el prefijo '0b' y se rellena con ceros a la izquierda
                aux = bin(j)[2:].zfill(i)
                #se incrementa el contador de simbolos por la longitud de la cadena binaria generada
                contador_simbolos += len(aux)
                #se incrementa el contador de unos contando cuantos '1' hay en la cadena
                contador_unos += aux.count('1')
                
                f.write(aux + ", ")

            nsimbolos.append(contador_simbolos)
            unos.append(contador_unos)
            f.write("\n")

        f.write('}')

    print("fin")


def graficacion():
    plt.clf()
    puntosx = list(range(1, len(nsimbolos) + 1))
    
    #ambos simbolos
    plt.plot(puntosx, nsimbolos, color='r')
    plt.xlabel("Cadenas")
    plt.ylabel("Simbolos")
    plt.title("Cadenas vs simbolos")
    plt.grid(True)
    plt.show()
    
    #simplemente el 1
    plt.plot(puntosx, unos, color='b')
    plt.xlabel("Cadenas")
    plt.ylabel("Simbolos")
    plt.title("Cadenas vs unos")
    plt.grid(True)
    plt.show()

def main():
    while True:
        print("1. Modo manual")
        print("2. Modo aleatorio")
        print("3. Salir")
        
        try:
            opcion = int(input("Seleccionar opcion:"))
            if opcion == 1:
                n = int(input("Ingresar un valor para n (entre 1 y 1000): "))
                if 0 < n <= 1000:
                    start = time.time()
                    binarios(n)
                    graficacion()
                    end = time.time()
                    print(f"tiempo: {end - start:.2f} segundos.")
                else:
                    print("valor invalido")
                    
            elif opcion == 2:
                n = random.randint(1, 1000)
                print(f"numero generado: {n}")
                start = time.time()
                binarios(n)
                graficacion()
                end = time.time()
                print(f"tiempo: {end - start:.2f} segundos.")
                
            elif opcion == 3:
                print("programa finalizado")
                break
            else:
                print("opcion invalida")
            
            repetir = input("repetir el programa? (si/no): ").strip().lower()
            if repetir != 'si':
                print("fin")
                break
            
        except ValueError:
            print("entrada invalida")

if __name__ == "__main__":
    main()