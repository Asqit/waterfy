from configure import run_configure, get_config_path
from platform import system
import shutil
import os


START_UP_PATH = os.path.join(
    os.path.expanduser(
        "~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
    ),
    "waterfy.bat",
)


def copy_to_startup():
    if system() == "Windows":
        try:
            shutil.copyfile(
                os.path.join(os.getcwd(), "assets", "waterfy.bat"),
                START_UP_PATH,
            )
        except Exception as e:
            print(f"An error occurred {e}")
    else:
        pass


def copy_configure_to_config_dir():
    try:
        shutil.copyfile(
            os.path.join(os.getcwd(), "configure.py"),
            os.path.join(get_config_path(), "configure.py"),
        )
        shutil.copyfile(
            os.path.join(os.getcwd(), "install.py"),
            os.path.join(get_config_path(), "install.py"),
        )
    except:
        print("Failed to copy configure.py to config directory")


if __name__ == "__main__":
    copy_to_startup()
    run_configure()
    copy_configure_to_config_dir()
