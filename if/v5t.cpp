#include <iostream>
#include <string>
#include <vector>
using namespace std;

// Función para convertir la derivación en código IF real
string convertToIF(const string& derivation) {
    string result;
    vector<string> stack;
    for (size_t i = 0; i < derivation.size(); ++i) {
        if (derivation[i] == 'i' && i + 2 < derivation.size() && derivation[i + 1] == 'C' && derivation[i + 2] == 't') {
            result += "if (condition) {\n";
            stack.push_back("}"); // Agregamos un cierre al stack
            i += 2; // Avanzamos por 'iCt'
        } else if (derivation[i] == ';' && i + 1 < derivation.size() && derivation[i + 1] == 'e') {
            result += "else {\n";
            stack.push_back("}"); // Agregamos un cierre al stack
            i += 1; // Avanzamos por ';e'
        } else if (derivation[i] == 'A' || derivation[i] == 'S') {
            // Ignoramos estos símbolos gramaticales en el resultado final
        } else {
            result += "/* code */\n"; // Código genérico
        }
    }

    // Cerramos las estructuras abiertas
    while (!stack.empty()) {
        result += stack.back() + "\n";
        stack.pop_back();
    }

    return result;
}

// Función de derivación por DFS
void derive(string current, int depth, int targetDepth, vector<string>& results) {
    // Si alcanzamos la profundidad deseada, añadimos el resultado
    if (depth == targetDepth) {
        results.push_back(current);
        return;
    }

    // Expandimos la regla para S -> iCtSA
    string expanded = current;
    size_t pos = current.find("S");
    if (pos != string::npos) {
        expanded.replace(pos, 1, "iCtSA");
        derive(expanded, depth + 1, targetDepth, results);
    }

    // Expandimos la regla para A -> ;eS
    pos = current.find("A");
    if (pos != string::npos) {
        string alt1 = current;
        alt1.replace(pos, 1, ";eS");
        derive(alt1, depth, targetDepth, results);

        // Expandimos A -> epsilon
        string alt2 = current;
        alt2.replace(pos, 1, "");
        derive(alt2, depth, targetDepth, results);
    }
}

int main() {
    int targetDepth;
    cout << "Ingrese el número de condicionales IF que desea generar: ";
    cin >> targetDepth;

    // Inicializamos el proceso de derivación
    string startSymbol = "S";
    vector<string> results;

    derive(startSymbol, 0, targetDepth, results);

    // Mostramos las derivaciones generadas
    cout << "Derivaciones generadas:\n";
    for (const auto& result : results) {
        cout << result << endl;
        cout << "\nTraducción a IF:\n";
        cout << convertToIF(result) << endl;
    }

    return 0;
}
