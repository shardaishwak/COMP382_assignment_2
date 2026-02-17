from grammar import Grammar

class CGFToCNFConverter(Grammar):
    def convert(self):
        # Call step 1
        self._step_new_start()
        # Call step 2
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



