from json import load, JSONDecodeError, dump
from plyer import notification
from platform import system
from sched import scheduler
from time import time, sleep
import os


def get_config_path() -> str:
    result: str = ""

    if system() == "Windows":
        result = "C:\\ProgramData\\waterfy\\"
    else:
        result = str(os.getenv("HOME")) + "/.waterfy/"

    return result


def get_corrected_minutes() -> int:
    while True:
        minutes = int(input("Enter amount of minutes between reminders: "))

        if minutes <= 0:
            print("Invalid value, please try again")
            continue

        return minutes


def create_configuration() -> None:
    minutes = get_corrected_minutes()
    path = get_config_path()

    if not os.path.exists(path):
        os.makedirs(path)

    data = {"frequency": minutes}

    try:
        with open(file=path + "waterfy.json", mode="w") as cfg:
            dump(data, cfg, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        print("Failed to write to a file")
    except Exception as e:
        print(f"An error occurred: {e}")
    else:
        return


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
        create_configuration()
        return

    try:
        with open(file=file_path, mode="r") as raw_file:
            parsed_json = load(raw_file)
    except FileNotFoundError:
        print("No configuration file was found, creating a new one")
        create_configuration()
    except JSONDecodeError:
        print("failed to parse the JSON config")
    except Exception as e:
        print(f"Unknown exception occurred: {e}")
    else:
        return parsed_json


def get_notification_frequency() -> int:
    config = load_configuration(get_config_path() + "waterfy.json")

    if config == None:
        raise Exception("Failed to load configuration")
    else:
        return config.get("frequency")


EVENT_SCHEDULER = scheduler(time, sleep)
NOTIFICATION_FREQUENCY = get_notification_frequency() * 60


def push_notification() -> None:
    notification.notify(
        app_name="Waterfy",
        app_icon=os.getcwd() + "\\assets\icon.ico",
        title="Waterfy",
        message="It is time to drink some water",
        timeout=2,
    )
    EVENT_SCHEDULER.enter(NOTIFICATION_FREQUENCY, 1, push_notification)


def init() -> None:
    EVENT_SCHEDULER.enter(1, 1, push_notification)
    EVENT_SCHEDULER.run()


if __name__ == "__main__":
    init()
