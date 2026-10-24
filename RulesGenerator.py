numbers = {"0": "⓪", "1": "①", "2": "②", "3": "③", "4": "④", "5": "⑤", "6": "⑥", "7": "⑦", "8": "⑧", "9": "⑨"}
letters = {"A": "a", "B": "b", "C": "c", "D": "d", "E": "e", "F": "f"}
alphabet = numbers | letters

class RulesGenerator:
    def __init__(self, file):
        self.file = open(file, "w", encoding="utf-8")
    
    def write_rule(self, curr_state, curr_symbol, move, next_symbol, next_state):
        self.file.write(f"{curr_state}\t{curr_symbol}\t{move}\t{next_symbol}\t{next_state}\n")

rules = RulesGenerator("machine_rules.tsv")

rules.write_rule(f"⎆", "[", "→", "", f"A_read_for_comparison")
for s0 in alphabet:
    rules.write_rule(f"A_read_for_comparison", s0, "→", alphabet[s0], f"A_has_{s0}_goto_B_for_comparison")

for s0 in alphabet:
    for s1 in alphabet:
        rules.write_rule(f"A_has_{s0}_goto_B_for_comparison", s1, "→", "", f"")

for s0 in alphabet:
    rules.write_rule(f"A_has_{s0}_goto_B_for_comparison", ",", "→", "", f"A_has_{s0}_compare_with_B")

for s0 in alphabet:
    for s1 in alphabet:
        a_symbol_value = list(alphabet).index(s0)
        b_symbol_value = list(alphabet).index(s1)
        if a_symbol_value > b_symbol_value:
            rules.write_rule(f"A_has_{s0}_compare_with_B", s1, "→", alphabet[s0], f"B_read_for_switch")
        elif b_symbol_value > a_symbol_value:
            rules.write_rule(f"A_has_{s0}_compare_with_B", s1, "←", "", f"B_rightleft_clean")
        else:
            rules.write_rule(f"A_has_{s0}_compare_with_B", s1, "←", alphabet[s1], f"B_goto_A_for_comparison")
        
for s0 in alphabet:
    rules.write_rule(f"B_read_for_switch", s0, "←", "", f"B_has_{s0}_goto_A_for_switch")

#A is bigger switch loop.
for s0 in alphabet:
    for s1 in alphabet:
        rules.write_rule(f"B_has_{s0}_goto_A_for_switch", alphabet[s1], "←", "", f"")
for s0 in alphabet:
    rules.write_rule(f"B_has_{s0}_goto_A_for_switch", ",", "←", "", f"B_has_{s0}_switch_with_A")

for s0 in alphabet:
    for s1 in alphabet:
        rules.write_rule(f"B_has_{s0}_switch_with_A", s1, "←", "", f"")
for s0 in alphabet:
    rules.write_rule(f"B_has_{s0}_switch_with_A", "[", "→", "", f"B_has_{s0}_switch_with_A_here")
for s0 in alphabet:
    rules.write_rule(f"B_has_{s0}_switch_with_A", ",", "→", "", f"B_has_{s0}_switch_with_A_here")
for s0 in alphabet:
    for s1 in alphabet:
        rules.write_rule(f"B_has_{s0}_switch_with_A", alphabet[s1], "→", "", f"B_has_{s0}_switch_with_A_here")

for s0 in alphabet:
    for s1 in alphabet:
        rules.write_rule(f"B_has_{s0}_switch_with_A_here", s1, "→", alphabet[s0], f"A_has_{s1}_goto_B_for_switch")

for s0 in alphabet:
    for s1 in alphabet:
        rules.write_rule(f"A_has_{s0}_goto_B_for_switch", s1, "→", "", f"")
for s0 in alphabet:
        rules.write_rule(f"A_has_{s0}_goto_B_for_switch", ",", "→", "", f"A_has_{s0}_switch_with_B")

for s0 in alphabet:
    for s1 in alphabet:
        rules.write_rule(f"A_has_{s0}_switch_with_B", alphabet[s1], "→", "", f"")
for s0 in alphabet:
    for s1 in alphabet:
        rules.write_rule(f"A_has_{s0}_switch_with_B", s1, "→", alphabet[s0], f"B_has_{s0}_goto_A_for_switch")

#B is bigger
for s0 in alphabet:
    rules.write_rule(f"B_rightleft_clean", alphabet[s0], "←", s0, f"")
rules.write_rule(f"B_rightleft_clean", ",", "←", s0, f"A_rightleft_clean")

for s0 in alphabet:
    rules.write_rule(f"A_rightleft_clean", s0, "←", "", f"")
for s0 in alphabet:
    rules.write_rule(f"A_rightleft_clean", alphabet[s0], "←", s0, f"")
rules.write_rule(f"A_rightleft_clean", "[", "→", s0, f"A_goto_B_for_new_comparison")
rules.write_rule(f"A_rightleft_clean", ",", "→", s0, f"A_goto_B_for_new_comparison")

for s0 in alphabet:
    rules.write_rule(f"A_goto_B_for_new_comparison", s0, "→", "", f"")
rules.write_rule(f"A_goto_B_for_new_comparison", ",", "→", "", f"")

#A and B has the same symbol.
for s0 in alphabet:
    rules.write_rule(f"B_goto_A_for_comparison", alphabet[s0], "←", "", f"")
rules.write_rule(f"B_goto_A_for_comparison", ",", "←", "", f"A_goto_leftmost_symbol_for_comparison")

for s0 in alphabet:
    rules.write_rule(f"A_goto_leftmost_symbol_for_comparison", s0, "←", "", f"")
for s0 in alphabet:
    rules.write_rule(f"A_goto_leftmost_symbol_for_comparison", alphabet[s0], "→", "", f"A_read_for_comparison")

#No more symbols when reading A
rules.write_rule(f"A_read_for_comparison", ",", "→", "", f"A_goto_leftmost_symbol_for_cleaning")
for s0 in alphabet:
    rules.write_rule(f"A_goto_leftmost_symbol_for_cleaning", alphabet[s0], "←", "", f"")
rules.write_rule(f"A_goto_leftmost_symbol_for_cleaning", "[", "→", "", f"A_leftright_clean")

for s0 in alphabet:
    rules.write_rule(f"A_leftright_clean", alphabet[s0], "→", s0, f"A_leftright_clean")
rules.write_rule(f"A_leftright_clean", ",", "→", "", f"B_leftright_clean")
for s0 in alphabet:
    rules.write_rule(f"B_leftright_clean", alphabet[s0], "→", s0, f"B_leftright_clean")
rules.write_rule(f"B_leftright_clean", ",", "→", "", f"A_goto_leftmost_symbol_for_comparison")

#No hex string.
rules.write_rule(f"A_read_for_comparison", "]", "←", "", f"A_goto_tape_start_for_ending")
rules.write_rule(f"A_goto_tape_start_for_ending", "]", "←", "", f"✔")

#No B for A to compare with. i.e. end of current sort cycle.
for s0 in alphabet:
    rules.write_rule(f"A_has_{s0}_goto_B_for_comparison", "]", "←", "", f"A_goto_left_wall_for_marking")
for s0 in alphabet:
    rules.write_rule(f"A_has_{s0}_goto_B_for_comparison", "/", "←", "", f"A_goto_left_wall_for_marking")

for s0 in alphabet:
    rules.write_rule(f"A_goto_left_wall_for_marking", s0, "←", "", f"")
for s0 in alphabet:
    rules.write_rule(f"A_goto_left_wall_for_marking", alphabet[s0], "←", s0, f"")
rules.write_rule(f"A_goto_left_wall_for_marking", ",", "←", "/", f"rightleft_low_clean")

for s0 in alphabet:
    rules.write_rule(f"rightleft_low_clean", alphabet[s0], "←", s0, f"")
rules.write_rule(f"rightleft_low_clean", ",", "←", "", f"")
rules.write_rule(f"rightleft_low_clean", "[", "→", "", f"A_read_for_comparison")

#when there is no left wall to mark (i.e. the full comparison is done).
rules.write_rule(f"A_goto_left_wall_for_marking", "[", "→", "", f"leftright_full_clean")
for s0 in alphabet:
    rules.write_rule(f"leftright_full_clean", alphabet[s0], "→", s0, f"")
rules.write_rule(f"leftright_full_clean", "/", "→", ",", f"")

rules.write_rule(f"leftright_full_clean", "]", "→", "", f"A_goto_tape_start_for_ending")