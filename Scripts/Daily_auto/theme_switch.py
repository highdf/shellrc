#! /bin/python

import os
import random
import subprocess
from datetime import datetime
from config_backup import log
from config_backup import handle_error
from config_backup import copy_resource


def ispath_exist(path: str) -> None:
    if not os.path.exists(path):
        handle_error(f"Not exist {path}")


def switch_kitty_theme() -> None:
    THEME_PATH = "/home/luky/.config/kitty/themes/"
    TARGET_FILE = "base.conf"
    THEME_GROUPS = [
        ["Catppuccin/latte.conf", "Catppuccin/macha.conf",],
        ["Tokyo_Night/day.conf", "Tokyo_Night/monn.conf",],
    ]
    DAY = int(os.getenv("DAY_START"))
    NIGHT = int(os.getenv("DAY_END"))
    current_time = datetime.now().hour

    theme = random.choice(THEME_GROUPS)
    target_path = os.path.join(THEME_PATH, TARGET_FILE)

    ispath_exist(THEME_PATH)
    log("Start switch kitty theme")

    if DAY <= current_time < NIGHT:
        theme_path = os.path.join(THEME_PATH, theme[0])
        ispath_exist(theme_path)
        log(f"Usage day theme: {theme[0]}")
    else:
        theme_path = os.path.join(THEME_PATH, theme[1])
        ispath_exist(theme_path)
        log(f"Usage night theme: {theme[1]}")

    copy_resource(theme_path, target_path)


def reload_kittyconfig() -> None:
    cmd = ["kitty", "@", "load-config"]

    log("Start reload kitty config")
    try:
        subprocess.run(cmd)
        subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
        )
        log("Successfully reload")
    except FileNotFoundError:
        handle_error("kitty command is not found")
    except subprocess.CalledProcessError as e:
        handle_error(f"Failed to configure reload:\nError details:{e.stderr}")


def main() -> None:
    switch_kitty_theme()
    reload_kittyconfig()


if __name__ == "__main__":
    main()
