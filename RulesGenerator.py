numbers = {"0": "⓪", "1": "①", "2": "②", "3": "③", "4": "④", "5": "⑤", "6": "⑥", "7": "⑦", "8": "⑧", "9": "⑨"}
letters = {"A": "a", "B": "b", "C": "c", "D": "d", "E": "e", "F": "f"}
alphabet = numbers | letters

class RulesGenerator:
    def __init__(self, file):
        self.file = open(file, "w", encoding="utf-8")
    
    def write_rule(self, curr_state, curr_symbol, move, next_symbol, next_state):
        self.file.write(f"{curr_state}\t{curr_symbol}\t{move}\t{next_symbol}\t{next_state}\n")

rules = RulesGenerator("machine_rules.tsv")

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