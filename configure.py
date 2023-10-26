from json import dump
from platform import system
import shutil
import os


def get_config_path() -> str:
    """A function that returns path to config directory depending on OS"""

    result: str = ""

    if system() == "Windows":
        result = "C:\\ProgramData\\waterfy\\"
    else:
        result = str(os.getenv("HOME")) + "/.waterfy/"

    return result


def get_corrected_minutes() -> int:
    """A function that returns only positive minutes (valid)"""
    while (value := int(input("Minutes between reminders?: "))) <= 0:
        print(f"Invalid value: {value}, please try again")
    else:
        return value


def move_assets() -> None:
    """A function that will move assets to config directory"""
    source = os.path.join(os.getcwd(), "assets")
    destination = os.path.join(get_config_path(), "assets")

    shutil.copytree(src=source, dst=destination)


def create_configuration() -> None:
    """A function responsible for creating configuration & it's directory"""
    minutes = get_corrected_minutes()
    path = get_config_path()

    if not os.path.exists(path):
        os.makedirs(path)

    data = {"frequency": minutes}

    try:
        move_assets()
    except Exception:
        exit(1)

    # Try creating the JSON config
    try:
        with open(file=path + "waterfy.json", mode="w") as cfg:
            dump(data, cfg, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        print("Failed to write to a file")
    except Exception as e:
        print(f"An error occurred: {e}")
    else:
        return


def run_configure():
    print("Running configure")
    config_path = get_config_path()
    if not os.path.exists(config_path):
        os.makedirs(config_path)
        create_configuration()


if __name__ == "__main__":
    run_configure()
