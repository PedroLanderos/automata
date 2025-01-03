import time
import random

class Automat:
    def __init__(self):
        self.stack = [] # pila del automata que almacena los estados
        self.currentState = "q0" # estado inicial
        self.descriptions = [] # lista para almacenar las descripciones instantaneas (IDs)

    # reinicia el automata de pila para cuando se procese una nueva cadena
    def Reset(self):
        self.stack = []
        self.currentState = "q0"
        self.descriptions = []

    def ProcessInput(self, input, animate=False):
        for symbol in input:
            if animate:
                self.DisplayState(symbol)

            self.descriptions.append(f"Estado: {self.currentState}, Pila: {' '.join(self.stack) if self.stack else '[Vacia]'}, Simbolo: {symbol}")

            if self.currentState == "q0":
                if symbol == "0":
                    self.stack.append("0")  
                elif symbol == "1" and self.stack:
                    self.stack.pop()       
                    self.currentState = "q1"
                else:
                    return False  
            elif self.currentState == "q1" and symbol == "1":
                if self.stack:
                    self.stack.pop()       
                else:
                    return False  
            else:
                return False

        if animate:
            self.DisplayState("END")

       
        self.descriptions.append(f"Estado final: {self.currentState}, Pila: {' '.join(self.stack) if self.stack else '[Vacia]'}, Simbolo: END")

        return self.currentState == "q1" and not self.stack

    def DisplayState(self, symbol):
        """Muestra el estado actual, la pila y el simbolo de entrada con animacion."""
        #print("\033[H\033[J", end="")  
        print(f"Procesando simbolo: {symbol}")
        print(f"Estado actual: {self.currentState}")
        print(f"Pila: {' '.join(self.stack) if self.stack else '[Vacia]'}")
        time.sleep(1)  

    def GenerateRandomString(self, length):
        if length % 2 != 0:
            length += 1 

        zeros = ["0"] * (length // 2)
        ones = ["1"] * (length // 2)
        combined = zeros + ones
        random.shuffle(combined)
        return "".join(combined)

    def SaveDescriptionsToFile(self, filename, is_valid):
        """Guarda las descripciones instantaneas (IDs) y el resultado de la evaluacion en un archivo."""
        with open(filename, "w") as file:
            for description in self.descriptions:
                file.write(description + "\n")
            if is_valid:
                file.write("\nLa cadena es valida y pertenece al lenguaje.\n")
            else:
                file.write("\nLa cadena no es valida y no pertenece al lenguaje.\n")


automat = Automat()

while True:
    print("\n--- Automata de pila ---")
    print("1. Ingresar cadena manualmente")
    print("2. Generar cadena aleatoria")
    print("3. Salir")
    
    choice = input("Elija una opcion: ")

    if choice == "1":
        user_input = input("Ingrese la cadena (0s y 1s): ")
        automat.Reset()
        animate = len(user_input) <= 10
        result = automat.ProcessInput(user_input, animate=animate)
        if result:
            print("La cadena es valida y pertenece al lenguaje.")
        else:
            print("La cadena no es valida y no pertenece al lenguaje.")
        automat.SaveDescriptionsToFile("descriptions.txt", result)
        print("Las descripciones instantaneas se han guardado en 'descriptions.txt'.")

    elif choice == "2":
        length = int(input("Ingrese la longitud de la cadena aleatoria (debe ser par): "))
        if length % 2 != 0:
            print("La longitud debe ser par. Se ajusta automaticamente.")
        random_string = automat.GenerateRandomString(length)
        print(f"Cadena generada: {random_string}")
        automat.Reset()
        animate = len(random_string) <= 10
        result = automat.ProcessInput(random_string, animate=animate)
        if result:
            print("La cadena generada es valida y pertenece al lenguaje.")
        else:
            print("La cadena generada no es valida y no pertenece al lenguaje.")
        automat.SaveDescriptionsToFile("descriptions.txt", result)
        print("Las descripciones instantaneas se han guardado en 'descriptions.txt'.")

    elif choice == "3":
        print("Saliendo del programa...")
        break

    else:
        print("Opcion no valida. Intente nuevamente.")