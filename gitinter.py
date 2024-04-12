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

import platform
import shutil
import subprocess

VERSION = "0.3.1.dev1"
COMMIT = "550c7da"
DATE = "10 Apr 2024"
DEV_STATE_SHORT = ""
DEV_STATE = "development"

def _execute_command(cmd, echo_result=True) -> int:
    '''Executes a command in the computer's shell.
    cmd: str - command to run'''
    try:
        subprocess.run(cmd, shell=True, check=True)
        if echo_result:
            print(f"Success: {cmd}")
            return 0
    except subprocess.CalledProcessError as e:
        print(f"Failed executing command: {cmd} (return code {e.returncode})")
        return e.returncode
    finally:
        echo_result = True

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

def _git_push():
    try:
        subprocess.run(['git', 'push'], check=True)
        print("Successfully pushed to remote")
    except subprocess.CalledProcessError as err:
        print(f"Failed to push to remote: {err}")

def _clear_screen() -> None:
    '''Clears the screen.'''
    if platform.system() == "Windows":
        _execute_command("cls", echo_result=False)
    else:
        # macOS or Linux
        _execute_command("clear", echo_result=False)

def gitui_addmenu() -> None:
    path = input("Pathspec to add to staged changes: ")
    try:
        subprocess.run(['git', 'add', path], check=True)
        print(f"Successfully added {path}")
    except subprocess.CalledProcessError as err:
        print(f"Failed to add {path}: {err}")

def gitui_movemenu() -> None:
    source = input("Source file to move: ")
    destination = input("Destination directory or path: ")
    try:
        subprocess.run(['git', 'move', source, destination], check=True)
        print(f"Successfully moved {source} to {destination}")
    except subprocess.CalledProcessError as err:
        print(f"Failed to move {source} to {destination}: {err}")

def gitui_restoremenu() -> None:
    print("Select an option below:")
    print("[U] - Unstage")
    print("[R] - Restore")
    print("[C] - Restore from Commit")
    print("[D] - Discard Untracked Files")

    while True:
        choice = input(f"[restore] {_get_current_repo_name()} on {_get_current_branch()}> ").lower()
        if choice == "u":
            path = input("Pathspec to unstage changes to: ")
            try:
                subprocess.run(["git", "restore", "--staged", path], check=True)
                print(f"Successfully unstaged changes to {path}")
            except subprocess.CalledProcessError as err:
                print(f"Failed to unstage changes to {path}: {err}")
        elif choice == "r":
            path = input("Pathspec to restore to last commit: ")
            try:
                subprocess.run(["git", "restore", path], check=True)
                print(f"Successfully restored {path}")
            except subprocess.CalledProcessError as err:
                print(f"Failed to restore {path}: {err}")
        elif choice == "c":
            path = input("Pathspec to restore: ")
            print("Hint: Type HEAD~# to reference a commit relatively.")
            print("hint: This means # commits ago (from HEAD).")
            commit = input("Commit to restore file from: ")
            source_flag = f"--source={commit}"
            try:
                subprocess.run(["git", "restore", "--staged", path], check=True)
                print(f"Successfully unstaged changes to {path}")
            except subprocess.CalledProcessError as err:
                print(f"Failed to unstage changes to {path}: {err}")
        elif choice == "d":
            try:
                subprocess.run(["git", "restore", "--source=HEAD", "--staged", "."], check=True)
                print(f"Successfully unstaged changes to {path}")
            except subprocess.CalledProcessError as err:
                print(f"Failed to unstage changes to {path}: {err}")
        else:
            print("Nothing chosen, nothing restored")

def gitui_removemenu() -> None:
    path = input("File(s) to remove: ")
    try:
        subprocess.run(['git', 'rm', path], check=True)
        print(f"Successfully removed {path}")
    except subprocess.CalledProcessError as err:
        print(f"Failed to remove {path}: {err}")

def gitui_commitmenu() -> None:
    print(_get_git_status())
    check = input("Are you sure you want to commit all staged changes? [y/n] ")
    if check.lower() == "y":
        message = input("Commit message: ")
        try:
            subprocess.run(['git', 'commit', '-m', message], check=True)
            print("Successfully committed changes")
            push = input("Push changes to remote? [y/n] ")
            if push.lower() == "y":
                _git_push()
        except subprocess.CalledProcessError as err:
            print(f"Failed to commit changes: {err}")

def gitui_workmenu() -> None:
    _clear_screen()
    gitui_printpage()

    print("Select an option below:")
    print("[A] - Add - Stage Changes")
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
            gitui_mainmenu()
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
    _clear_screen()
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
