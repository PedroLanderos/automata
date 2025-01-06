import random
import re

# Definición de la gramática en formato BNF
GRAMMAR = {
    'S': ['iCtSA'],
    'A': [';eS', '']
}

# Función para contar el número de 'IF's en una cadena
def count_IFs(string):
    # Asumimos que cada 'iCtS' representa un IF
    return len(re.findall(r'iCtS', string))

# Función para generar la derivación
def derive_grammar(desired_IFs, max_derivations=1000, seed=None):
    if seed is not None:
        random.seed(seed)  # Para reproducibilidad en pruebas

    derivation_steps = []
    current_string = 'S'
    derivation_steps.append(current_string)
    derivations = 0
    current_IFs = 0

    while current_IFs < desired_IFs and derivations < max_derivations:
        # Buscar los símbolos no terminales en la cadena actual
        non_terminals = [m.start() for m in re.finditer(r'[SA]', current_string)]
        if not non_terminals:
            break  # No hay más símbolos para expandir

        # Seleccionar aleatoriamente uno de los símbolos no terminales
        pos = random.choice(non_terminals)
        symbol = current_string[pos]

        # Seleccionar aleatoriamente una producción para el símbolo
        production = random.choice(GRAMMAR[symbol])

        # Reemplazar el símbolo en la posición seleccionada
        new_string = current_string[:pos] + production + current_string[pos+1:]

        # Registrar el paso
        derivation_steps.append(new_string)
        derivations += 1

        # Actualizar el contador de IFs
        current_IFs = count_IFs(new_string)

        # Actualizar la cadena actual
        current_string = new_string

    return derivation_steps, current_string, derivations, current_IFs

# Función para convertir la cadena derivada en pseudocódigo
def generate_pseudocode(derived_string):
    # Esta función puede ser personalizada según cómo se desee interpretar la cadena
    # Por simplicidad, vamos a reemplazar las producciones con pseudocódigo básico
    pseudocode = derived_string
    pseudocode = pseudocode.replace('i', 'if ')
    pseudocode = pseudocode.replace('C', 'condition')
    pseudocode = pseudocode.replace('t', 'then')
    pseudocode = pseudocode.replace('S', 'statement')
    pseudocode = pseudocode.replace('A', '')
    pseudocode = pseudocode.replace(';', ' else ')
    pseudocode = pseudocode.replace('e', 'end if')
    # Eliminar espacios innecesarios
    pseudocode = re.sub(r'\s+', ' ', pseudocode).strip()
    return pseudocode

# Función principal
def main():
    import argparse

    parser = argparse.ArgumentParser(description='Derivar gramática BNF para condicional IF.')
    parser.add_argument('-n', '--number', type=int, help='Número deseado de IFs a generar', required=True)
    parser.add_argument('-o1', '--output_steps', type=str, help='Archivo para registrar los pasos de derivación', default='derivations.txt')
    parser.add_argument('-o2', '--output_pseudocode', type=str, help='Archivo para el pseudocódigo generado', default='pseudocode.txt')
    parser.add_argument('--seed', type=int, help='Semilla para la generación aleatoria', default=None)
    args = parser.parse_args()

    desired_IFs = args.number
    output_steps = args.output_steps
    output_pseudocode = args.output_pseudocode
    seed = args.seed

    derivation_steps, final_string, total_derivations, final_IFs = derive_grammar(desired_IFs, seed=seed)

    # Escribir los pasos de derivación en el archivo correspondiente
    with open(output_steps, 'w') as f_steps:
        for step_num, step in enumerate(derivation_steps):
            f_steps.write(f"Paso {step_num}: {step}\n")

    # Generar el pseudocódigo y escribirlo en el otro archivo
    pseudocode = generate_pseudocode(final_string)
    with open(output_pseudocode, 'w') as f_pseudo:
        f_pseudo.write(pseudocode + '\n')

    # Informar al usuario sobre el resultado
    print(f"Derivación completada.")
    print(f"Total de derivaciones realizadas: {total_derivations}")
    print(f"Total de IFs generados: {final_IFs}")
    print(f"Pasos de derivación registrados en: {output_steps}")
    print(f"Pseudocódigo generado en: {output_pseudocode}")

if __name__ == "__main__":
    main()
