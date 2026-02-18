#https://www.cs.rit.edu/~jmg/courses/cs380/20051/slides/7-1-chomsky.pdf

#This will be the main file that when run does the comparison between the CFG to the CNF


from grammar import Grammar
from CGFToCNFConverter import CGFToCNFConverter

def main():

    test_string = """
    S -> aBa
    B -> b | ε
    """
    g = CGFToCNFConverter()

    g.parse(test_string)

    g.convert()

    print(g)

    is_valid = g.valid_cnf()
    print(f"Is valid results {is_valid}")

if __name__ == "__main__":
    main()