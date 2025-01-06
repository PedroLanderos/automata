import random
import os

class IFGrammar:
    def __init__(self):
        # Inicializamos los parámetros de la clase
        self.derivations = []  # Para almacenar cada derivación
        self.steps = []  # Para almacenar cada paso de las derivaciones
    
    def generate_condition(self):
        # Genera una condición aleatoria simple (puede ser más compleja si lo deseas)
        return f"Condition_{random.randint(1, 100)}"
    
    def generate_code_block(self):
        # Genera un bloque de código aleatorio representado por "S"
        return f"Code_Block_{random.randint(1, 100)}"
    
    def generate_derivation_step(self, current_derivation):
        # Genera el siguiente paso de la derivación
        new_derivation = ""
        if 'S' in current_derivation:
            # Reemplazamos S con la producción "iCtSA"
            new_derivation = current_derivation.replace('S', f"i {self.generate_condition()} t {self.generate_code_block()} A")
        if 'A' in new_derivation:
            # Reemplazamos A con la producción ";eS" o ε
            if random.choice([True, False]):
                new_derivation = new_derivation.replace('A', f"; e {self.generate_code_block()} S")
            else:
                new_derivation = new_derivation.replace('A', "ε")
        return new_derivation
    
    def derive(self, num_derivations=1, max_steps=1000):
        # Iniciamos la derivación desde S
        current_derivation = "S"
        self.derivations.append(current_derivation)
        self.steps.append(current_derivation)
        
        step_count = 0
        while step_count < max_steps and len(self.derivations) < num_derivations:
            step_count += 1
            current_derivation = self.generate_derivation_step(current_derivation)
            self.derivations.append(current_derivation)
            self.steps.append(current_derivation)
        
        return self.derivations
    
    def save_to_file(self, filename, content):
        # Guarda el contenido en un archivo usando codificación 'utf-8'
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
    
    def generate_pseudocode(self, derivation):
        # Genera el pseudocódigo correspondiente a la derivación
        pseudocode = ""
        for part in derivation.split(" "):
            if part.startswith("Condition"):
                pseudocode += f"if {part}:\n"
                pseudocode += "    # Execute code block\n"
            elif part.startswith("Code_Block"):
                pseudocode += f"    # {part}\n"
            elif part == ";":
                pseudocode += "else:\n"
            elif part == "e":
                pseudocode += "    # Execute else block\n"
        return pseudocode

# Función principal
def main():
    # Crear una instancia de la clase IFGrammar
    grammar = IFGrammar()

    # Generar las derivaciones aleatorias
    num_derivations = int(input("Ingrese el número de derivaciones (hasta 1000): "))
    derivations = grammar.derive(num_derivations=num_derivations)

    # Guardar las derivaciones en un archivo
    derivation_file = "derivations.txt"
    grammar.save_to_file(derivation_file, "\n".join(grammar.steps))

    # Generar el pseudocódigo para las derivaciones
    pseudocode = "\n\n".join([grammar.generate_pseudocode(derivation) for derivation in derivations])

    # Guardar el pseudocódigo en otro archivo
    pseudocode_file = "pseudocode.txt"
    grammar.save_to_file(pseudocode_file, pseudocode)

    print(f"Las derivaciones y el pseudocódigo se han guardado en '{derivation_file}' y '{pseudocode_file}'.")

# Ejecutar el programa
if __name__ == "__main__":
    main()
