alphabet = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
letters = ["A", "B", "C", "D", "E", "F"]
letters = {"A": "10", "B": "11", "C": "12", "D": "13", "E": "14", "F": "15"}
states = {"PIVOT": "pivot"}

file = open("machine_rules.tsv", "w", encoding="utf-8")

def write_rule(curr_state, curr_symbol, move, next_symbol, next_state):
    file.write(f"{curr_state}\t{curr_symbol}\t{move}\t{next_symbol}\t{next_state}\n")


write_rule("⎆", "[", "→", "", "setup")

for n0 in numbers:
    write_rule(f"setup", n0, "→", "", f"setup")
for l0 in letters:
    write_rule(f"setup", l0, "→", "", f"setup")
write_rule(f"setup", ",", "→", "", f"setup")
write_rule(f"setup", "]", "←", "|", f"return")

for n0 in numbers:
    write_rule(f"return", n0, "←", "", f"return")
for l0 in letters:
    write_rule(f"return", l0, "←", "", f"return")
write_rule(f"return", ",", "←", "", f"return")
write_rule(f"return", "[", "→", "", f"start")






for s0 in alphabet:
    write_rule(f"read_", s0, "→", "", f"next_{s0}")
    write_rule(f"next_{s0}", ",", "→", "", f"compare_{s0}")
    write_rule(f"compare_{s0}", "s0", "→", "", f"compare_{s0}")
    for s1 in alphabet:
        write_rule(f"go_swap_{s0}", s1, "→", "", f"go_swap_{s0}")
    for s1 in alphabet:
        write_rule(f"pivot_{s0}", s1, "→", "", f"next_word_{s0}{s1}")

write_rule(f"read_word", ",", "→", "", f"next_word_{s0}")