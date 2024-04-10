"""Git interface for ParaShell"""

##    parashell.gitinter - Git interface for ParaShell
##    Copyright (C) 2024 Oliver Nguyen
##
##    This file is part of ParaShell.
##
##    ParaShell is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    ParaShell is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import shutil
import subprocess

VERSION = "0.3.1.dev1"
COMMIT = "aaab602"
DATE = "07 Apr 2024"
DEV_STATE_SHORT = ""
DEV_STATE = "development"

def _git_exists() -> bool:
    return (shutil.which("git") != None)

def _head_detached() -> bool:
    try:
        subprocess.check_output(['git', 'symbolic-ref', '--quiet', 'HEAD'])
        return False
    except subprocess.CalledProcessError:
        return True

def _get_current_repo_name() -> str:
    current_repo_path = str(subprocess.check_output(['git', 'rev-parse', '--show-toplevel']), 'utf-8')
    return current_repo_path.split(sep="/")[-1].strip()

def _get_current_commit_hash() -> str:
    return str(subprocess.check_output(['git', 'rev-parse', 'HEAD']), 'utf-8')

def _get_current_branch() -> str:
    current_branch = str(subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']), 'utf-8')
    current_branch = current_branch.strip()
    if _head_detached():
        hash = _get_current_commit_hash()
        hash_abbrev = hash[0:6]
        return(f"detached at {hash_abbrev}")
    return current_branch

def _get_git_status() -> str:
    return str(subprocess.check_output(['git', 'status']), 'utf-8')

def _get_git_log(num_commits: int) -> str:
    n_flag = '-n' + str(num_commits)
    pretty_flag = '--pretty=format:%h | %ar | %s'
    return str(subprocess.check_output(['git', 'log', pretty_flag, n_flag]), 'utf-8')

def gitui_addmenu() -> None:
    path = input("Please enter a pathspec to add to staged changes: ")
    try:
        subprocess.run(['git', 'add', path], check=True)
        print(f"Successfully added {path}")
    except subprocess.CalledProcessError as err:
        print(f"Failed to add {path}: {err}")

def gitui_movemenu() -> None:
    raise NotImplementedError

def gitui_restoremenu() -> None:
    raise NotImplementedError

def gitui_removemenu() -> None:
    raise NotImplementedError

def gitui_commitmenu() -> None:
    raise NotImplementedError

def gitui_workmenu() -> None:
    gitui_printpage()

    print("Select an option below:")
    print("[A] - Add")
    print("[M] - Move")
    print("[R] - Restore")
    print("[V] - Remove")
    print("[C] - Commit")
    print("[B] - Back to main menu")
    print("[Ctrl-C] - Quit")

    while True:
        choice = input(f"{_get_current_repo_name()} on {_get_current_branch()}> ").lower()
        if choice == "a":
            gitui_addmenu()
        elif choice == "m":
            gitui_movemenu()
        elif choice == "r":
            gitui_restoremenu()
        elif choice == "c":
            gitui_commitmenu()
        elif choice == "b":
            break
        elif choice == "q":
            quit()
        

def gitui_revmenu() -> None:
    raise NotImplementedError

def gitui_branchmenu() -> None:
    raise NotImplementedError

def gitui_collabmenu() -> None:
    raise NotImplementedError

def gitui_printpage() -> None:
    columns, lines = shutil.get_terminal_size()
    repo_name = _get_current_repo_name()
    branch = _get_current_branch()
    top_divider_msg = f"[Parashell GitUI {VERSION} - {repo_name} on {branch}]"
    top2_divider_msg = f"[Warning: {DEV_STATE} version. Bugs may be present.]"

    print(f"{top_divider_msg:=^{columns}}")
    print(f"{top2_divider_msg:-^{columns}}")
    print(_get_git_status())
    print('='*columns)
    print(_get_git_log(6))
    print('='*columns)

def gitui_mainmenu() -> None:
    gitui_printpage()

    print("Select an option below:")
    print("[W] - Work")
    print("[R] - Revisions")
    print("[B] - Branches and Tags")
    print("[C] - Collaborate")
    print("[Ctrl-C] - Quit")

    while True:
        choice = input(f"{_get_current_repo_name()} on {_get_current_branch()}> ").lower()
        if choice == "w":
            gitui_workmenu()
        elif choice == "r":
            gitui_revmenu()
        elif choice == "b":
            gitui_branchmenu()
        elif choice == "c":
            gitui_collabmenu()
        elif choice == "q":
            print("Leaving Parashell GitUI...")
            quit()
        else:
            print("Error: Invalid choice")

if __name__ == "__main__":
    if _git_exists():
        gitui_mainmenu()
    else:
        print("Error: Git not installed. Please install Git to continue.")
