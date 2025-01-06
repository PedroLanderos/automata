import random

def Derivations(numberOfIf):
    limit = 1000
    #el simbolo inicia con S para hacer la derivacion de los if
    string = "S"

    while numberOfIf > 0:
        #el currentsymbol ahora es S, por lo que se tiene que derivar:
        string = string.replace("S", "iCtSA", 1) 
        numberOfIf -= 1
        #para elegir de manera aleatoria si el A representa un ;eS (else) o un epsilon (vacio)
        if random.choice([True, False]):
            string = string.replace("A", ";eS", 1)
            if numberOfIf > 0:
                string_parts = string.rsplit("S", 1)
                string = "iCtSA".join(string_parts)
                numberOfIf -= 1
        else:
            string = string.replace("A", "", 1)

    #encontrar todos los S sobrantes para eliminarlos de la cadena
    string = string.replace("S", "").replace("A", "")

    return string

def InsertAtPosition(string, position, value):
    return string[:position] + value + string[position:]

def GeneratePseudoCode(string):
    pseudocode = ""
    indentLevel = 0

    for symbol in string:
        if symbol == "i":
            pseudocode += "    " * indentLevel + "if"
        elif symbol == "C":
            pseudocode += " (condition):\n"
            indentLevel += 1
        elif symbol == "t":
            pseudocode += "    " * indentLevel + "//code\n"
        elif symbol == ";":
            pseudocode += "\n"
        elif symbol == "e":
            indentLevel -= 1
            pseudocode += "    " * indentLevel + "else:\n"

    # Remove extra blank lines caused by misplaced `;` or `else`
    pseudocode_lines = pseudocode.splitlines()
    cleaned_lines = []
    for i, line in enumerate(pseudocode_lines):
        if line.strip() == "else:" and (i + 1 >= len(pseudocode_lines) or pseudocode_lines[i + 1].strip() == ""):
            continue
        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)

numberOfIf = int(input("Ingresa el numero de ifs: "))

derivations = Derivations(numberOfIf)
print(derivations)


