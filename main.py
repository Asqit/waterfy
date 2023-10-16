import sched
import time
import json
import os
from plyer import notification


def read_config(file_path: str) -> str:
    """
    A function that parses a JSON config file

    Arguments:
        file_path: a string containing a path of the config file
    Returns:
        the parsed configuration file or None
    """

    assert type(file_path) == str, f"Invalid parameter type."

    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("Config file was not found")
    except json.JSONDecodeError:
        print("Failed to parse the JSON config")
    return None


def get_notification_frequency() -> int:
    """
    A function that retrieves a frequency of each notification
    Returns:
        a frequency of each notification
    """

    APP_DATA_PATH = os.getenv("TEMP")
    CONFIG_PATH = os.path.join(APP_DATA_PATH, "waterfy.json")

    config = read_config(CONFIG_PATH)

    if config == None:
        raise Exception("Failed to load config file")

    return config["waterfy_frequency"]


HOUR_IN_SECS = 3600
WATERFY_DELAY = HOUR_IN_SECS * get_notification_frequency()
EVENT_SCHEDULE = sched.scheduler(time.time, time.sleep)


def notify() -> None:
    """A function that pushes notification"""

    notification.notify(
        title="Waterfy", message="It is time to drink some water", timeout=2
    )
    EVENT_SCHEDULE.enter(WATERFY_DELAY, 1, notify)


def init() -> None:
    """A function that starts the program"""
    EVENT_SCHEDULE.enter(1, 1, notify)
    EVENT_SCHEDULE.run()


if __name__ == "__main__":
    init()
