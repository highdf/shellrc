#! /bin/python

import os
import subprocess
from typing import Any
from config_backup import log
from config_backup import handle_error


def prompt(repo: dict[str, Any], branch: str) -> None:
    print("The following repositories and branches are about to be operated")

    print("Repositories infomation")
    for repo_name, repo_path in repo.items():
        print(f"repository name : [{repo_name}]", end=" | ")
        print(f"repository path : [{repo_path}]")

    print("Branches name", end=" : ")
    for branch_name in branch:
        print(f"[{branch_name}]", end=" ")
    print()
    print("There will be a force push")


def confirm_operation(path: str) -> bool:
    re = True

    while True:
        response = input(f"===>Whether or no to push {path} [Y]es or [N]o: ").upper()
        if response in {"No", "N"}:
            re = False
            break
        elif response in {"Yes", "Y"}:
            break
    return re


def verification_repo(repo: dict[str, Any]) -> None:
    for repo_name, repo_path in repo.items():
        git_dir = os.path.join(repo_path, ".git")
        if not os.path.exists(repo_path):
            handle_error(f"Path {repo_path} is not exist")
        if not os.path.exists(git_dir):
            handle_error(f"Not exist .git in the {repo_path}")


def push_repository(repos: dict[str, Any], branch: str) -> None:
    operation = [
        ["git", "add", "."],
        ["git", "commit", "--amend", "--no-edit"],
        ["git", "push", "--force", "origin", branch],
    ]

    prompt = [
        "stage success...",
        "Commit success...",
        "Push success...",
    ]
    for repo_name, repo_path in repos.items():
        if not confirm_operation(repo_path):
            log(f"[[Jumped the repository -> {repo_path}]]")
            continue
        log(f"Starting push [{repo_name}]")
        os.chdir(repo_path)
        for cmd, message in zip(operation, prompt):
            try:
                subprocess.run(
                    cmd,
                    check=True,
                    timeout=40,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
            except subprocess.CalledProcessError as e:
                handle_error(f"Git failed:\n{e.stderr}")
            except subprocess.TimeoutExpired:
                handle_error("TimeOut")
            except FileNotFoundError:
                handle_error("Git command is not found")
            print(message)
    log("[[Push repository complete]]")


def main() -> None:
    REPOS = {
            "Code": os.path.expanduser("~/Code/"),
            "Environments": os.path.expanduser("~/Environments/"),
            "Pictures": os.path.expanduser("~/Pictures/"),
            "nvim": os.path.expanduser("~/.config/nvim"),
            "NoteBook": os.path.expanduser("~/NoteBook/")
    }
    BRANCH = "main"

    verification_repo(REPOS)
    prompt(REPOS, BRANCH)
    push_repository(REPOS, BRANCH)


if __name__ == "__main__":
    main()
