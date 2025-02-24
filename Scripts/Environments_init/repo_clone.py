#! /bin/python

import os
import subprocess
import sys


def log(message: str) -> None:
    print(f"{message}")


def handle_error(message: str) -> None:
    log(f"Error: {message}")
    sys.exit(1)


def ispath_exist(path: str) -> bool:
    return os.path.exists(path) and os.path.isdir(path)


def verification(target_path: list[str]) -> None:
    for path in target_path:
        if ispath_exist(path):
            handle_error(f"Path already exist: {path}")


def prompty(source: list[str], target_path: list[str]) -> None:
    log("Repository to be cloned")
    for urls, path in zip(source, target_path):
        log(f"Repository URL: {urls} clone --> {path}")


def confirm_operation(repo_url: str, path: str) -> bool:
    re = True

    while True:
        response = input(f"===>Whether or not clone {repo_url} [Y]es or [N]o: ").upper()
        if response in ("Y", "YES"):
            break
        elif response in ("N", "NO"):
            re = False
            break
    return re


def repo_clone(source: list[str], target_path: list[str]) -> None:
    for repo_url, path in zip(source, target_path):
        if not confirm_operation(repo_url, path):
            log(f"Jumping over the {repo_url}")
            continue
        cmd = ["git", "clone", repo_url, path]
        log(f"\n--------->[ Start clone repository {repo_url} ]<---------")
        log("Cloneing...")
        try:
            subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            log(f"Warning: Cloned is failed for {repo_url}\n{e.stderr}")
            continue
        except FileNotFoundError as e:
            handle_error(f"Git command is not exist:\n{e.stderr}")
        log(f"--------->[ {repo_url} is success ]<---------")


def main() -> None:
    SOURCE = [
        "git@github.com:highdf/Code.git",
        "git@github.com:highdf/nvim-configure.git",
        "git@github.com:highdf/Picture.git",
        "git@github.com:highdf/NoteBook.git"
        # "git@github.com:highdf/Environments.git"
    ]
    TARGET_PATH = [
        "/home/luky/Code",
        "/home/luky/.config/nvim",
        "/home/luky/Pictures/",
        "/home/luky/NoteBook/",
        # "/home/luky/Environments/",
    ]

    verification(TARGET_PATH)
    prompty(SOURCE, TARGET_PATH)
    repo_clone(SOURCE, TARGET_PATH)


if __name__ == "__main__":
    main()
