import random

def Derivations(numberOfIf, limit=1000):
    """
    Derives a grammar for a given number of IF statements.
    """
    string = "S"  # Initial symbol
    derivation_steps = []  # To store derivation steps
    count_if = 0  # Counter for IF statements

    while "S" in string and count_if < numberOfIf and limit > 0:
        # Derive S -> iCtSA or eliminate S if max IF count is reached
        if count_if >= numberOfIf:
            string = string.replace("S", "", 1)
        else:
            string = string.replace("S", "iCtSA", 1)
            count_if += 1

        # Derive A -> ;eS or A -> epsilon
        string = string.replace("A", ";eS", 1)
        if(count_if <= numberOfIf):
            string_parts = string.rsplit("S", 1)
            string = "iCtSA".join(string_parts)
            count_if += 1

        derivation_steps.append(string)
        limit -= 1
        print(string)

    # Replace remaining S or A with epsilon
    string = string.replace("S", "").replace("A", "")
    derivation_steps.append(string)
    return derivation_steps, string


def InsertAtPosition(string, position, value):
    """
    Inserts a value into a string at a specific position.
    """
    return string[:position] + value + string[position:]


def GeneratePseudoCode(derived_string):
    """
    Converts a derived grammar string into pseudocode.
    """
    pseudocode = ""
    indent_level = 0
    last_position = 0

    for symbol in derived_string:
        if symbol == "i":
            pseudocode += " " * indent_level + "if"
            last_position = len(pseudocode)
        elif symbol == "C":
            pseudocode = InsertAtPosition(pseudocode, last_position, " (condition){\n")
            indent_level += 4  # Increase indentation for nested blocks
            last_position = len(pseudocode)
        elif symbol == "t":
            pseudocode += " " * indent_level + "//codigo\n"
            last_position = len(pseudocode)
        elif symbol == ";":
            indent_level -= 4  # Close the current block
            pseudocode += " " * indent_level + "} else if (condition) {\n"
            indent_level += 4  # Add new block for "else if"
        elif symbol == "e":
            indent_level -= 4  # Close the "else if" block
            pseudocode += " " * indent_level + "}\n"

    # Close any remaining open blocks
    while indent_level > 0:
        indent_level -= 4
        pseudocode += " " * indent_level + "}\n"

    return pseudocode


def save_to_file(filename, content):
    """
    Saves content to a file.
    """
    with open(filename, "w") as file:
        file.write(content)


if __name__ == "__main__":
    max_if = int(input("Enter the maximum number of IF statements: "))

    # Generate derivations
    steps, final_string = Derivations(max_if)

    print(final_string)

    # Convert to pseudocode
    pseudocode = GeneratePseudoCode(final_string)

    # Save outputs
    save_to_file("derivations.txt", "\n".join(steps))
    save_to_file("pseudocode.txt", pseudocode)

    print("Derivations and pseudocode have been saved to 'derivations.txt' and 'pseudocode.txt'.")
