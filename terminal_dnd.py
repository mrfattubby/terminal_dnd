from yaml import safe_load_all, YAMLError


class State():
    def __init__(self, name: str, command: str, allowed_states: list[str]) -> None:
        self.name = name
        self.command = command
        self.allowed_states = allowed_states


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
        self.speed = config["Speed"]
        self.prof_bonus = config["Proficiency Bonus"]
        self.attributes = config["Attributes"]


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
        if usr_input == state.command:
            return state
    # Return the current state if the user input doesn't match an allowed transition command
    return current_state


def main() -> None:
    my_char = Character(yaml_read("char_sheet.yaml", "Character"))
    states = {"main": State("main", "BAC", ["spells"]),
              "spells": State("spells", "SPE", ["main"])}

    # Mainloop
    usr_input = ""
    state = states["main"]
    while usr_input != "EXI":
        usr_input = trim_input(input(">>>"))
        state = transition_states(allowed_states=[states[name] for name in states.keys() if name in state.allowed_states],
                                  usr_input=usr_input,
                                  current_state=state)
        print(state.name)


if __name__ == "__main__":
    main()