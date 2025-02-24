#!/bin/python

import os
import subprocess
from repo_clone import log
from repo_clone import handle_error


def clean_old_config(old_config_paths: dict[str, str]) -> None:
    log("Starting cleanup of old configuration files...")

    for file_anme, path in old_config_paths.items():
        if os.path.exists(path):
            log(f"Removeing old configure {file_anme}")
            rmpath(path)
        log(f"Successfully remove: {file_anme}")


def rmpath(path: str) -> None:
    try:
        if os.path.isdir(path):
            subprocess.run(
                ["rm", "-rf", path],
                check=True,
                stderr=subprocess.PIPE,
                text=True,
            )
        elif os.path.isfile(path):
            subprocess.run(
                ["rm", path],
                check=True,
                stderr=subprocess.PIPE,
                text=True,
            )
        else:
            handle_error(f"The {path} is exception")
    except FileNotFoundError:
        handle_error("'rm' command is not found")
    except subprocess.CalledProcessError as e:
        handle_error(f"Failed to remove {path}:\nError details: {e.stderr}")


def update_new_config(new_config_path: str, old_config_paths: dict[str, str]) -> None:
    if not os.path.exists(new_config_path):
        handle_error(f"The {new_config_path} is now exist")
    log("Initializing new configure...")

    for new_config_file_name in os.listdir(new_config_path):
        new_config_file_path = os.path.join(new_config_path, new_config_file_name)
        target_paht = old_config_paths[new_config_file_name]
        log(f"Initializing configure {new_config_file_name}")
        copypath(new_config_file_path, target_paht)
        log(f"Initializing successfully: {new_config_file_name}")


def copypath(source_path: str, target_path: str) -> None:
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
        handle_error(f"failded to Initializing {target_path}:\nError details: {e.stderr}")


def main() -> None:
    old_config_paths = {
        ".zshrc": "/home/luky/.zshrc",
        ".tmux.conf": "/home/luky/.tmux.conf",
        "kitty":  "/home/luky/.config/kitty",
        "yazi": "/home/luky/.config/yazi",
    }
    new_config_path = "/home/luky/Environments/Configs/Dynamic"

    clean_old_config(old_config_paths)
    update_new_config(new_config_path, old_config_paths)

if __name__ == "__main__":
    main()
