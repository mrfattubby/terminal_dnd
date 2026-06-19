from yaml import safe_load_all, YAMLError


LINE_SEP = 80 * "*"


# TODO: Split spells into a separate module
class Spell():
    def __init__(self, name: str, level: int, cast_time: str, range: str, duration: str, components: str, description: str, prepared: bool = True, concentration: bool = False, ritual: bool = False, free_casts: int = 0, wild_shape: bool = False):
        # TODO: Finish setting up later
        pass


class Character():
    def __init__(self, config: dict) -> None:
        self.name = config["Name"]
        self.level = config["Level"]
        self.char_class = config["Class"]  # Can't use .class since class is a restricted Python expression
        self.subclass = config["Subclass"]
        self.background = config["Background"]
        self.species = config["Species"]
        self.subspecies = config["Subspecies"]
        self.alignment = config["Alignment"]
        self.size = config["Size"]
        self.ac = config["AC"]
        self.initiative = config["Initiative"]
        self.speed = config["Speed"]
        self.prof_bonus = config["Proficiency Bonus"]
        self.attributes = config["Attributes"]
        self.spells = config["Spells"]  # TODO: Convert spell names into Spell objects


class State():
    def __init__(self, char: Character, name: str, entry_command: str, allowed_states: list[str], help_message: str) -> None:
        self.char = char
        self.name = name
        self.entry_command = entry_command
        self.allowed_states = allowed_states
        self.help_message = help_message
        self.commands = {}

    def show_entry(self) -> None:
        pass

    def show_help(self, all_states: list) -> None:
        print(f"Current state: {self.name.title()}")

        print("Commands:")
        for command in self.commands.keys():
            print(f"\t{command}\t{self.commands[command]['name'].title()}")

        print("Available states:")
        for state in all_states:
            if state.name in self.allowed_states:
                print(f"\t{state.entry_command}\t{state.name.title()}")
        print("\tEXI\tExit terminal")


class Main_State(State):
    def __init__(self, char: Character, name: str, entry_command: str, allowed_states: list[str], help_message: str):
        super().__init__(char, name, entry_command, allowed_states, help_message)
        self.commands = {"ACC": {"func": self.show_ac, "name": "Show AC"}, "MOV": {"func": self.show_movement, "name": "Show Movement Speed"}}  # TODO: Extend

    def show_entry(self) -> None:
        super().show_entry()
        print(LINE_SEP)
        print(f"{self.char.name}")
        print(f"Level:\t\t{self.char.level}")
        print(f"Class:\t\t{self.char.char_class} - {self.char.subclass}")
        print(f"Species:\t{self.char.species} - {self.char.subspecies}")
        print(f"Background:\t{self.char.background}")
        print(f"Alignment:\t{self.char.alignment}")
        print(LINE_SEP)
        print("Attributes:")
        print(f"STR:\t\t{self.char.attributes['STR']}")
        print(f"DEX:\t\t{self.char.attributes['DEX']}")
        print(f"CON:\t\t{self.char.attributes['CON']}")
        print(f"INT:\t\t{self.char.attributes['INT']}")
        print(f"WIS:\t\t{self.char.attributes['WIS']}")
        print(f"CHA:\t\t{self.char.attributes['CHA']}")
        print(LINE_SEP)
        print(f"AC:\t\t{self.char.ac}")
        print(f"Initiative:\t{self.char.initiative}")
        print(f"Speed:\t\t{self.char.speed}")
        print(LINE_SEP)

    def show_ac(self):
        print(f"AC = {self.char.ac}")

    def show_movement(self):
        print(f"Speed = {self.char.speed}")


class Spells_State(State):
    def __init__(self, char: Character, name: str, entry_command: str, allowed_states: list[str], help_message: str):
        super().__init__(char, name, entry_command, allowed_states, help_message)
        self.commands = {"LIS": {"func": self.show_spells, "name": "List Spells"}, "SLO": {"func": self.show_slots, "name": "Show Spell Slots"}, "CAS": {"func": self.cast_spell, "name": "Cast Spell"}}

    def show_help(self, all_states) -> None:
        super().show_help(all_states)

    def show_spells(self) -> None:
        print("All spells:")
        # TODO: Flesh this out for Spell objects
        for spell in self.char.spells:
            print(f"\t{spell}")

    def show_slots(self) -> None:
        # TODO: Implement
        pass

    def cast_spell(self) -> None:
        # TODO: Implement
        # Want the input for this to be e.g. "CAS 2" to cast a level 2 spell
        # May want to put catches in here for specific spells e.g. free casts, ritual, etc.
        pass


def yaml_read(yaml_file: str, section: str) -> dict:
    """Safely read data from a .yaml file.

    Args:
        yaml_file (str): path to .yaml file
        section (str): section heading of .yaml file to read data of

    Returns:
        dict: .yaml file data
    """
    with open(yaml_file, "r") as stream:
        try:
            for data in safe_load_all(stream):
                if "section" in data and data["section"] == section:
                    return data["dict"]
        except YAMLError as e:
            raise SystemError(f"Error reading yaml file {e}")


def trim_input(usr_input: str) -> str:
    return usr_input.upper()[:3]


def transition_states(allowed_states: list[State], usr_input: str, current_state: State) -> State:
    """Transition to a new state if the user commands it. Otherwise 'transition' to the current state.

    Args:
        allowed_states (list[State]): subset of all states that we're allowed to transition to from our current state
        usr_input (str): user input in format 'XXX'
        current_state (State): the state we're currently in
    Returns:
        State: the new state to transition to, or our current state if the user input doesn't match any of our allowed commands
    """
    for state in allowed_states:
        if usr_input == state.entry_command:
            state.show_entry()
            return state
    # Return the current state if the user input doesn't match an allowed transition command
    return current_state


def main() -> None:
    my_char = Character(yaml_read("char_sheet.yaml", "Character"))
    states = {"main": Main_State(char=my_char, name="main", entry_command="MAI", allowed_states=["spells"], help_message=""),
              "spells": Spells_State(char=my_char, name="spells", entry_command="SPE", allowed_states=["main"], help_message="")}

    # Mainloop
    usr_input = ""
    state = states["main"]
    state.show_entry()
    while usr_input != "EXI":
        usr_input = trim_input(input(">>>"))
        if usr_input == "HEL":
            # The user needs help!
            state.show_help(states.values())
        state = transition_states(allowed_states=[states[name] for name in states.keys() if name in state.allowed_states],
                                  usr_input=usr_input,
                                  current_state=state)
        if usr_input in state.commands.keys():
            state.commands[usr_input]["func"]()


if __name__ == "__main__":
    main()
