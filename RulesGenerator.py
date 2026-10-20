alphabet = {"0": "⓪", "1": "①", "2": "②", "3": "③", "4": "④", "5": "⑤", "6": "⑥", "7": "⑦", "8": "⑧", "9": "⑨", "A": "a", "B": "b", "C": "c", "D": "d", "E": "e", "F": "f"}

numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
letters = ["A", "B", "C", "D", "E", "F"]

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
write_rule(f"return", "[", "→", "", f"compare")

for s0 in alphabet:
    write_rule(f"compare", s0, "→", alphabet[s0], f"compare_forward_{s0}")
    write_rule(f"compare_forward_{s0}", s0, "→", "", f"compare_forward_{s0}")
    write_rule(f"compare_forward_{s0}", ",", "→", "", f"compare_{s0}")
    for s1 in alphabet:
        #look at index and decide to replace or not
        write_rule(f"compare_{s0}", s1, "→", "", f"compare_forward_{s0}")



for s0 in alphabet:
    write_rule(f"read_", s0, "→", "", f"next_{s0}")
    write_rule(f"next_{s0}", ",", "→", "", f"compare_{s0}")
    write_rule(f"compare_{s0}", "s0", "→", "", f"compare_{s0}")
    for s1 in alphabet:
        write_rule(f"go_swap_{s0}", s1, "→", "", f"go_swap_{s0}")
    for s1 in alphabet:
        write_rule(f"pivot_{s0}", s1, "→", "", f"next_word_{s0}{s1}")

write_rule(f"read_word", ",", "→", "", f"next_word_{s0}")