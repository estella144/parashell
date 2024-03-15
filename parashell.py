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
import shutil
import subprocess
import sys

VERSION = "0.2.0"
DATE = "15 Mar 2024"

NOTICE = """Parashell Copyright (C) 2024 Oliver Nguyen
This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
This is free software, and you are welcome to redistribute it
under certain conditions; type `show c' for details."""

page_idx = 0

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
input("[Enter] - Continue")

def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        # macOS or Linux
        os.system("clear")

def get_dir_output():
    if platform.system() == "Windows":
        out = subprocess.check_output("dir", shell=True)
    else:
        # macOS or Linux
        out = subprocess.check_output("ls -l", shell=True)
    return out.decode("utf-8")

def paginate_output(out):
    lines = out.split("\n")
    if platform.system() == "Windows":
        header_lines = 5
        footer_lines = 2
        footer = lines[-footer_lines:]
        content = lines[header_lines:-footer_lines]
    else:
        # macOS or Linux
        header_lines = 1
        footer_lines = 0
        footer = []
        content = lines[header_lines:]
    header = lines[0:header_lines]
    pages = [content[i:i+12] for i in range(0, len(content), 12)]
    if len(content) % 12 != 0:
        remaining_lines = content[len(content)//12*12:]
        pages.append(remaining_lines)
    return [header, footer, pages]

def print_page(header, footer, pages, page_idx, cd):
    global VERSION
    columns, lines = shutil.get_terminal_size()

    if page_idx != 0:
        left_arrow = "< "
    else:
        left_arrow = ""

    if page_idx != len(pages)-1:
        right_arrow = " >"
    else:
        right_arrow = ""

    current_page = pages[page_idx]
    top_divider_msg = f"[Parashell {VERSION} - {cd}]"
    bottom_divider_msg = f"[{left_arrow}Page {page_idx+1} of {len(pages)-1}{right_arrow}]"

    print(f"{top_divider_msg:=^{columns}}")
    print('\n'.join(header))
    print('\n'.join(current_page))
    print('\n'.join(footer))
    print(f"{bottom_divider_msg:=^{columns}}")

while True:
    clear_screen()
    cd = os.getcwd()
    output = get_dir_output()
    header, footer, pages = paginate_output(output)
    print_page(header, footer, pages, page_idx, cd)

    cmd = input(f"{cd}> ")
    if cmd.startswith("cd"):
        try:
            cl = cmd.split(" ", 1)
            os.chdir(cl[1])
            print(f"Success: changed directory to {cl[1]}")
        except IndexError:
            print("Error: 1 argument required for cd.")
            input("[Enter] - Continue")
        except FileNotFoundError:
            print("Error: Directory not found.")
            input("[Enter] - Continue")
        except NotADirectoryError:
            print("Error: Not a directory.")
            input("[Enter] - Continue")
    elif cmd == "help":
        print("Type any command you would normally type in your console/shell.")
        print("exit - exit Parashell")
        print("info - show Parashell info")
        print("help - show this help")
        print("next - next page of dir listing")
        print("prev - previous page of dir listing")
        input("[Enter] - Continue")
    elif cmd == "show w":
        print("Refer to the GNU GPL, section 15 <https://www.gnu.org/licenses/>.")
    elif cmd == "show c":
        print("Refer to the GNU GPL, section 4-6 <https://www.gnu.org/licenses/>.")
    elif cmd == "info":
        info()
    elif cmd == "exit":
        break
    elif cmd == "next":
        if page_idx == len(pages)-2:
            print("No more pages to display")
            input("[Enter] - Continue")
        else:
            page_idx += 1
    elif cmd == "prev":
        if page_idx == 0:
            print("No more pages to display")
            input("[Enter] - Continue")
        else:
            page_idx -= 1
    else:
        exit_code = os.system(cmd)
        if exit_code != 0:
            print(f"Fail (exit code {exit_code})")
        else:
            print(f"Success (exit code {exit_code})")
        input("[Enter] - Continue")

print("Goodbye")
