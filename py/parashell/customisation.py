"""Customisation functions for ParaShell"""

##    parashell.customisation - customisation for Parashell
##    Copyright (C) 2024 Oliver Nguyen
##
##    This file is part of ParaShell.
##
##    ParaShell is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import configparser
import os

import parashell.utils as utils

def get_shell_path(shell_name) -> str:
    return shutil.which(shell_name)

def get_best_shell() -> str:
    '''Get the best shell for the current machine.'''
    if platform.system() == 'Windows':
        return "C:\\Windows\\System32\\cmd.exe"
    else:
        if shell_exists("zsh"):
            print("zsh found")
            return get_shell_path("zsh")
        elif shell_exists("bash"):
            print("bash found")
            return get_shell_path("bash")
        else:
            print("zsh and bash not found, defaulting to sh")
            return get_shell_path("sh")

def get_shell_choice() -> str:
    windows_shells = [("cmd", "C:\\Windows\\System32\\cmd.exe"),
                      ("powershell", "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe")]
    shells = [("zsh", "/bin/zsh"),
              ("bash", "/bin/bash"),
              ("sh", "/bin/sh")]

    if platform.system() == "Windows":
        i = 1
        print(f"0. Best shell ({get_best_shell()})")
        for shell in windows_shells:
            print(f"{i}. {shell[0]} ({shell[1]})")
            i += 1
        shell_number = int(input("Enter shell number: "))
        if shell_number == 0:
            return get_best_shell()
        else:
            return windows_shells[shell_number-1][1]
    else:
        i = 1
        print(f"0. Best shell ({get_best_shell()})")
        for shell in shells:
            print(f"{i}. {shell[0]} ({shell[1]})")
            i += 1
        shell_number = int(input("Enter shell number: "))
        if shell_number == 0:
            return get_best_shell()
        else:
            return shells[shell_number-1][1]

def apply_customisation(parashell_dir) -> dict:
    """Gets custom prompt and custom shell, returning dict."""
    cwd = os.getcwd()
    prompt_format = get_custom_prompt(parashell_dir)
    shell = get_custom_shell(parashell_dir)
    return {"prompt_format": prompt_format, "shell": shell}

def get_custom_prompt(parashell_dir) -> str:
    '''Reads custom prompt from config file and returns it as a string.'''
    config = configparser.ConfigParser()
    config.read(os.path.join(parashell_dir, "config.ini"))
    try:
        return config["Prompt"]["PromptFormat"]
    except KeyError:
        print("Error: Prompt key not found. Your config.ini may be out of date.")
        print("       Delete your config.ini file and restart ParaShell.")
        return "[{shell}] {username}@{hostname}:{cwd}"

def get_custom_shell(parashell_dir) -> str:
    '''Reads custom shell from config file and returns it as a string'''
    config = configparser.ConfigParser()
    config.read(os.path.join(parashell_dir, "config.ini"))
    try:
        return config["Shell"]["Shell"]
    except KeyError:
        print("Error: Shell key not found. Your config.ini may be out of date.")
        print("       Delete your config.ini file and restart ParaShell.")
        return utils.get_shell_choice()

if __name__ == "__main__":
    print("This file is not intended to be run directly!")
    print("Please run parashell.py to run the main program.")
    input("[Enter] - Quit")
    quit()
