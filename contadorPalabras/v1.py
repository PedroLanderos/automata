from collections import defaultdict, deque
import networkx as nx
import matplotlib.pyplot as plt

class Automat:
    def __init__(self):
        self.transitions = defaultdict(list)
        self.startState = 'q0'
        self.acceptStates = set()
        self.stateCount = 0

    def AddTransition(self, stateFrom, symbol, stateTo):
        self.transitions[stateFrom].append((symbol, stateTo))

    def SetFinalStates(self, state):
        self.acceptStates.add(state)

    def IsDeterministic(self):
        for state, trans in self.transitions.items():
            visitedSymbols = set()
            for symbol, _ in trans:
                if symbol in visitedSymbols:
                    return False
                visitedSymbols.add(symbol)
        return True

    def plot(self):
        # Crear un grafo dirigido con NetworkX
        G = nx.DiGraph()

        # Agregar las transiciones como aristas al grafo, excluyendo las que llevan a "-"
        for state, transitions in self.transitions.items():
            for symbol, next_state in transitions:
                if next_state != "-":  # Excluir transiciones al estado "-"
                    G.add_edge(state, next_state, label=symbol)

        # Crear una disposición visual de los nodos (estados)
        pos = nx.kamada_kawai_layout(G)  # Usamos un 'kamada_kawai_layout' para mejor disposición

        # Asegurarse de que la figura se ajusta al tamaño necesario
        plt.figure(figsize=(12, 12))  # Ajustar el tamaño de la ventana

        # Dibujar los nodos y las aristas
        nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=10, font_weight="bold")
        
        # Etiquetas de las aristas (símbolos)
        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        # Resaltar el estado inicial (en verde)
        nx.draw_networkx_nodes(G, pos, nodelist=[self.startState], node_color="green", node_size=3000)

        # Resaltar los estados finales (en rojo)
        nx.draw_networkx_nodes(G, pos, nodelist=list(self.acceptStates), node_color="red", node_size=3000)

        # Título del grafo
        plt.title("Automata Visualization")
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)  # Ajustar los márgenes de la ventana
        plt.show()

    def to_deterministic(self):
        if self.IsDeterministic():
            print("El autómata ya es determinista.")
            return self  # Ya es determinista

        # Obtener todos los símbolos de entrada
        symbols = set()
        for trans in self.transitions.values():
            for symbol, _ in trans:
                symbols.add(symbol)
        symbols = sorted(symbols)  # Ordenar para consistencia

        # Inicializar el DFA
        dfa = Automat()
        dfa.startState = self.startState
        dfa.transitions = defaultdict(list)

        # Mapeo de conjuntos de estados a nombres de estados en el DFA
        state_mapping = {}
        # Usaremos una cola para procesar los conjuntos de estados
        queue = deque()

        # Estado inicial del DFA es el conjunto que contiene el estado inicial del NFA
        start_set = frozenset([self.startState])
        state_mapping[start_set] = self.startState
        queue.append(start_set)

        # Determinar si el estado inicial es de aceptación
        if any(state in self.acceptStates for state in start_set):
            dfa.SetFinalStates(state_mapping[start_set])

        while queue:
            current_set = queue.popleft()
            current_state_name = state_mapping[current_set]

            for symbol in symbols:
                # Obtener el conjunto de estados al que se llega con el símbolo
                next_set = set()
                for state in current_set:
                    for trans_symbol, next_state in self.transitions[state]:
                        if trans_symbol == symbol:
                            next_set.add(next_state)
                next_set = frozenset(next_set)

                if not next_set:
                    next_state_name = "-"
                else:
                    if next_set not in state_mapping:
                        # Asignar un nombre al nuevo conjunto de estados
                        next_state_name = ''.join(sorted(next_set))
                        state_mapping[next_set] = next_state_name
                        queue.append(next_set)

                        # Determinar si este nuevo estado es de aceptación
                        if any(state in self.acceptStates for state in next_set):
                            dfa.SetFinalStates(next_state_name)
                    else:
                        next_state_name = state_mapping[next_set]

                # Agregar la transición al DFA
                dfa.AddTransition(current_state_name, symbol, next_state_name)

        print("El autómata ha sido convertido a determinista.")
        return dfa


# Construir el autómata basado en las palabras
def BuildAutomat(words):
    # Obtener todas las letras que servirán como valores para cambiar entre los estados
    automat = Automat()
    currentState = 'q0'

    for word in words:
        currentState = 'q0'
        for letter in word:
            nextState = f"q{automat.stateCount + 1}"
            automat.AddTransition(currentState, letter, nextState)
            currentState = nextState
            automat.stateCount += 1
        automat.SetFinalStates(currentState)

    automat.plot()

    if automat.IsDeterministic():
        print("El autómata es determinista.")
    else:
        print("El autómata no es determinista.")
    return automat


# Lista de palabras para construir el NFA
words = ["acoso", "acecho", "agresion", "victima", "violacion", "machista"]
nfa = BuildAutomat(words)

# Convertir el NFA a DFA
dfa = nfa.to_deterministic()

print("Autómata Determinista (DFA):")
dfa.plot()
