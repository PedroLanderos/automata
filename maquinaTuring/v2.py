import time

def turing_machine(input_string, max_length=1000):
    """
    Simula una máquina de Turing para verificar si una cadena de 0s seguida de 1s es aceptada.

    Parámetros:
    - input_string (str): La cadena de entrada compuesta por '0's y '1's.
    - max_length (int): Longitud máxima permitida para la cadena de entrada.

    Retorna:
    - None: Imprime el resultado de la simulación y guarda los pasos en un archivo.
    """

    # Verificar longitud de entrada
    if len(input_string) > max_length:
        raise ValueError(f"La cadena no puede exceder {max_length} caracteres.")

    # Verificación adicional para asegurarse de que solo contiene '0's y '1's
    if not set(input_string).issubset({'0', '1'}):
        raise ValueError("La cadena solo puede contener caracteres '0' y '1'.")

    # Tabla de transiciones basada en la especificación de la máquina
    transitions = {
        ('q0', '0'): ('q1', 'X', 'R'),
        ('q1', '0'): ('q1', '0', 'R'),
        ('q1', '1'): ('q2', 'Y', 'L'),
        ('q2', '0'): ('q2', '0', 'L'),
        ('q2', 'X'): ('q0', 'X', 'R'),
        ('q0', 'Y'): ('q3', 'Y', 'R'),
        ('q1', 'Y'): ('q1', 'Y', 'R'),
        ('q2', 'Y'): ('q2', 'Y', 'L'),
        ('q3', 'Y'): ('q3', 'Y', 'R'),
        ('q3', 'B'): ('q4', 'B', 'R'),  # Estado final de aceptación
    }

    # Inicialización de la cinta
    tape = list(input_string) + ['B'] * (max_length - len(input_string))  # 'B' representa blanco
    head = 0  # Posición inicial del cabezal
    state = 'q0'  # Estado inicial

    steps = []  # Lista para almacenar los pasos de la simulación

    # Simulación de la máquina de Turing
    try:
        while state != 'q4':  # 'q4' es el estado de aceptación
            current_symbol = tape[head]
            if (state, current_symbol) in transitions:
                new_state, write_symbol, direction = transitions[(state, current_symbol)]
                tape[head] = write_symbol
                # Registrar el paso actual con la posición del cabezal
                tape_snapshot = ''.join(tape).strip()
                steps.append(f"Estado: {state}, Cinta: {tape_snapshot}, Cabezal en: {head}")
                state = new_state
                # Mover el cabezal
                if direction == 'R':
                    head += 1
                elif direction == 'L':
                    head -= 1
                else:
                    raise ValueError(f"Dirección inválida: {direction}")

                # Verificar que el cabezal no se salga de los límites de la cinta
                if head < 0 or head >= len(tape):
                    raise RuntimeError("El cabezal se salió de los límites de la cinta.")
            else:
                # Si no hay transición definida para el par (estado, símbolo), rechazar la cadena
                raise RuntimeError(f"No se encontró transición para el par ({state}, {current_symbol}).")
    except RuntimeError as e:
        # Rechazo de la cadena
        steps.append(f"Rechazado: {e}")
        accepted = False
    else:
        # Aceptación de la cadena
        steps.append("Cadena aceptada.")
        accepted = True

    # Guardar las descripciones de los pasos en un archivo
    with open("turing_simulation.txt", "w") as file:
        for step in steps:
            file.write(step + "\n")

    # Mostrar animación de la simulación si la cadena es corta
    if len(input_string) <= 10:
        print("Animación de la máquina de Turing:")
        for step in steps:
            print(step)
            time.sleep(0.5)  # Pausa de 0.5 segundos entre pasos

    # Mostrar mensaje final de aceptación o rechazo
    if accepted:
        print("Resultado: La cadena pertenece al lenguaje (Aceptada).")
    else:
        print("Resultado: La cadena no pertenece al lenguaje (Rechazada).")

# Ejemplo de uso
if __name__ == "__main__":
    input_string = input("Introduce una cadena de 0s seguidos de 1s (ejemplo: 000111): ").strip()
    turing_machine(input_string)
