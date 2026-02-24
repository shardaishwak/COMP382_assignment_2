# COMP 382 Assignment 2 
# Group 9 Topic 5
# Ishwak, Darius, Ryan, Brayden

CFG to CNF Converter is a Python program that converts Context-Free Grammars into Chomsky Normal Form. 

## Features implemented

- Epsilon Removal
- Unit Production Removal
- Terminal Normalization
- Binary Decomposition
- Validation

## Conversion Process

The program follows 4-steps:
1. _step_new_start: Create a new start symbol (S0).
2. _step_remove_epsilon: Eliminate empty productions and update rules.
3. _step_remove_unit: Replace unit rules (A -> B) with the actual contents of B.
4. _step_remove_form: Split long rules into binary form.

## Why bother converting?
# Simple Visual example
![CFG vs CNF Visual 1](cfg-cnf-visuals1.png)
![CFG vs CNF Visual 2](cfg-cnf-visuals2.png)

## Project Structure

```text
COMP382_assignment_2/
├── src/
│   ├── grammar.py            # Base Grammar class and parsing logic
│   ├── CGFToCNFConverter.py  # CNF conversion algorithm implementation
│   ├── main.py               # Main entry point with test cases
|
├── tests/
│   └── test_converter.py     # Unit tests for conversion steps
├── README.md                 
└── setup.sh                  
```

## Installation
1. Clone the repository. 
2. Ensure you have Python 3.x installed. 
3. Pytest for test cases (optional)

```bash
git clone https://github.com/your-repo/COMP382_assignment_2.git
cd COMP382_assignment_2
```

## Output
Before
```  
  S0 -> S
  A -> bA | ε
  B -> b | S | a
  S -> aAB | BA
```
Converted
```  
  S0 -> U_aX_1 | U_aB | BA | b | a
  A -> U_bA | b
  B -> b | U_aX_1 | U_aB | BA | a
  S -> U_aX_1 | U_aB | BA | b | a
  U_a -> a
  U_b -> b
  X_1 -> AB
```  

## Vlog Link
(add here when complete)



