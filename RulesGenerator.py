numbers = {"0": "⓪", "1": "①", "2": "②", "3": "③", "4": "④", "5": "⑤", "6": "⑥", "7": "⑦", "8": "⑧", "9": "⑨"}
letters = {"A": "a", "B": "b", "C": "c", "D": "d", "E": "e", "F": "f"}
alphabet = numbers | letters

class RulesGenerator:
    def __init__(self, file):
        self.file = open(file, "w", encoding="utf-8")
    
    def write_rule(self, curr_state, curr_symbol, move, next_symbol, next_state):
        self.file.write(f"{curr_state}\t{curr_symbol}\t{move}\t{next_symbol}\t{next_state}\n")

rules = RulesGenerator("machine_rules.tsv")

rules.write_rule(f"⎆", "[", "→", "", f"A_read")
for s0 in alphabet:
    rules.write_rule(f"A_read", s0, "→", "", f"A_has_{s0}_goto_B")
for s0 in alphabet:
    for s1 in alphabet:
        rules.write_rule(f"A_has_{s0}_goto_B", s1, "→", "", "")
for s0 in alphabet:
    rules.write_rule(f"A_has_{s0}_goto_B", ",", "→", "", f"B_compare_with_{s0}")
for s0 in alphabet:
    for s1 in alphabet:
        a_symbol_value = list(alphabet).index(s0)
        b_symbol_value = list(alphabet).index(s1)
        if a_symbol_value > b_symbol_value:
            rules.write_rule(f"B_compare_with_{s0}", s1, "←", alphabet[s0], f"B_has_{s1}_goto_leftmost_A_replace")
        elif b_symbol_value > a_symbol_value:
            rules.write_rule(f"B_compare_with_{s0}", s1, "←", "", f"B_clean")
        else:
            rules.write_rule(f"B_compare_with_{s0}", s1, "←", alphabet[s1], f"B_goto_leftmost_A_mark")

for s0 in alphabet:
    for s1 in alphabet:
        rules.write_rule(f"B_has_{s0}_goto_leftmost_A_replace", s1, "←", "", "")
rules.write_rule(f"B_has_{s0}_goto_leftmost_A_replace", ",", "←", "", f"goto_leftmost_A_replace_with_{s0}")
for s0 in alphabet:
    for s1 in alphabet:
        rules.write_rule(f"goto_leftmost_A_replace_with_{s0}", s1, "←", "", "")

rules.write_rule(f"goto_leftmost_A_replace_with_{s0}", "[", "→", "", f"A_replace_with_{s0}")
rules.write_rule(f"goto_leftmost_A_replace_with_{s0}", ",", "→", "", f"A_replace_with_{s0}")
for s0 in alphabet:
    for s1 in alphabet:
        rules.write_rule(f"goto_leftmost_A_replace_with_{s0}", alphabet[s1], "→", "", f"A_replace_with_{s0}")
for s0 in alphabet:
    rules.write_rule(f"A_replace_with_{s0}", s1, "→", alphabet[s0], f"A_read")

for s0 in alphabet:
    rules.write_rule(f"B_rightleft_clean", alphabet[s0], "←", s0, "")
rules.write_rule(f"B_rightleft_clean", ",", "←", "", f"goto_leftmost_A_clean")

for s0 in alphabet:
    rules.write_rule(f"goto_leftmost_A_clean", s0, "←", "", "")
for s0 in alphabet:
    rules.write_rule(f"goto_leftmost_A_clean", alphabet[s0], "←", "", "")
rules.write_rule(f"goto_leftmost_A_clean", "[", "→", "", f"A_leftright_clean")
rules.write_rule(f"goto_leftmost_A_clean", ",", "→", "", f"A_leftright_clean")

for s0 in alphabet:
    rules.write_rule(f"A_leftright_clean", s0, "→", "", "")
for s0 in alphabet:
    rules.write_rule(f"A_leftright_clean", alphabet[s0], "→", s0, "")
rules.write_rule(f"A_leftright_clean", ",", "→", "", f"A_read")

for s0 in alphabet:
    rules.write_rule(f"B_goto_leftmost_A_mark", s0, "←", "", "")
for s0 in alphabet:
    rules.write_rule(f"B_goto_leftmost_A_mark", alphabet[s0], "←", "", "")
rules.write_rule(f"B_goto_leftmost_A_mark", ",", "←", "", f"goto_leftmost_A_mark")

for s0 in alphabet:
    rules.write_rule(f"goto_leftmost_A_mark", s0, "←", "", "")
for s0 in alphabet:
    rules.write_rule(f"goto_leftmost_A_mark", alphabet[s0], "→", "", f"read_A")
rules.write_rule(f"goto_leftmost_A_mark", "[", "→", "", f"read_A")
rules.write_rule(f"goto_leftmost_A_mark", ",", "→", "", f"read_A")

rules.write_rule(f"read_A", ",", "→", "", f"")
rules.write_rule(f"read_A", "]", "→", "", f"")





#old
rules.write_rule("⎆", "[", "→", "", "start")

for s0 in alphabet:
    rules.write_rule(f"start", s0, "→", "", f"start_{s0}")
    #write_rule(f"start", alphabet[s0], "→", "", f"start")
    for s1 in alphabet:
        rules.write_rule(f"start_{s0}", s1, "→", "", f"start_{s0}")
    rules.write_rule(f"start_{s0}", ",", "→", "", f"compare_{s0}")
    rules.write_rule(f"compare_{s0}", s0, "←", alphabet[s0], f"goto_A")
    for s1 in alphabet:
        rules.write_rule(f"compare_{s0}", alphabet[s1], "→", "", f"compare_{s0}")
        if s1 != s0:
            rules.write_rule(f"compare_{s0}", s1, "←", alphabet[s0], f"replace_A_start_with_{s1}")
        rules.write_rule(f"replace_A_start_with_{s1}", s0, "←", "", f"replace_A_start_with_{s1}")
        rules.write_rule(f"replace_A_start_with_{s1}", alphabet[s0], "←", "", f"replace_A_start_with_{s1}")
for s1 in alphabet:
    rules.write_rule(f"replace_A_start_with_{s1}", ",", "←", "", f"replace_start_with_{s1}")
    for s0 in alphabet:
        rules.write_rule(f"replace_start_with_{s1}", s0, "←", "", f"replace_start_with_{s1}")
        rules.write_rule(f"replace_start_with_{s1}", alphabet[s0], "→", "", f"replace_with_{s1}")
for s1 in alphabet:
    rules.write_rule(f"replace_start_with_{s1}", "[", "→", "", f"replace_with_{s1}")
    rules.write_rule(f"replace_start_with_{s1}", ",", "→", "", f"replace_with_{s1}")
    for s0 in alphabet:
        rules.write_rule(f"replace_with_{s1}", s0, "→", alphabet[s1], f"start")
for s0 in alphabet:
    rules.write_rule(f"goto_A", s0, "←", "", f"goto_A")
    rules.write_rule(f"goto_A", alphabet[s0], "←", "", f"goto_A")
rules.write_rule(f"goto_A", ",", "←", "", f"goto_string_start")
for s0 in alphabet:
    rules.write_rule(f"goto_string_start", s0, "←", "", f"goto_string_start")
    rules.write_rule(f"goto_string_start", alphabet[s0], "→", "", f"mark")
rules.write_rule(f"goto_string_start", "[", "→", "", f"mark")
rules.write_rule(f"goto_string_start", ",", "→", "", f"mark")
for s0 in alphabet:
    rules.write_rule(f"mark", s0, "→", alphabet[s0], f"start")

rules.write_rule(f"start", ",", "→", "", f"clean_string_clean_string")

for s0 in alphabet:
    rules.write_rule(f"clean_string__clean_string", alphabet[s0], "→", s0, f"clean_string__clean_string")
rules.write_rule(f"clean_string__clean_string", ",", "→", "", f"start")