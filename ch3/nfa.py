
class FARule:
    def __init__(self, state, character, next_state):
        self.state = state
        self.character  = character
        self.next_state = next_state

    def applies_to(self, state, character):
        return self.state == state and self.character == character

    @staticmethod
    def follow(self):
        return self.next_state

    def __repr__(self):
        return "<FARule: %s -- %s --> %s>" % (self.state, self.character, self.next_state)

class NFARulebook:
    def __init__(self, rules):
        self.rules = rules

    def rules_for(self, state, character):
        return [rule for rule in self.rules if rule.applies_to(state, character)]

    def next_states(self, states, character):
        s = set()
        for state in states:
            s.update(map(FARule.follow, self.rules_for(state, character)))
        return s

    def follow_free_moves(self, states):
        more_states = self.next_states(states, None)
        return states if more_states.issubset(states) else self.follow_free_moves(states | more_states)

class NFA:
    def __init__(self, current_states, accept_states, rulebook):
        self.current_states = current_states
        self.accept_states = accept_states
        self.rulebook = rulebook

    def accepting(self):
        return bool(self.get_current_states() & self.accept_states)

    def read_character(self, character):
        self.current_states = self.rulebook.next_states(self.get_current_states(), character)

    def read_string(self, s):
        for c in s:
           self.read_character(c)

    def get_current_states(self):
        return self.rulebook.follow_free_moves(self.current_states)

class NFADesign:
    def __init__(self, start_state, accept_states, rulebook):
        self.start_state = start_state
        self.accept_states = accept_states
        self.rulebook = rulebook

    def to_nfa(self):
        return NFA({self.start_state}, self.accept_states, self.rulebook)

    def accepts(self, s):
        nfa = self.to_nfa()
        nfa.read_string(s)
        return nfa.accepting()

if __name__ == '__main__':
    rb = NFARulebook([
        FARule(1, 'a', 1), FARule(1, 'b', 1), FARule(1, 'b', 2),
        FARule(2, 'a', 3), FARule(2, 'b', 3),
        FARule(3, 'a', 4), FARule(3, 'b', 4)
    ])
    print(rb.next_states({1}, 'b'))
    print(rb.next_states({1,2}, 'a'))
    print(rb.next_states({1,3}, 'b'))
    print(' ')

    print(NFA({1}, {4}, rb).accepting())
    print(NFA({1, 2, 4}, {4}, rb).accepting())

    nfa = NFA({1}, {4}, rb)
    print(nfa.accepting())
    nfa.read_string('bbbbb')
    print(nfa.accepting())
    print(' ')

    nfa_design = NFADesign(1, {4}, rb)
    print(nfa_design.accepts('bab'))
    print(nfa_design.accepts('bbbbb'))
    print(nfa_design.accepts('bbabb'))
    print(' ')

    rb2 = NFARulebook([
     FARule(1, None, 2), FARule(1, None, 4),
     FARule(2, 'a', 3),
     FARule(3, 'a', 2),
     FARule(4, 'a', 5),
     FARule(5, 'a', 6),
     FARule(6, 'a', 4)
    ])
    print(rb2.next_states({1}, None))
    print(rb2.follow_free_moves({1}))
    print(' ')

    nfa_design = NFADesign(1, {2, 4}, rb2)
    print(nfa_design.accepts('aa'))
    print(nfa_design.accepts('aaa'))
    print(nfa_design.accepts('aaaaa'))
    print(nfa_design.accepts('aaaaaa'))



