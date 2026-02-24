#https://www.cs.rit.edu/~jmg/courses/cs380/20051/slides/7-1-chomsky.pdf

#This will be the main file that when run does the comparison between the CFG to the CNF


from grammar import Grammar
from CGFToCNFConverter import CGFToCNFConverter

def main():

    test_string = """
    S -> aAB | BA
    A -> bA | ε
    B -> b | S | a
    """

    invalid_string = """
    S -> aA | B
    A -> b | ε
    B -> C
    """

    test_string2 = """
    S -> aA | B
    A -> b | ε
    B -> C
    C -> c
    """

    g = CGFToCNFConverter()

    #Invalid 
    success, message = g.parse(invalid_string)
    if not success:
        print(f"Error Not valid: {message}" "\n")
    else:
        g.convert()
        print(g)

    # valid 
    success, message = g.parse(test_string)
    if not success:
        print(f"Error: {message}")
    else:
        g.convert()
        print(g)
        is_valid = g.valid_cnf()
        print(f"Is valid results: {is_valid}")

if __name__ == "__main__":
    main()