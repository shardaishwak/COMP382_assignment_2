#https://www.cs.rit.edu/~jmg/courses/cs380/20051/slides/7-1-chomsky.pdf

#This will be the main file that when run does the comparison between the CFG to the CNF


from pyscript import window
from grammar import Grammar
from CGFToCNFConverter import CGFToCNFConverter

def convertCGFToCNF(input_string):

    try:
        g = CGFToCNFConverter()
        g.parse(input_string)
        g.convert()
        is_valid = g.valid_cnf()
        return g
    except Exception as e:
        return "Invalid Grammar"

window.convertCGFToCNF = convertCGFToCNF