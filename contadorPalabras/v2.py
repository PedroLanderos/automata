from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

class Automat:
    def __init__(self):
        #map que va a contener una lista de tuplas que van a contener los estados y los simbolos que van a generar una transicion 
        self.transitions = defaultdict(list) 
        self.startState = 'q0'
        #almacena los estados finales
        self.acceptStates = set() 
        #contador para el numero de estados
        self.stateCount = 0

    #agrega una transicion de un estado a otro
    def AddTransition(self, stateFrom, symbol, stateTo):
        self.transitions[stateFrom].append((symbol, stateTo))

    #define los estados finales que van a siginificar que una palabra fue encontrada
    def SetFinalStates(self, state):
        self.acceptStates.add(state)

    #si un simbolo se repite 2 veces en alguna de las transiciones entonces el automata no es determinsta 
    def IsDeterministic(self):
        for state, trans in self.transitions.items():
            visitedSymbols = set()
            for symbol, _ in trans:
                if symbol in visitedSymbols: 
                    return False
                visitedSymbols.add(symbol)
        return True
    
    #graficar el automata
    def plot(self):
        # Crear un grafo dirigido con NetworkX
        G = nx.DiGraph()

        # Agregar las transiciones como aristas al grafo
        for state, transitions in self.transitions.items():
            for symbol, next_state in transitions:
                G.add_edge(state, next_state, label=symbol)

        # Crear una disposición visual de los nodos (estados)
        pos = nx.spring_layout(G, seed=42)  # Usamos un 'seed' para reproducibilidad en el layout

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
        plt.show()
    


#construir el automata basado en las palabras
def BuildAutomat(words):
    #obtener todas las letras que serviran como valores para cambiar entre los estados
    automat = Automat()
    stateMapping = {'q0': automat.startState}
    currentState = 0

    for word in words:
        currentState = 'q0'
        for letter in word:
            nextState = f"q{automat.stateCount + 1}"
            automat.AddTransition(currentState, letter, nextState)
            currentState = nextState
            automat.stateCount += 1
        automat.SetFinalStates(currentState)

    if(automat.IsDeterministic()):
        print("is deterministic")
    else:
        print("is not deterministic") 

    automat.plot()
    return automat

words = ["abc", "acd"]
automat = BuildAutomat(words)