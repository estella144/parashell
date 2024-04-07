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

def _get_current_commit_hash() -> str:
    return str(subprocess.check_output(['git', 'rev-parse', 'HEAD']), 'utf-8')

def _get_current_branch() -> str:
    current_branch = str(subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']), 'utf-8')
    current_branch = current_branch.strip()
    if current_branch == "HEAD":
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

def gitui_workmenu() -> None:
    raise NotImplementedError

def gitui_revmenu() -> None:
    raise NotImplementedError

def gitui_branchmenu() -> None:
    raise NotImplementedError

def gitui_collabmenu() -> None:
    raise NotImplementedError

def gitui_mainmenu() -> None:
    columns, lines = shutil.get_terminal_size()
    top_divider_msg = f"[Parashell GitUI {VERSION}]"
    top2_divider_msg = f"[Warning: {DEV_STATE} version. Bugs may be present.]"

    print(f"{top_divider_msg:=^{columns}}")
    print(f"{top2_divider_msg:-^{columns}}")
    print(_get_git_status())
    print('='*columns)
    print(_get_git_log(6))
    print('='*columns)

    print("Select an option below:")
    print("[W] - Work")
    print("[R] - Revisions")
    print("[B] - Branches and Tags")
    print("[C] - Collaborate")
    print("[Q] - Quit")

    while True:
        choice = input(f"{_get_current_branch()}> ").lower()
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
            break
        else:
            print("Error: Invalid choice")

if __name__ == "__main__":
    gitui_mainmenu()
