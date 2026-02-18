from grammar import Grammar
from itertools import combinations
class CGFToCNFConverter(Grammar):
    def convert(self):
        # Call step 1
        self._step_new_start()
        print(self)
        print()
        # Call step 2
        self._step_remove_epsilon()
        print(self)
        print()
        # Call step 3
        self._step_remove_unit()
        print(self)
        print()
        # Call step 4
        self._step_remove_form()
        print(self)
        print()
        return self

    # Step 0: Add new start variable S0 -> S
    def _step_new_start(self):
        old_start = self.start_symbol
        new_start = old_start + "0"
        while new_start in self.non_terminals:
            # Handle the case where a variable was already called S0(')*
            new_start += "'"

        self.non_terminals.add(new_start)
        self.productions[new_start] = [[old_start]]
        self.start_symbol = new_start

    # Step 2: Remove epsilon rule
    def _step_remove_epsilon(self):
        nullable = set()
        changed = True
        while changed:
            changed = False
            for var in self.non_terminals:
                if var in nullable:
                    continue
                for prod in self.productions.get(var, []):
                    if prod == ['ε'] or all(sym in nullable for sym in prod):
                        nullable.add(var)
                        changed = True
        
        # After detecting the eplison, we will continue to removing it
        for var in self.non_terminals:
            new_prods = []
            for prod in self.productions.get(var, []):
                nullable_pos = [i for i, sym in enumerate(prod) if sym in nullable]
                # We will try every subset of nullable positions to remove
                for r in range(len(nullable_pos) + 1):
                    for combo in combinations(nullable_pos, r):
                        remove = set(combo)
                        new_prod = [sym for i, sym in enumerate(prod) if i not in remove]
                        if len(new_prod) == 0:
                            if var == self.start_symbol and ["ε"] not in new_prods:
                                new_prods.append(["ε"])
                        elif new_prod not in new_prods:
                            new_prods.append(new_prod)
                if prod != ["ε"] and prod not in new_prods:
                    new_prods.append(prod)
            self.productions[var] = [p for p in new_prods if p != ["ε"] or var == self.start_symbol]


    # Step 3: Remove unit rules (similar to a transition rule) (A -> B)
    def _step_remove_unit(self):
        # Gonna check for transitions from one variable to another
        changed = True
        while changed:
            changed = False
            for var in list(self.non_terminals):
                new_prods = []
                for prod in self.productions.get(var, []):
                    if len(prod) ==1 and prod[0] in self.non_terminals:
                        # We found the rule A -> B
                        target = prod[0]
                        for target_prod in self.productions.get(target, []):
                            if target_prod not in new_prods and target_prod not in self.productions[var]:
                                new_prods.append(target_prod)
                        changed = True
                    else:
                        if prod not in new_prods:
                            new_prods.append(prod)
                self.productions[var] = new_prods

    # Step 4: Convert to proper binary form
    def _step_remove_form(self):
        # 1) Replace terminals in rules of length >= 2 with new variables. E.g. A -> bcd => X -> b, Y -> C, Z -> d, A -> XYZ
        terminal_vars = {}
        for var in list(self.non_terminals):
            new_prods = []
            for prod in self.productions.get(var, []):
                if len(prod) >= 2:
                    new_prod = []
                    for sym in prod:
                        if sym in self.terminals:
                            if sym not in terminal_vars:
                                # Ensure that the ID is unique
                                new_var = "U_" + sym
                                while new_var in self.non_terminals:
                                    new_var += "'"
                                terminal_vars[sym] = new_var
                                self.non_terminals.add(new_var)
                                self.productions[new_var] = [[sym]]
                            new_prod.append(terminal_vars[sym])
                        else:
                            # it is non-terminal so we just append it
                            new_prod.append(sym)
                    new_prods.append(new_prod)
                else:
                    new_prods.append(prod)
            self.productions[var] = new_prods
        
        # 2) Break the 3+ symbols into binary rules
        counter = 0
        tail_vars = {}  # maps tail tuple -> existing helper variable
        for var in list(self.non_terminals):
            new_prods = []
            for prod in self.productions.get(var, []):
                if len(prod) <= 2:
                    new_prods.append(prod)
                else:
                    # A -> u1 u2 ... uk becomes A -> u1 X1, X1 -> u2 X2, ...
                    symbols = list(prod)
                    current_var = var
                    first = True
                    while len(symbols) > 2:
                        tail = tuple(symbols[1:])
                        if tail in tail_vars:
                            # Reuse existing helper variable
                            if first:
                                new_prods.append([symbols[0], tail_vars[tail]])
                            else:
                                self.productions[current_var] = [[symbols[0], tail_vars[tail]]]
                            break
                        counter += 1
                        new_var = f"X_{counter}"
                        # Uniqueness
                        while new_var in self.non_terminals:
                            counter += 1
                            new_var = f"X_{counter}"
                        self.non_terminals.add(new_var)
                        tail_vars[tail] = new_var
                        if first:
                            new_prods.append([symbols[0], new_var]) # A -> symbols[0] new_var
                            first = False
                        else:
                            self.productions[current_var] = [[symbols[0], new_var]]
                        current_var = new_var
                        symbols = symbols[1:]
                    else:
                        self.productions[current_var] = [symbols]
            if new_prods:
                self.productions[var] = new_prods
                        

if __name__ == "__main__":
    g = CGFToCNFConverter()
    g.parse("""
            S -> ASA | aB
            A -> B | S
            B -> b | ε
            """)

    print(g)
    print()
    g.convert()
    # print("------")
    # print(g)