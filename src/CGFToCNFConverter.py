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
        self._step_replace_terminals()
        # Call step 5
        self._step_break_down_products_to_binary()

        return self

    
    def _step_new_start(self):
        """Step 1: Add new start variable S0 -> S"""
        old_start = self.start_symbol
        new_start = old_start + "0"
        while new_start in self.non_terminals:
            # Handle the case where a variable was already called S0(')*
            new_start += "'"

        self.non_terminals.add(new_start)
        self.productions[new_start] = [[old_start]]
        self.start_symbol = new_start

    
    def _step_remove_epsilon(self):
        """Step 2: Remove epsilon rule"""
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


    
    def _step_remove_unit(self):
        """Step 3: Remove unit rules (similar to a transition rule) (A -> B)"""
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

    def _step_replace_terminals(self):
        """Step 4: replace terminals when RHS Lenght > 2 and replace them with a variable """
        #For example, A->aB
        #becomes 
        #A-> X_aB        ,and
        #X_a -> a
        
        terminals = {}
        x_index = 1
        for x in list(self.non_terminals):
            new_prods = []
            for prod in self.productions.get(x, []): #get each one
                #if the prods are <=1 add them
                if len(prod) <= 1:

                    new_prods.append(prod)
                    
                    continue
                    
                new_prod = []
                for symbol in prod:
                    if symbol in self.terminals: 
                        if symbol not in terminals:
                            #we havent seen it yet so create a new non-terminal for this terminal
                            new_var = f"X{x_index}" #name like X1,X2....
                           
                            while new_var in self.non_terminals: #if X1,X2 .. are taken etc
                                x_index +=1
                                new_var = f"X{x_index}" #name like X1,X2....

                            self.non_terminals.add(new_var)
                            self.productions[new_var] = [[symbol]]
                            terminals[symbol] = new_var

                        new_prod.append(terminals[symbol])
                    else:
                        new_prod.append(symbol)
                new_prods.append(new_prod)
            self.productions[x] = new_prods        



    def _step_break_down_products_to_binary(self):
        """Step 5:breaks down productions into binary(2) ones"""
        #For example A->BCD is invalid so we much break it down 
        #WE can do
        #A ->BC1
        #C1 ->CD
        #valid  ✓
        x_index = 1 #for naming non-terminals

        for x in list(self.non_terminals):
            new_prods = []
            for prod in self.productions.get(x, []): 
                if len(prod) <= 2: #we chilling add it
                    new_prods.append(prod)
                    continue

                #A ->B1 B2 B3 B4 ....... Bn
                #A -> B1 C1 , C1 -> B2 C2. repeating, the last rule will have two non-terminals Cn-2 -> Bn-1 Bn

                current_var = x #left hand side
                for i in range(len(prod) -2):
                    new_var = f"C{x_index}" #like step 4
                    while new_var in self.non_terminals: 
                        x_index +=1
                        new_var = f"C{x_index}" 

                    self.non_terminals.add(new_var)
                    if current_var == x: # if this is the first time update the original rule
                        new_prods.append([prod[i], new_var]) 
                    else: # else make a new rule
                        self.productions[current_var] = [[prod[i], new_var]]

                    current_var = new_var #move to next
                    x_index +=1
                    
            #cover the last 2 operations no in  for i in range(len(prod) -2)
                self.productions[current_var] = [[prod[-2], prod[-1]]]

            self.productions[x] = new_prods




                



