#! /bin/python3

import os
import sys
import subprocess
from datetime import datetime


def log(message: str) -> None:
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{current_time}]: {message}")


def handle_error(message: str) -> None:
    log(f"Error:{message}")
    sys.exit(1)


def rm_resource(path: str) -> None:
    try:
        subprocess.run(
                ["rm", "-rf", path],
                check=True,
                stderr=subprocess.PIPE,
                text=True,
        )
    except FileNotFoundError:
        handle_error("'rm' command is not found")
    except subprocess.CalledProcessError as e:
        handle_error(f"Fialed remove {path}:\nError details: {e.stderr}")


def copy_resource(source_path: str, target_path: str) -> None:
    try:
        subprocess.run(
                ["cp", "-r", source_path, target_path],
                check=True,
                stderr=subprocess.PIPE,
                text=True,
        )
    except FileNotFoundError:
        handle_error("'cp' command is not found")
    except subprocess.CalledProcessError as e:
        handle_error(f"Fialed backup {os.path.basename(source_path)}:\nError details: {e.stderr}")


def ispath_exist(path: str) -> None:
    if not os.path.exists(path):
        handle_error(f"{path} is not exist")


def clean_old_backup(target: str) -> None:
    log("Starting clean old backup")

    ispath_exist(target)

    for resource_name in os.listdir(target):
        resource_path = os.path.join(target, resource_name)
        rm_resource(resource_path)
        log(f"Successfully clean: {resource_name}")


def make_new_backup(source: list[str], target: str) -> None:
    log("Start make new backup")

    for resource_path in source:
        ispath_exist(resource_path)

        resource_name = os.path.basename(resource_path)
        target_path = os.path.join(target, resource_name)

        copy_resource(resource_path, target_path)
        log(f"Successfully backup: {resource_name}")


def main() -> None:
    TARGET_DIR = "/home/luky/Environments/Configs/Dynamic/"
    SOURCE = [
        "/home/luky/.zshrc",
        "/home/luky/.tmux.conf",
        "/home/luky/.config/kitty",
        "/home/luky/.config/yazi",
    ]

    log("Start update dynamic config")

    clean_old_backup(TARGET_DIR)

    make_new_backup(SOURCE, TARGET_DIR)


if __name__ == "__main__":
    main()
