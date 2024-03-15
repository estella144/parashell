#    parashell - a shell
#    Copyright (C) 2024 Oliver Nguyen
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import platform
import sys

SCRIPT_VERSION = "0.1.0"
SCRIPT_DATE = "12 Mar 2024"
NOTICE = """Parashell Copyright (C) 2024 Oliver Nguyen
This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
This is free software, and you are welcome to redistribute it
under certain conditions; type `show c' for details."""


def info():
    print(f"Parashell v{SCRIPT_VERSION} ({SCRIPT_DATE}) on {sys.platform}")
    print(f"Python:   {sys.version}")
    print(f"Platform: {platform.system()} {platform.release()} ({platform.platform()})")
    if platform.system() == "Windows":
        release, version, csd, ptype = platform.win32_ver()
        print(f"Windows:  {release} {platform.win32_edition()} ({version}) {csd} {ptype}")
    elif platform.system() == "Darwin":
        # macOS
        release, versioninfo, machine = platform.mac_ver()
        print(f"macOS:    {release} on {machine}")

print("Starting Parashell...")
print()
print(NOTICE)
print()
info()
print()
print("Please ensure full paths (not relative) are used with cd.")
print("Type 'help' for help.")

while True:
    cwd = os.getcwd()
    cmd = input(f"{cwd}> ")
    if cmd.startswith("cd"):
        cl = cmd.split(" ", 1)
        os.chdir(cl[1])
        print(f"Directory successfully changed to {cl[1]}")
    elif cmd == "help":
        if platform.system() == "Windows":
            print("Enter any command you would normally enter into cmd.")
            print("Type 'exit' to exit.")
            print("'cd' only accepts full paths.")
        else:
            print("Enter any command you would normally enter into Terminal.")
            print("'cd' only accepts full paths.")
    elif cmd == "show w":
        print("See section 15 of the GNU GPL on <https://www.gnu.org/licenses/>.")
    elif cmd == "show c":
        print("See sections 4-6 of the GNU GPL on <https://www.gnu.org/licenses/>.")
    elif cmd == "exit":
        print("Goodbye")
        break
    else:
        exit_code = os.system(cmd)
        if exit_code != 0:
            print(f"{cmd}: Failure (exit code {exit_code})")
        else:
            print(f"{cmd}: Success (exit code {exit_code})")
