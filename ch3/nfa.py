
class FARule:
    def __init__(self, state, character, next_state):
        self.state = state
        self.character  = character
        self.next_state = next_state

    def applies_to(self, state, character):
        return self.state == state and self.character == character

    def follow(self):
        return self.next_state

    def __repr__(self):
        return "<FARule: %s -- %s --> %s>" % (self.state, self.character, self.next_state)


class DFARulebook:
    def __init__(self, rules):
        self.rules = rules

    def rule_for(self, state, character):
        for rule in self.rules:
            if rule.applies_to(state, character):
                return rule
        return None

    def next_state(self, state, character):
        return self.rule_for(state, character).follow()

class DFA:
    def __init__(self, current_state, accept_states, rulebook):
        self.current_state = current_state
        self.accept_state = accept_states
        self.rulebook = rulebook

    def accepting(self):
        return self.current_state in self.accept_state

    def read_character(self, character):
        self.current_state = self.rulebook.next_state(self.current_state, character)

    def read_string(self, s):
        for c in s:
           self.read_character(c)

class DFADesign:
    def __init__(self, current_state, accept_states, rulebook):
        self.current_state = current_state
        self.accept_state = accept_states
        self.rulebook = rulebook

    def to_dfa(self):
        return DFA(self.current_state, self.accept_state, self.rulebook)

    def accepts(self, s):
        dfa = self.to_dfa()
        dfa.read_string(s)
        return dfa.accepting()

if __name__ == '__main__':
    rb = DFARulebook([
        FARule(1, 'a', 2), FARule(1, 'b', 1),
        FARule(2, 'a', 2), FARule(2, 'b', 3),
        FARule(3, 'a', 3), FARule(3, 'b', 3)
    ])
    print(rb.next_state(1, 'a'))
    print(rb.next_state(1, 'b'))
    print(rb.next_state(2, 'b'))
    print(' ')

    print(DFA(1, [1,3], rb).accepting())
    print(DFA(1, [3], rb).accepting())
    print(' ')

    dfa_design = DFADesign(1, [3], rb)
    print(dfa_design.accepts('a'))
    print(dfa_design.accepts('baa'))
    print(dfa_design.accepts('baba'))
    print(' ')


