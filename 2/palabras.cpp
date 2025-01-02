#include <iostream>
#include <fstream>
#include <string>
#include <unordered_map>
#include <vector>

using namespace std;

unordered_map<int, unordered_map<char, int>> CreateAutomata(string palabra)
{
    unordered_map<int, unordered_map<char, int>> grafo;
    int estadoAct = 0;

    for(char c : palabra)
    {
        grafo[estadoAct][tolower(c)] = estadoAct + 1;
        estadoAct++;
    }

    return grafo;
}

bool Automata()
{
    
}



int main(int argc, char const *argv[])
{
    
    return 0;
}
