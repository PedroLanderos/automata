#include<iostream>
#include <string>
#include <random>
#include <cstdlib>
#include <ctime>

using namespace std;

string ReplaceA(string cadena, int *ifs);
string ReplaceS(string cadena, int *ifs);

string ReplaceS(string cadena, int *ifs)
{
    //encontrar de derecha a izquierda la primera S:
    int position = cadena.rfind('S');
    //decidir si la s se transforma
    
    int randomNumber = rand() % 2 + 1;
    if(randomNumber == 1 && *ifs > 0) // si si quiero que se transforme
    {
        //transformar la S por ictSA
        (*ifs)--;
        cadena.replace(position, 1, "iCtSA");
        if(ifs == 0) return cadena;
        cadena = ReplaceS(cadena, ifs); //llamo a la misma funcion
        cadena = ReplaceA(cadena, ifs);
    }
    else //remplazar la S por un ""
    {
        cadena.replace(position, 1, "");
    }
   
    return cadena;
}

string ReplaceA(string cadena, int *ifs)
{
    int position = cadena.find('A');
    //decidir si a se transforma
    int randomNumber = rand() % 2 + 1;
    if(randomNumber == 1 && *ifs > 0)//si a si se transforma
    {
        //encontrar la posicion de A 
        (*ifs)--;
        cadena.replace(position, 1, ";eictSA");
        if(ifs == 0) return cadena;
        //remplazar A por;eS
        //remplazar ;eS por ;eictSA
        //;eictS
        cadena = ReplaceA(cadena, ifs); //decidir nuevamente si la A se transforma
        cadena = ReplaceS(cadena, ifs);
    }
    else //si no quiero que se transforme, entonces la A debe ser remplazada por un " "
    {
        cadena.replace(position, 1, "E");
    }
    
    return cadena;
}

string Derivations(int numberOfIf)
{
    int limit = 1000;
    string cadena = "S";
    int position = 0;
    int randomNumber;

    while ((numberOfIf > 0))
    {
        cout<<"esta entrando en la sol: "<<numberOfIf<<endl;
        //significa que aun hay S en la cadena que procesar
        position = cadena.find('S');
        //si o si se remplaza
        cadena.replace(position, 1, "iCtSA");
        numberOfIf--;
        //ver si la A se remplaza o no 
        cadena = ReplaceA(cadena, &numberOfIf);
        //si no se remplaza la A simplemente se sigue remplazando la S 
    }

    cadena.replace(cadena.find('S'), 1, "");

    return cadena;
}



int main(int argc, char const *argv[])
{
    int ifs;
    cout<<"ingresar el numero de ifs: ";
    cin>>ifs;
    cout<<ifs<<endl;
    srand(time(0));
    string cadena = "";
    cadena = Derivations(ifs);
    cout<<cadena<<endl;

    return 0;
}