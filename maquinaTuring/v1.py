import time
import sys

# Definimos la máquina de Turing
class TuringMachine:
    def __init__(self, transitions, tape, start_state, accept_state, reject_state):
        self.transitions = transitions
        self.tape = list(tape) + ['B'] * 1000  # Llenamos con espacios en blanco (B)
        self.head = 0
        self.state = start_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.steps = []

    def step(self):
        # Guardamos la descripción instantánea
        self.steps.append(f"State: {self.state}, Tape: {''.join(self.tape)}, Head: {self.head}")

        # Obtenemos el símbolo actual bajo el cabezal
        current_symbol = self.tape[self.head]
        
        # Revisamos si hay una transición válida
        if (self.state, current_symbol) in self.transitions:
            next_state, write_symbol, move = self.transitions[(self.state, current_symbol)]
            self.tape[self.head] = write_symbol
            self.head += 1 if move == 'R' else -1
            self.state = next_state
        else:
            self.state = self.reject_state  # Si no hay transición, la máquina rechaza

    def run(self):
        while self.state not in [self.accept_state, self.reject_state]:
            self.step()
        self.steps.append(f"Final State: {self.state}, Tape: {''.join(self.tape)}, Head: {self.head}")
        return self.state == self.accept_state

# Definimos la tabla de transiciones basada en la imagen proporcionada
transitions = {
    ('q0', '0'): ('q1', 'X', 'R'),
    ('q1', '0'): ('q1', '0', 'R'),
    ('q1', '1'): ('q2', 'Y', 'L'),
    ('q1', 'Y'): ('q1', 'Y', 'R'),
    ('q2', '0'): ('q2', '0', 'L'),
    ('q2', 'X'): ('q0', 'X', 'R'),
    ('q2', 'Y'): ('q2', 'Y', 'L'),
    ('q3', 'Y'): ('q3', 'Y', 'R'),
    ('q3', 'B'): ('q4', 'B', 'R')
}

# Estados
start_state = 'q0'
accept_state = 'q4'
reject_state = 'reject'

def save_to_file(filename, steps):
    with open(filename, 'w') as f:
        for step in steps:
            f.write(step + '\n')

def animate(machine, delay=0.5):
    for step in machine.steps:
        sys.stdout.write("\033c")  # Limpia la pantalla
        print(step)
        time.sleep(delay)

if __name__ == "__main__":
    # Entrada del usuario
    user_input = input("Ingrese una cadena (máximo 1000 caracteres, solo 0s y 1s): ")
    if not user_input:
        user_input = '0011'  # Cadena por defecto

    # Validación de entrada
    if len(user_input) > 1000 or not all(c in '01' for c in user_input):
        print("Entrada inválida. Asegúrese de que la cadena tenga máximo 1000 caracteres y contenga solo 0s y 1s.")
        sys.exit(1)

    # Instancia de la máquina de Turing
    turing_machine = TuringMachine(transitions, user_input, start_state, accept_state, reject_state)

    # Ejecutamos la máquina
    accepted = turing_machine.run()

    # Guardamos la salida en un archivo
    save_to_file("turing_output.txt", turing_machine.steps)
    print(f"La máquina ha {'aceptado' if accepted else 'rechazado'} la cadena.")
    print("Las descripciones instantáneas se han guardado en 'turing_output.txt'.")

    # Animación para cadenas pequeñas
    if len(user_input) <= 10:
        animate(turing_machine)
