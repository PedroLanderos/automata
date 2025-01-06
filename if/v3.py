import random

def Derivations(numberOfIf):
    limit = 1000
    cola = []
    #el simbolo inicia con S para hacer la derivacion de los if
    string = "S"
    while numberOfIf > 0:
        #el currentsymbol ahora es S, por lo que se tiene que derivar:
        string = string.replace("S", "iCtSA", 1)    
        numberOfIf -= 1
        #para elegir de manera aleatoria si el A representa un ;eS (else) o un epsilon (vacio)
        
        if random.choice([True, False]):
            string = string.replace("A", ";eS", 1)
            aux = ";eS"
            #;eS
            while "S" in aux:
                aux = aux.replace("S", "iCtSA", 1)
                #;eiCtSA y puede ser: ;eiCtS o ;eiCt;eS pero eso significa que pueden haber if dentro de los else if
                if random.choice([True, False]):
                    aux = aux.replace("S", "iCtSA", 1)
                    #;eiCtict


#se puede hacer una funcion recursiva para ver si se van a construir mas if else o solo if dentro de los if else 
           

    #encontrar todos los S sobrantes para eliminarlos de la cadena
    string = string.replace("S", "").replace("A", "")

    return string


v = Derivations(3)
print(v)