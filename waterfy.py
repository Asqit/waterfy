from json import load, JSONDecodeError, dump
from plyer import notification
from platform import system
from sched import scheduler
from time import time, sleep
import os


def get_config_path() -> str:
    """A function that returns path to config directory depending on OS"""

    result: str = ""

    if system() == "Windows":
        result = "C:\\ProgramData\\waterfy\\"
    else:
        result = str(os.getenv("HOME")) + "/.waterfy/"

    return result


def run_configure() -> None:
    try:
        with open(os.path.join(get_config_path(), "configure.py")) as f:
            exec(f.read())
    except:
        print("Failed to execute configure.py")


def load_configuration(file_path: str) -> dict | None:
    """
    A function that parses a JSON configuration file
    Arguments:
        file_path {str}: a path of the config file
    Returns:
        parsed config or None
    """

    assert isinstance(file_path, str), "Invalid parameter type, expected a string"

    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        print("No configuration file found, creating a new one")
        run_configure()

    try:
        with open(file=file_path, mode="r") as raw_file:
            parsed_json = load(raw_file)
    except FileNotFoundError:
        print("No configuration file was found, creating a new one")
        run_configure()
    except JSONDecodeError:
        print("failed to parse the JSON config")
    except Exception as e:
        print(f"Unknown exception occurred: {e}")
    else:
        return parsed_json


def get_notification_frequency() -> int:
    """simple function that returns frequency key from JSON config"""
    config = load_configuration(get_config_path() + "waterfy.json")

    if config == None:
        raise Exception("Failed to load configuration")
    else:
        return config.get("frequency")


EVENT_SCHEDULER = scheduler(time, sleep)
NOTIFICATION_FREQUENCY = get_notification_frequency() * 60


def push_notification() -> None:
    """Actual function that calls the plyer API for notification"""
    notification.notify(
        app_name="Waterfy",
        app_icon=os.path.join(get_config_path(), "assets", "icon.ico"),
        title="Waterfy",
        message="It is time to drink some water",
        timeout=2,
    )
    EVENT_SCHEDULER.enter(NOTIFICATION_FREQUENCY, 1, push_notification)


def init() -> None:
    """Entry point of our app"""
    EVENT_SCHEDULER.enter(1, 1, push_notification)
    EVENT_SCHEDULER.run()


if __name__ == "__main__":
    init()
