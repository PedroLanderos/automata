#include <iostream>
#include <stack>
#include <fstream> // Para manejo de archivos
#include <string>

using namespace std;

int main(int argc, char const *argv[])
{
    //declarar el automata de pila
    stack<char> pila;

    //comparate the symbols '()' and '{}' and see if they are balanced

    //the 3 states of the PDA are going to be: empty, no empty and the final state
    //if the character is '(' or '{' then the program makes a push, if is a close symbol makes a top comparation and if the symbol is different its wrong

    string s;

    ifstream archivo("cadena.txt"); 
    if (!archivo.is_open()) {
        cout << "Error: No se pudo abrir el archivo." << endl;
        return 1;
    }

    getline(archivo, s);
    archivo.close(); 

    if (s.empty()) {
        cout << "cadena vacia." << endl;
        return 1;
    }

    for (char c : s)
    {
        if(c == '(' || c == '{')
            pila.push(c);
        else if(c == ')' || c == '}')
        {
            if(pila.empty())
            {
                cout<<"llaves desbalanceadas"<<endl;
                return;
            }
            char current = pila.top();
            pila.pop();
            if(current == '('){
                if(c !=  ')')
                {
                    cout<<"llaves desbalacedas"<<endl;
                    return;
                }
            }
            else if(current == '{')
            {
                if(c != '}')
                {
                    cout<<"llaves desbalanceadas"<<endl;
                    return;
                }
            }
        }
        else {
            cout<<"Caracter invalido"<<endl;
            return;
        }
    }
    cout<<"Llaves balancedas"<<endl;

    return 0;
}