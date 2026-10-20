input    = "[" , ( entries | ε ) , "]"

entries  = hex_word , { "," , hex_word }

hex_word = hex , hex , hex , hex
           hex , hex , hex , hex
           hex , hex , hex , hex
           hex , hex , hex , hex



hex = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]

class TuringMachine:
    def __init__(self, tape_alphabet, blank_symbol, states, halting_states, start_state, accepting_halt_state, transition_function):


    def count():
        step_counter += 1

    def read():


    def write():


    def update():
        self.state =

    def move():
        
