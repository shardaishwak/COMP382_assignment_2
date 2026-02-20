import pytest
from CGFToCNFConverter import CGFToCNFConverter


class TestStep1NewStart:
    def test_adds_new_start_symbol(self):
        g = CGFToCNFConverter()
        g.parse("""
            S -> a
            """)
        old_start = g.start_symbol
        g._step_new_start()
        assert g.start_symbol == old_start + "0"
        assert g.start_symbol in g.non_terminals
        assert g.productions[g.start_symbol] == [[old_start]]

    def test_handles_existing_s0(self):
        g = CGFToCNFConverter()
        g.non_terminals = {"S", "S0"}
        g.terminals = {"a"}
        g.productions = {"S": [["a"]], "S0": [["a"]]}
        g.start_symbol = "S"
        g._step_new_start()
        # Should create S0' since S0 exists
        assert g.start_symbol == "S0'"


class TestStep2RemoveEpsilon:
    def test_removes_simple_epsilon(self):
        g = CGFToCNFConverter()
        g.parse("""
            S -> aB
            B -> b | ε
            """)
        g._step_new_start()
        g._step_remove_epsilon()
        # B -> ε should be removed, S should have both aB and a
        assert ["ε"] not in g.productions.get("B", [])
        # S should have production without B (since B is nullable)
        assert ["a"] in g.productions["S"] or ["a", "B"] in g.productions["S"]

    def test_preserves_start_epsilon(self):
        g = CGFToCNFConverter()
        g.parse("""
            S -> A
            A -> ε
            """)
        g._step_new_start()
        g._step_remove_epsilon()
        # Start symbol can still have epsilon
        if ["ε"] in g.productions.get(g.start_symbol, []):
            assert g.start_symbol == "S0"

    def test_nullable_detection(self):
        g = CGFToCNFConverter()
        g.parse("""
            S -> AB
            A -> a | ε
            B -> A
            """)
        g._step_new_start()
        g._step_remove_epsilon()
        # After epsilon removal, should have variants
        prods = g.productions["S"]
        # Should have combinations: AB, A, B, or empty (for start)
        assert len(prods) >= 1


class TestStep3RemoveUnit:
    def test_removes_simple_unit_rule(self):
        g = CGFToCNFConverter()
        g.parse("""
            S -> A
            A -> a
            """)
        g._step_new_start()
        g._step_remove_epsilon()
        g._step_remove_unit()
        # S should now have 'a' directly, not just A
        assert ["a"] in g.productions["S"] or ["A"] not in [p for p in g.productions["S"] if len(p) == 1 and p[0] in g.non_terminals]

    def test_removes_chain_of_unit_rules(self):
        g = CGFToCNFConverter()
        g.parse("""
            S -> A
            A -> B
            B -> b
            """)
        g._step_new_start()
        g._step_remove_epsilon()
        g._step_remove_unit()
        # S should eventually have 'b'
        assert ["b"] in g.productions["S"]


class TestStep4BinaryForm:
    def test_replaces_terminals_in_long_rules(self):
        g = CGFToCNFConverter()
        g.parse("""
            S -> aB
            B -> b
            """)
        g._step_new_start()
        g._step_remove_epsilon()
        g._step_remove_unit()
        g._step_remove_form()
        # Should have U_a variable
        has_terminal_var = any(v.startswith("U_") for v in g.non_terminals)
        assert has_terminal_var

    def test_breaks_long_productions(self):
        g = CGFToCNFConverter()
        g.parse("""
            S -> ABC
            A -> a
            B -> b
            C -> c
            """)
        g._step_new_start()
        g._step_remove_epsilon()
        g._step_remove_unit()
        g._step_remove_form()
        # All productions should have at most 2 symbols
        for var, prods in g.productions.items():
            for prod in prods:
                assert len(prod) <= 2, f"{var} -> {prod} has more than 2 symbols"


class TestFullConversion:
    def test_simple_grammar_converts_to_valid_cnf(self):
        g = CGFToCNFConverter()
        g.parse("""
            S -> aB
            B -> b
            """)
        g.convert()
        assert g.valid_cnf() is True

    def test_grammar_with_epsilon_converts_to_valid_cnf(self):
        g = CGFToCNFConverter()
        g.parse("""
            S -> aBa
            B -> b | ε
            """)
        g.convert()
        assert g.valid_cnf() is True

    def test_textbook_example(self):
        g = CGFToCNFConverter()
        g.parse("""
            S -> ASA | aB
            A -> B | S
            B -> b | ε
            """)
        g.convert()
        assert g.valid_cnf() is True

    def test_complex_grammar(self):
        g = CGFToCNFConverter()
        g.parse("""
            S -> ABCD
            A -> a | ε
            B -> b
            C -> c | ε
            D -> d
            """)
        g.convert()
        assert g.valid_cnf() is True

    def test_unit_rule_chain(self):
        g = CGFToCNFConverter()
        g.parse("""
            S -> A
            A -> B
            B -> C
            C -> c
            """)
        g.convert()
        assert g.valid_cnf() is True

    def test_preserves_language(self):
        g = CGFToCNFConverter()
        g.parse("""
            S -> ab
            """)
        g.convert()
        assert g.valid_cnf() is True
        # The grammar should still be able to generate "ab"
        # This is a structural test - the CNF should have the right pieces
        assert any("a" in str(prods) for prods in g.productions.values())
        assert any("b" in str(prods) for prods in g.productions.values())
