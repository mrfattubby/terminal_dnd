from yaml import safe_load_all, YAMLError


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

def main() -> None:
    my_char = Character(yaml_read("char_sheet.yaml", "Character"))
    print(my_char)
    print(my_char.name)
    print(my_char.attributes)


if __name__ == "__main__":
    main()