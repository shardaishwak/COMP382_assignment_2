import pytest
from grammar import Grammar

class TestValidCNF:
    def test_valid_cnf_single_terminal(self):
        g = Grammar()
        g.non_terminals = {"S", "A"}
        g.terminals = {"a", "b"}
        g.productions = {
            "S": [["a"]],
            "A": [["b"]]
        }
        assert g.valid_cnf() is True

    def test_valid_cnf_two_nonterminals(self):
        g = Grammar()
        g.non_terminals = {"S", "A", "B"}
        g.terminals = {"a", "b"}
        g.productions = {
            "S": [["A", "B"]],
            "A": [["a"]],
            "B": [["b"]]
        }
        assert g.valid_cnf() is True

    def test_invalid_cnf_terminal_nonterminal_mix(self):
        g = Grammar()
        g.non_terminals = {"S", "A"}
        g.terminals = {"a"}
        g.productions = {
            "S": [["a", "A"]],
            "A": [["a"]]
        }
        assert g.valid_cnf() is False

    def test_invalid_cnf_unit_rule(self):
        g = Grammar()
        g.non_terminals = {"S", "A"}
        g.terminals = {"a"}
        g.productions = {
            "S": [["A"]],
            "A": [["a"]]
        }
        assert g.valid_cnf() is False
