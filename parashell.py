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

VERSION = "0.1.1"
DATE = "13 Mar 2024"

NOTICE = """Parashell Copyright (C) 2024 Oliver Nguyen
This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
This is free software, and you are welcome to redistribute it
under certain conditions; type `show c' for details."""

print(NOTICE)
print()
print(f"Parashell {VERSION} ({DATE}) on {sys.platform}")
print(f"Python:   {sys.version}")
print(f"Platform: {platform.system()} {platform.release()} ({platform.platform()})")
if platform.system() == "Windows":
    release, version, csd, ptype = platform.win32_ver()
    edition = platform.win32_edition()
    print(f"Windows:  {release} {edition} {csd} ({version}) {ptype}")
print()
print("For cd, please enter full (absolute) path - not relative path.")
print("Type help for help.")

cd = os.getcwd()
while True:
    cmd = input(f"{cd}> ")
    if cmd.startswith("cd"):
        cl = cmd.split(" ", 1)
        os.chdir(cl[1])
    elif cmd == "help":
        print("Type any command you would normally type in cmd or Terminal.")
        print("Type info for program info.")
    elif cmd == "show w":
        print("Refer to the GNU GPL, section 15 <https://www.gnu.org/licenses/>.")
    elif cmd == "show c":
        print("Refer to the GNU GPL, section 4-6 <https://www.gnu.org/licenses/>.")
    elif cmd == "info":
        print(f"Parashell {VERSION} ({DATE}) on {sys.platform}")
        print(f"Python:   {sys.version}")
        print(f"Platform: {platform.system()} {platform.release()} ({platform.platform()})")
    elif cmd == "exit":
        break
    else:
        exit_code = os.system(cmd)
        if exit_code != 0:
            print(f"Fail (exit code {exit_code})")
        else:
            print(f"Success (exit code {exit_code})")

print("Goodbye")
