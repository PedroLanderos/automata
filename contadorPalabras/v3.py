from collections import defaultdict, deque
import networkx as nx
import matplotlib.pyplot as plt
import re

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
        G = nx.DiGraph()
        for state, transitions in self.transitions.items():
            for symbol, next_state in transitions:
                if next_state != "-":
                    G.add_edge(state, next_state, label=symbol)
        pos = nx.kamada_kawai_layout(G)
        plt.figure(figsize=(12, 12))
        nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=10, font_weight="bold")
        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        nx.draw_networkx_nodes(G, pos, nodelist=[self.startState], node_color="green", node_size=3000)
        nx.draw_networkx_nodes(G, pos, nodelist=list(self.acceptStates), node_color="red", node_size=3000)
        plt.title("Automata Visualization")
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        plt.show()

    def to_deterministic(self):
        if self.IsDeterministic():
            print("El autómata ya es determinista.")
            return self
        symbols = set()
        for trans in self.transitions.values():
            for symbol, _ in trans:
                symbols.add(symbol)
        symbols = sorted(symbols)
        dfa = Automat()
        dfa.startState = self.startState
        dfa.transitions = defaultdict(list)
        state_mapping = {}
        queue = deque()
        start_set = frozenset([self.startState])
        state_mapping[start_set] = self.startState
        queue.append(start_set)
        if any(state in self.acceptStates for state in start_set):
            dfa.SetFinalStates(state_mapping[start_set])
        while queue:
            current_set = queue.popleft()
            current_state_name = state_mapping[current_set]
            for symbol in symbols:
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
                        next_state_name = ''.join(sorted(next_set))
                        state_mapping[next_set] = next_state_name
                        queue.append(next_set)
                        if any(state in self.acceptStates for state in next_set):
                            dfa.SetFinalStates(next_state_name)
                    else:
                        next_state_name = state_mapping[next_set]
                dfa.AddTransition(current_state_name, symbol, next_state_name)
        print("El autómata ha sido convertido a determinista.")
        return dfa

    def minimize(self):
        if not self.IsDeterministic():
            print("El autómata debe ser determinista para minimizar.")
            return self
        partition = [self.acceptStates, set(self.transitions.keys()) - self.acceptStates]
        for p in partition:
            p.discard("-")
        symbols = set()
        for trans in self.transitions.values():
            for symbol, _ in trans:
                symbols.add(symbol)
        step = 1
        while True:
            new_partition = []
            for group in partition:
                splitter = defaultdict(set)
                for state in group:
                    key = tuple(
                        next((i for i, p in enumerate(partition) if any(dest in p for dest in [t[1] for t in self.transitions[state] if t[0] == symbol])), -1)
                        for symbol in sorted(symbols)
                    )
                    splitter[key].add(state)
                new_partition.extend(splitter.values())
            if new_partition == partition:
                break
            partition = new_partition
            step += 1
        state_to_group = {}
        for i, group in enumerate(partition):
            for state in group:
                state_to_group[state] = i
        minimized_dfa = Automat()
        group_names = {i: f"Q{i}" for i in range(len(partition))}
        minimized_dfa.startState = group_names[state_to_group[self.startState]]
        minimized_dfa.transitions = defaultdict(list)
        for group_index, group in enumerate(partition):
            if any(state in self.acceptStates for state in group):
                minimized_dfa.SetFinalStates(group_names[group_index])
        for group_index, group in enumerate(partition):
            representative = next(iter(group))
            for symbol, dest in self.transitions[representative]:
                if dest == "-":
                    dest_group = "-"
                else:
                    dest_group = group_names[state_to_group[dest]]
                minimized_dfa.AddTransition(group_names[group_index], symbol, dest_group)
        print("El autómata ha sido minimizado.")
        return minimized_dfa

    def to_string(self):
        print("Estados:", list(self.transitions.keys()))
        print("Estado inicial:", self.startState)
        print("Estados finales:", list(self.acceptStates))
        print("Transiciones:")
        for state, trans in self.transitions.items():
            for symbol, next_state in trans:
                print(f"  {state} --{symbol}--> {next_state}")

# Construir el autómata basado en las palabras
def BuildAutomat(words):
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

def search_words_in_text(automat, filename, history_filename):
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
    words = re.findall(r'\b\w+\b', text.lower())
    results = defaultdict(list)
    with open(history_filename, 'w', encoding='utf-8') as history_file:
        for index, word in enumerate(words):
            current_state = automat.startState
            valid = True
            history_file.write(f"Procesando palabra: '{word}'\n")
            for letter in word:
                transitions = [t for t in automat.transitions[current_state] if t[0] == letter]
                if transitions:
                    next_state = transitions[0][1]
                    history_file.write(f"  Estado actual: {current_state}, Símbolo: '{letter}', Próximo estado: {next_state}\n")
                    current_state = next_state
                else:
                    valid = False
                    history_file.write(f"  Estado actual: {current_state}, Símbolo: '{letter}', No hay transición válida\n")
                    break
            if valid and current_state in automat.acceptStates:
                results[word].append(index)
                history_file.write(f"  Palabra '{word}' aceptada en el estado final: {current_state}\n")
            else:
                history_file.write(f"  Palabra '{word}' rechazada.\n")
            history_file.write("\n")
    word_counts = {word: len(positions) for word, positions in results.items()}
    return word_counts, results

# Lista de palabras para construir el autómata
words = ["abc", "acd"]
nfa = BuildAutomat(words)

# Convertir el NFA a DFA
dfa = nfa.to_deterministic()
print("Autómata Determinista (DFA):")
dfa.plot()

# Reducir el DFA
min_dfa = dfa.minimize()
print("Autómata Minimizado:")
min_dfa.plot()

# Buscar palabras en un archivo de texto
filename = 'texto.txt'  # Reemplaza con el nombre de tu archivo
history_filename = 'historial.txt'
word_counts, word_positions = search_words_in_text(min_dfa, filename, history_filename)

print("\nConteo total de palabras:")
for word, count in word_counts.items():
    print(f"'{word}': {count}")
