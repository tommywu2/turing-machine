alphabet = {"0": "⓪", "1": "①", "2": "②", "3": "③", "4": "④", "5": "⑤", "6": "⑥", "7": "⑦", "8": "⑧", "9": "⑨", "A": "a", "B": "b", "C": "c", "D": "d", "E": "e", "F": "f"}

numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
letters = ["A", "B", "C", "D", "E", "F"]

states = {"PIVOT": "pivot"}

file = open("machine_rules.tsv", "w", encoding="utf-8")

def write_rule(curr_state, curr_symbol, move, next_symbol, next_state):
    file.write(f"{curr_state}\t{curr_symbol}\t{move}\t{next_symbol}\t{next_state}\n")


write_rule("⎆", "[", "→", "", "start")

for s0 in alphabet:
    write_rule(f"start", s0, "→", "", f"start_{s0}")
    #write_rule(f"start", alphabet[s0], "→", "", f"start")
    for s1 in alphabet:
        write_rule(f"start_{s0}", s1, "→", "", f"start_{s0}")
    write_rule(f"start_{s0}", ",", "→", "", f"compare_{s0}")
    write_rule(f"compare_{s0}", s0, "←", alphabet[s0], f"goto_A")
    for s1 in alphabet:
        write_rule(f"compare_{s0}", alphabet[s1], "→", "", f"compare_{s0}")
        if s1 != s0:
            write_rule(f"compare_{s0}", s1, "←", alphabet[s0], f"replace_A_start_with_{s1}")
        write_rule(f"replace_A_start_with_{s1}", s0, "←", "", f"replace_A_start_with_{s1}")
        write_rule(f"replace_A_start_with_{s1}", alphabet[s0], "←", "", f"replace_A_start_with_{s1}")
for s1 in alphabet:
    write_rule(f"replace_A_start_with_{s1}", ",", "←", "", f"replace_start_with_{s1}")
    for s0 in alphabet:
        write_rule(f"replace_start_with_{s1}", s0, "←", "", f"replace_start_with_{s1}")
        write_rule(f"replace_start_with_{s1}", alphabet[s0], "→", "", f"replace_with_{s1}")
for s1 in alphabet:
    write_rule(f"replace_start_with_{s1}", "[", "→", "", f"replace_with_{s1}")
    write_rule(f"replace_start_with_{s1}", ",", "→", "", f"replace_with_{s1}")
    for s0 in alphabet:
        write_rule(f"replace_with_{s1}", s0, "→", alphabet[s1], f"start")
for s0 in alphabet:
    write_rule(f"goto_A", s0, "←", "", f"goto_A")
    write_rule(f"goto_A", alphabet[s0], "←", "", f"goto_A")
write_rule(f"goto_A", ",", "←", "", f"goto_string_start")
for s0 in alphabet:
    write_rule(f"goto_string_start", s0, "←", "", f"goto_string_start")
    write_rule(f"goto_string_start", alphabet[s0], "→", "", f"mark")
write_rule(f"goto_string_start", "[", "→", "", f"mark")
write_rule(f"goto_string_start", ",", "→", "", f"mark")
for s0 in alphabet:
    write_rule(f"mark", s0, "→", alphabet[s0], f"start")

write_rule(f"start", ",", "→", "", f"clean_string_clean_string")

for s0 in alphabet:
    write_rule(f"clean_string__clean_string", alphabet[s0], "→", s0, f"clean_string__clean_string")
write_rule(f"clean_string__clean_string", ",", "→", "", f"start")