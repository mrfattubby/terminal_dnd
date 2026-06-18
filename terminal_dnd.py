from yaml import safe_load_all, YAMLError


class Character():
    def __init__(config: dict) -> None:
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

def main() -> None:
    print(yaml_read("char_sheet.yaml", "Character"))


if __name__ == "__main__":
    main()