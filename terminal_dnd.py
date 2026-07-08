from yaml import safe_load, YAMLError


TOTAL_WIDTH = 76  # Half of my laptop screen
LINE_SEP = TOTAL_WIDTH * "*"
CONFIG_PATH = "char_sheet.yaml"
EMPTY_CIRCLE = "\u25ef"
FILLED_CIRCLE = "\u2b24"

# TODO: Split spells into a separate module
class Spell():
    def __init__(self, name: str, level: int, cast_time: str, range: str, duration: str, components: str, description: str, prepared: bool = True, concentration: bool = False, ritual: bool = False, free_casts: int = 0, wild_shape: bool = False) -> None:
        # TODO: Finish setting up later
        pass


class Character():
    def __init__(self, config: dict) -> None:
        self.load_char(config)

    def load_char(self, config: dict) -> None:
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
        self.saving_throws = config["Saving Throws"]
        self.skills = config["Skills"]
        self.max_hp = config["HP"]["Maximum HP"]
        self.current_hp = config["HP"]["Current HP"]
        self.temp_hp = config["HP"]["Temporary HP"]
        self.death_saves = config["HP"]["Death Saves"]
        self.hit_dice = config["HP"]["Hit Dice"]
        self.attacks = config["Attacks"]
        self.spell_slots = config["Spell Slots"]
        self.spells = config["Spells"]  # TODO: Convert spell names into Spell objects
        self.abilities = config["Abilities"]


class State():
    def __init__(self, char: Character, name: str, entry_command: str, allowed_states: list[str], help_message: str) -> None:
        self.char = char
        self.name = name
        self.entry_command = entry_command
        self.allowed_states = allowed_states
        self.help_message = help_message
        self.commands = {"REL": {"func": self.reload_char, "name": "Reload Character"}}

    def show_entry(self) -> None:
        print(LINE_SEP)
        print(f"{self.name.title()} Screen")
        print(LINE_SEP)

    def show_help(self, all_states: list) -> None:
        print(LINE_SEP)
        print(f"{self.name.title()} Screen\n")

        print("Commands:")
        for command in self.commands.keys():
            print(f"\t{command}\t{self.commands[command]['name']}")

        print()
        for state in all_states:
            if state.name in self.allowed_states:
                print(f"\t{state.entry_command}\t{state.name.title()} Screen")

        print("\tEXI\tExit terminal")
        print(LINE_SEP)

    def reload_char(self) -> None:
        self.char.load_char(yaml_read(CONFIG_PATH))
        print(f'Reloaded character from "{CONFIG_PATH}"')
        self.show_entry()

class Main_State(State):
    def __init__(self, char: Character, name: str, entry_command: str, allowed_states: list[str], help_message: str) -> None:
        super().__init__(char, name, entry_command, allowed_states, help_message)
        self.commands.update({"ACC": {"func": self.show_ac, "name": "Show AC"},
                              "MOV": {"func": self.show_movement, "name": "Show Movement Speed"}})  # TODO: Extend

    def show_entry(self) -> None:
        super().show_entry()
        print(f"{self.char.name}")
        print(f"Level:\t\t{self.char.level}")
        print(f"Class:\t\t{self.char.char_class} - {self.char.subclass}")
        print(f"Species:\t{self.char.species} - {self.char.subspecies}")
        print(f"Background:\t{self.char.background}")
        print(f"Alignment:\t{self.char.alignment}")
        print(LINE_SEP)
        print("Attributes:")
        for attribute in self.char.attributes:
            print(f"   {attribute["name"]}\t\t{attribute["mod"]:>2}\t({attribute["val"]:>2})\t{attribute["notes"]}")  # 3 space offset to line up with saving throws and skills
        print(LINE_SEP)
        print("Skills:")
        for skill in self.char.skills:
            print(f"{FILLED_CIRCLE if skill["expert"] else " "}{FILLED_CIRCLE if skill["prof"] else EMPTY_CIRCLE} {skill["name"]:<12}\t{skill["mod"]:>2}\t{skill["attribute"]}\t{skill["notes"]}")
        print(LINE_SEP)

    def show_ac(self) -> None:
        print(f"AC = {self.char.ac}")

    def show_movement(self) -> None:
        print(f"Speed = {self.char.speed}")


class Spells_State(State):
    def __init__(self, char: Character, name: str, entry_command: str, allowed_states: list[str], help_message: str) -> None:
        super().__init__(char, name, entry_command, allowed_states, help_message)
        self.commands.update({"LIS": {"func": self.show_spells, "name": "List Spells"},
                              "CAS": {"func": self.cast_spell, "name": "Cast Spell"}})

    def show_entry(self) -> None:
        super().show_entry()
        print_spell_slots(self.char)
        print(LINE_SEP)

    def show_help(self, all_states) -> None:
        super().show_help(all_states)

    def show_spells(self) -> None:
        print("All spells:")
        # TODO: Flesh this out for Spell objects
        for spell in self.char.spells:
            print(f"\t{spell}")

    def cast_spell(self) -> None:
        # TODO: Implement
        # Want the input for this to be e.g. "CAS 2" to cast a level 2 spell
        # May want to put catches in here for specific spells e.g. free casts, ritual, etc.
        pass


class Combat_State(State):
    # TODO: Add. E.g. HP, "quick" attacks like on char sheet.
    def __init__(self, char: Character, name: str, entry_command: str, allowed_states: list[str], help_message: str) -> None:
        super().__init__(char, name, entry_command, allowed_states, help_message)
        self.commands.update({"HIT": {"func": self.modify_hp, "name": "Modify HP"}})

    def show_entry(self) -> None:
        super().show_entry()
        print(f"AC:\t\t{self.char.ac}")
        print(f"Initiative:\t{self.char.initiative}")
        print(f"Speed:\t\t{self.char.speed}")
        print(LINE_SEP)
        print_hp(self.char)
        print(LINE_SEP)
        print("Death Saves")
        num_successes, num_failures = [int(x) for x in self.char.death_saves.split("/")]
        print(f"Successes:\t{num_successes * FILLED_CIRCLE + (3 - num_successes) * EMPTY_CIRCLE}")
        print(f"Failures:\t{num_failures * FILLED_CIRCLE + (3 - num_failures) * EMPTY_CIRCLE}")
        print(LINE_SEP)
        print("Saving Throws")
        for save in self.char.saving_throws:
            print(f" {FILLED_CIRCLE if save["prof"] else EMPTY_CIRCLE} {save["name"]}\t\t{save["mod"]}\t\t{save["notes"]}")  # Two spaces after circle to align with skills due to expertise
        print(LINE_SEP)
        print("Quick Attack Reference")
        print("Name\t\tAtt.\tDamage\t\tRange\tNotes")
        for attack in self.char.attacks:
            print(f"{attack['name']:<15}\t{attack['att']:<7}\t{attack['dam']:<15}\t{attack['range']:<7}\t{attack['notes']}")  # TODO: Fix Notes wrapping onto new line at start of line: keep wrapping in line with Notes column
        print(LINE_SEP)

    def show_help(self, all_states) -> None:
        super().show_help(all_states)

    def modify_hp(self):
        pass


class Abilities_State(State):
    def __init__(self, char: Character, name: str, entry_command: str, allowed_states: list[str], help_message: str) -> None:
        super().__init__(char, name, entry_command, allowed_states, help_message)
    
    def show_entry(self):
        super().show_entry()
        print("Name\t\tUses\tRecover Uses\t\tNotes")
        for ability in self.char.abilities:
            print(f"{helper_print_ability_uses(ability)}\t{ability['notes']}")  # TODO: Fix Notes wrapping onto new line at start of line: keep wrapping in line with Notes column
        print(LINE_SEP)


class Rest_State(State):
    def __init__(self, char: Character, name: str, entry_command: str, allowed_states: list[str], help_message: str) -> None:
        super().__init__(char, name, entry_command, allowed_states, help_message)
    
    def show_entry(self):
        super().show_entry()
        print_hp(self.char)
        try:
            num, die = self.char.hit_dice.split(" ")
            used, total = [int(x) for x in num.split("/")]
            to_print = f"{used * FILLED_CIRCLE + (total - used) * EMPTY_CIRCLE:<7}\t{die}"
        except (TypeError, ValueError) as e:
            to_print = f"!!{num:<5}\t{die}"  # Cut off at 5 since we add two exclamation marks (total of 7 chars)
        print(f"Hit Dice:\t{to_print}")
        print(LINE_SEP)
        print_spell_slots(self.char)
        print(LINE_SEP)
        print("Abilities")
        print("Name\t\tUses\tRecover Uses")
        for ability in self.char.abilities:
            if "SR" in ability["recover_uses"] or "LR" in ability["recover_uses"]:
                print(f"{helper_print_ability_uses(ability)}\t{ability['notes']}")  # TODO: Fix Notes wrapping onto new line at start of line: keep wrapping in line with Notes column
        print(LINE_SEP)


def print_hp(char: Character) -> None:
    print("Hit Points")
    try:
        print(f"|{int(char.current_hp) * "="}{int(char.temp_hp) * "+"}{(int(char.max_hp) - int(char.current_hp)) * "-"}|")
    except (TypeError, ValueError) as e:
        print("!!Error printing HP bar, make sure all HP values are integers.")
    print(f"Maximum HP:\t{char.max_hp}")
    print(f"Current HP:\t{char.current_hp}")
    print(f"Temporary HP:\t{char.temp_hp}")


def print_spell_slots(char: Character) -> None:
    print("Spell Slots:")
    for level, slots in char.spell_slots.items():
        used, total = [int(x) for x in slots.split("/")]
        print(f"{level}:\t{used * FILLED_CIRCLE + (total - used) * EMPTY_CIRCLE}")


def helper_print_ability_uses(ability: dict) -> str:
    to_print = f"{ability['name']:<15}\t"
    if ability["uses"]:
        try:
            used, total = [int(x) for x in ability["uses"].split("/")]
            to_print += f"{used * FILLED_CIRCLE + (total - used) * EMPTY_CIRCLE:<7}\t"
        except (TypeError, ValueError) as e:
            to_print += f"!!{ability["uses"][:5]:<5}\t"  # Cut off at 5 since we add two exclamation marks (total of 7 chars)
    else:
        to_print += f"{"":<7}\t"
    return to_print + f"{ability['recover_uses']:<22}"

def yaml_read(yaml_file: str) -> dict:
    """Safely read data from a .yaml file.

    Args:
        yaml_file (str): path to .yaml file

    Returns:
        dict: .yaml file data
    """
    with open(yaml_file, "r") as stream:
        try:
            return safe_load(stream)
        except YAMLError as e:
            raise SystemError(f"Error reading yaml file {e}")


def yaml_write(yaml_file: str, label: str, value: str | int) -> None:
    new_lines = []
    with open(yaml_file, "r") as stream:
        lines = stream.readlines()
        for i in range(len(lines)):
            try:
                if label in lines[i].split(":")[0]:  # Use in (not ==) due to indentation in yaml file
                    lines[i] = ":".join([lines[i].split(":")[0], f' "{value}"\n'])  # Use .join to preserve indentation
            except IndexError:
                # Line doesn't have a label, skip
                continue
        new_lines = lines
    
    with open(yaml_file, "w") as stream:
        stream.writelines(new_lines)


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
    my_char = Character(yaml_read(CONFIG_PATH))
    states = [Main_State(char=my_char, name="main", entry_command="MAI", allowed_states=["spells", "combat", "abilities", "rest"], help_message=""),
              Spells_State(char=my_char, name="spells", entry_command="SPE", allowed_states=["main", "combat", "abilities", "rest"], help_message=""),
              Combat_State(char=my_char, name="combat", entry_command="COM", allowed_states=["main", "spells", "abilities", "rest"], help_message=""),
              Abilities_State(char=my_char, name="abilities", entry_command="ABI", allowed_states=["main", "spells", "combat", "rest"], help_message=""),
              Rest_State(char=my_char, name="rest", entry_command="RES", allowed_states=["main", "spells", "combat", "abilities"], help_message="")]

    # Mainloop
    usr_input = ""
    state = states[0]
    state.show_entry()
    while usr_input != "EXI":
        usr_input = trim_input(input(">>>"))
        if usr_input == "HEL":
            # The user needs help!
            state.show_help(states)
        state = transition_states(allowed_states=[x for x in states if x.name in state.allowed_states],
                                  usr_input=usr_input,
                                  current_state=state)
        if usr_input in state.commands.keys():
            state.commands[usr_input]["func"]()


if __name__ == "__main__":
    main()
