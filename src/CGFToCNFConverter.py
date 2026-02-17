from grammar import Grammar
from itertools import combinations
class CGFToCNFConverter(Grammar):
    def convert(self):
        # Call step 1
        self._step_new_start()
        # Call step 2
        self._step_remove_epsilon()
        # Call step 3
        self._step_remove_unit()
        # Call step 4
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



