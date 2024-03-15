##    parashell - a shell
##    Copyright (C) 2024 Oliver Nguyen
##
##    This program is free software: you can redistribute it and/or modify
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

import os
import platform
import sys

VERSION = "0.1.3"
DATE = "15 Mar 2024"

NOTICE = """Parashell Copyright (C) 2024 Oliver Nguyen
This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
This is free software, and you are welcome to redistribute it
under certain conditions; type `show c' for details."""

def info():
    print(f"Parashell {VERSION} ({DATE}) on {sys.platform}")
    print(f"Python:   {sys.version}")
    print(f"Platform: {platform.system()} {platform.release()} ({platform.platform()})")
    if platform.system() == "Windows":
        release, version, csd, ptype = platform.win32_ver()
        edition = platform.win32_edition()
        print(f"Windows:  {release} {edition} {csd} ({version}) {ptype}")
    elif platform.system() == "Darwin":
        release, versioninfo, machine = platform.mac_ver()
        print(f"macOS:    {release} on {machine}")

print(NOTICE)
print()
info()
print()
print("For cd, please enter full (absolute) path - not relative path.")
print("Type help for help.")
print()

while True:
    cd = os.getcwd()
    cmd = input(f"{cd}> ")
    if cmd.startswith("cd"):
        try:
            cl = cmd.split(" ", 1)
            os.chdir(cl[1])
        except IndexError:
            print("Error: 1 argument required for cd.")
        except FileNotFoundError:
            print("Error: Directory not found.")
        except NotADirectoryError:
            print("Error: Not a directory.")
    elif cmd == "help":
        print("Type any command you would normally type in your console/shell.")
        print("Type info for program info.")
    elif cmd == "show w":
        print("Refer to the GNU GPL, section 15 <https://www.gnu.org/licenses/>.")
    elif cmd == "show c":
        print("Refer to the GNU GPL, section 4-6 <https://www.gnu.org/licenses/>.")
    elif cmd == "info":
        info()
    elif cmd == "exit":
        break
    else:
        exit_code = os.system(cmd)
        if exit_code != 0:
            print(f"Fail (exit code {exit_code})")
        else:
            print(f"Success (exit code {exit_code})")

print("Goodbye")
