class AutomataDePila:
    def __init__(self):
        self.pila = []

    def revisar_balanceo(self, cadena):
        for i, caracter in enumerate(cadena):
            if caracter in "({":
                # Empujar paréntesis o llave de apertura a la pila
                self.pila.append(caracter)
            elif caracter in ")}":
                # Verificar si la pila está vacía o el tope no coincide
                if not self.pila:
                    return f"Error: Cierre inesperado '{caracter}' en posición {i}."
                tope = self.pila.pop()
                if (caracter == ")" and tope != "(") or (caracter == "}" and tope != "{"):
                    return f"Error: Mismatch entre '{tope}' y '{caracter}' en posición {i}."
            else:
                # Si hay un carácter no válido
                return f"Error: Carácter no válido '{caracter}' en posición {i}."
        
        # Verificar si la pila no está vacía al final
        if self.pila:
            faltantes = {}
            for simbolo in self.pila:
                faltantes[simbolo] = faltantes.get(simbolo, 0) + 1
            return f"Error: Faltan cierres para los siguientes símbolos: {faltantes}."
        
        return "La cadena está balanceada."


# Ejemplo de uso
if __name__ == "__main__":
    # Define el string aquí
    cadena = "{()))()}"
    print(f"Revisando la cadena: {cadena}")
    
    automata = AutomataDePila()
    resultado = automata.revisar_balanceo(cadena)
    print(resultado)
