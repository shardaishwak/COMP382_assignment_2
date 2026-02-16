class Grammar:
    def __init__(self, _non_terminals = set(), _terminals = set(), _productions = {}, _start_symbol = None):
        self.non_terminals = _non_terminals
        self.terminals = _terminals
        self.productions = _productions # The format is {"A", [["a", "B", "b"], ["c"]]}
        self.start_symbol = _start_symbol

    def parse(self, grammar_string):
        self.non_terminals = set()
        self.terminals = set()
        self.productions = {} # The format is {"A", [["a", "B", "b"], ["c"]]}
        self.start_symbol = None

        # TODO: Read the lines
        lines = grammar_string.strip().split("\n")
        # TODO: Consider the non-terminal names from the left side
        non_terminals_names = set()
        for line in lines:
            line = line.strip()
            if not line or "->" not in line:
                continue
            lhs, _ = line.split("->", 1)
            non_terminals_names.add(lhs.strip())

        # TODO: Build productions, terminals, non-terminals
        for line in lines:
            line = line.strip()
            if not line or "->" not in line:
                continue

            lhs, rhs = line.split("->", 1)
            lhs = lhs.strip()
            # There is only the non-terminal on the left side
            self.non_terminals.add(lhs)
            if self.start_symbol is None:
                # NOTE: assuming the first rule is the start
                self.start_symbol = lhs
            if lhs not in self.productions:
                self.productions[lhs] = []
            
            # Split the alternatives by "\" as [[...], [...]]
            alternatives = rhs.split("|")
            for alt in alternatives:
                alt = alt.strip()
                body = []
                for char in alt:
                    if char == " ":
                        continue
                    if char.isupper() or char in non_terminals_names:
                        self.non_terminals.add(char)
                    else:
                        self.terminals.add(char)
                    body.append(char)
                self.productions[lhs].append(body)
        return self.non_terminals, self.terminals, self.productions, self.start_symbol
    
    def __str__(self):
        lines = []
        order = []
        if self.start_symbol:
            order.append(self.start_symbol)
        order += sorted(self.non_terminals - {self.start_symbol} if self.start_symbol else self.non_terminals)
        for var in order:
            prods = self.productions.get(var, [])
            if prods:
                rhs = " | ".join("".join(p) for p in prods)
                lines.append(f"  {var} -> {rhs}")
        return "\n".join(lines)


if __name__ == "__main__":
    grammar_string = """
    S -> aBa | CD
    B -> c
    P -> r | s
    """

    g = Grammar()
    g.parse(grammar_string)
    print(grammar_string)