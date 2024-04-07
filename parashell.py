"""ParaShell - a shell"""

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

import configparser
import getpass
import os
import platform
import shutil
import subprocess
import sys

VERSION = "0.3.0"
COMMIT = "acd0b67"
DATE = "05 Apr 2024"
DEV_STATE_SHORT = ""
DEV_STATE = "development"

def get_username() -> str:
    '''Get the current user's username.'''
    return getpass.getuser()

def get_hostname() -> str:
    '''Get the current computer's name.'''
    return os.uname().nodename

def shell_exists(shell_name) -> bool:
    try:
        subprocess.run(["which", shell_name], check=True, stdout=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

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

def get_custom_prompt() -> str:
    '''Reads custom prompt from config file and returns it as a string'''
    config = configparser.ConfigParser()
    config.read("config.ini")
    try:
        return config["Prompt"]["PromptFormat"]
    except KeyError:
        print("Error: Prompt key not found. Your config.ini may be out of date.")
        print("       Delete your config.ini file and restart ParaShell.")
        return get_best_shell()

def get_custom_shell() -> str:
    '''Reads custom shell from config file and returns it as a string'''
    config = configparser.ConfigParser()
    config.read("config.ini")
    try:
        return config["Shell"]["Shell"]
    except KeyError:
        print("Error: Shell key not found. Your config.ini may be out of date.")
        print("       Delete your config.ini file and restart ParaShell.")
        return get_best_shell()

def execute_command(cmd, echo_result=True, shell=get_custom_shell()) -> int:
    '''Executes a command in the computer's shell.
    cmd: str - command to run'''
    try:
        subprocess.run(cmd, shell=True, check=True, executable=shell)
        if echo_result:
            print(f"Success: {cmd}")
            return 0
    except subprocess.CalledProcessError as e:
        print(f"Failed executing command: {cmd} (return code {e.returncode})")
        return e.returncode
    finally:
        echo_result = True

def check_for_config() -> bool:
    '''Checks if config.ini is present.
    Returns True if config.ini is present, and False if not.'''
    try:
        f = open('config.ini', mode='r', encoding="utf-8")
        f.close()
        return True
    except FileNotFoundError:
        print("Config file not found")
        return False

def setup_config() -> None:
    '''Writes default values to config.ini, if it does not exist.'''
    global VERSION
    config_file_exists = check_for_config()
    if not config_file_exists:
        print("Setting up...")
        f = open('config.ini', mode='w', encoding="utf-8")
        f.close()
        config = configparser.ConfigParser()
        config.read('config.ini')
        config["Version"] = {"ParashellVersion": VERSION}
        config["CmdAliases"] = {}
        config["Prompt"] = {"PromptFormat": "{username}@{hostname}:{cwd}"}
        if platform.system() != "Windows":
            config["Shell"] = {"Shell": get_best_shell()}
        with open('config.ini', mode='w', encoding="utf-8") as f:
            config.write(f)
    else:
        print("Config file found")

def info(continue_prompt=True) -> None:
    '''Prints Parashell and system info.
    continue_prompt: bool (kwarg) - if True, displays continue prompt.'''
    global VERSION
    global COMMIT
    global DATE

    print(f"Parashell {VERSION} ({COMMIT}, {DATE}) on {sys.platform}")
    print(f"Python:   {sys.version}")
    print(f"Platform: {platform.system()} {platform.release()} ({platform.platform()})")
    if platform.system() == "Windows":
        release, version, csd, ptype = platform.win32_ver()
        edition = platform.win32_edition()
        print(f"Windows:  {release} {edition} {csd} ({version}) {ptype}")
    elif platform.system() == "Darwin":
        release, versioninfo, machine = platform.mac_ver()
        print(f"macOS:    {release} on {machine}")
    if continue_prompt:
        input("[Enter] - Continue")
    continue_prompt = True

def clear_screen() -> None:
    '''Clears the screen.'''
    if platform.system() == "Windows":
        execute_command("cls", echo_result=False)
    else:
        # macOS or Linux
        execute_command("clear", echo_result=False)

def get_dir_output() -> str:
    '''Get directory output.'''
    if platform.system() == "Windows":
        out = subprocess.check_output("dir", shell=True)
    else:
        # macOS or Linux
        out = subprocess.check_output("ls -l", shell=True)
    try:
        return out.decode("utf-8")
    except UnicodeDecodeError as ue:
        return f"Error: Cannot get directory listing\n{ue}"

def paginate_output(out: str) -> list:
    '''Paginates a directory listing into 12 line pages.
    out: str - directory listing to paginate.'''
    if not out.startswith("Error"):
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
    else:
        return ["", "", out]

def print_page(header: str, footer: str, pages: list[str], page_idx: int, cd: str) -> None:
    '''Prints a directory listing page with header, footer and dividers.
    header: str - page header
    footer: str - page footer
    pages: list[str] - pages of directory listing
    page_idx: int - index of page to print
    cd: str - current directory'''

    global VERSION
    global DEV_STATE

    WARNING_SHORT = f"[Warning: {DEV_STATE} release. Bugs may be present.]"
    columns, lines = shutil.get_terminal_size()

    if page_idx != 0:
        left_arrow = "< "
    else:
        left_arrow = ""

    if page_idx != len(pages)-2:
        right_arrow = " >"
    else:
        right_arrow = ""

    if not type(pages) == str:
        current_page = pages[page_idx]
    else:
        current_page = pages
    top_divider_msg = f"[Parashell {VERSION} - {cd}]"
    bottom_divider_msg = f"[{left_arrow}Page {page_idx+1} of {len(pages)-1}{right_arrow}]"

    print(f"{top_divider_msg:=^{columns}}")
    print(f"{WARNING_SHORT:-^{columns}}")
    print('\n'.join(header))
    if not type(pages) == str:
        print('\n'.join(current_page))
    else:
        print(current_page)
    print('\n'.join(footer))
    print(f"{bottom_divider_msg:=^{columns}}")

def process_cd(cmd) -> int:
    '''Processes a 'cd' command.
    cmd: str - full command, including `cd`'''
    try:
        cl = cmd.split(" ", 1)
        os.chdir(cl[1])
        page_idx = 0
        print(f"Success: changed directory to {cl[1]}")
        return 0
    except IndexError:
        print("Error: 1 argument required for cd.")
        input("[Enter] - Continue")
        return 1
    except FileNotFoundError:
        print("Error: Directory not found.")
        input("[Enter] - Continue")
        return 1
    except NotADirectoryError:
        print("Error: Not a directory.")
        input("[Enter] - Continue")
        return 1

def process_goto(cmd, pages) -> None:
    '''Processes a `goto` command.
    cmd: str - full command including `goto`'''
    try:
        if len(cmd.split(' ')) == 1:
            p = int(input(f"Which page to display? [1-{len(pages)-1}] "))
            p -= 1
            if (p < 0) or (p >= len(pages)):
                print(f"Error: Page index {p} out of range")
                input("[Enter] - Continue")
            else:
                page_idx = p
        else:
            cl = cmd.split(' ', 1)
            cp = int(cl[1])-1
            if (cp < 0) or (cp >= len(pages)):
                print(f"Error: Page index {cp} out of range")
                input("[Enter] - Continue")
            else:
                page_idx = cp
    except ValueError:
        print(f"Error: Invalid page index")
        input("[Enter] - Continue")

def refresh_page(page_idx) -> list:
    '''Refreshes the directory listing.
    page_idx: int - current page index'''
    clear_screen()
    cd = os.getcwd()
    output = get_dir_output()
    header, footer, pages = paginate_output(output)
    print_page(header, footer, pages, page_idx, cd)
    return [header, footer, pages, page_idx, cd]

def main_loop() -> None:
    '''Main loop of Parashell.'''
    page_idx = 0
    dir_data = refresh_page(page_idx)
    pages = dir_data[2]
    prompt_format = get_custom_prompt()
    shell = get_custom_shell()
    username = get_username()
    hostname = get_hostname()
    cwd = os.getcwd()

    while True:
        username = get_username()
        hostname = get_hostname()
        cwd = os.getcwd()
        prompt = prompt_format.format(username=username, hostname=hostname, cwd=cwd)
        cmd = input(f"{prompt} ")
        if cmd.startswith("cd"):
            process_cd(cmd)
            refresh_page(page_idx)
        elif cmd == "help":
            print("Type any command you would normally type in your console/shell.")
            print("exit - exit Parashell")
            print("goto - go to specific page of dir listing")
            print("info - show Parashell info")
            print("help - show this help")
            print("next - next page of dir listing")
            print("prev - previous  page of dir listing")
            print("refr - refresh dir listing")
            print("shll - show current shell path")
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
                print("Error: No more pages to display")
            else:
                page_idx += 1
                refresh_page(page_idx)
        elif cmd == "prev":
            if page_idx == 0:
                print("Error: No more pages to display")
            else:
                page_idx -= 1
                refresh_page(page_idx)
        elif cmd.startswith("goto"):
            process_goto(cmd, len(pages))
        elif cmd == "refr":
            refresh_page(page_idx)
        elif cmd == "shll":
            print(get_custom_shell())
        else:
            execute_command(cmd, shell=shell)

def main() -> None:
    '''Starts Parashell.'''

    global DEV_STATE

    NOTICE = """Parashell Copyright (C) 2024 Oliver Nguyen
This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
This is free software, and you are welcome to redistribute it
under certain conditions; type `show c' for details."""

    WARNING = f"""Warning! This is a {DEV_STATE} release. Bugs may be present.
Please report bugs to the GitHub repository:
<github.com/estella144/parashell/issues>"""

    clear_screen()

    print(NOTICE)
    print()
    print(WARNING)
    print()
    info(continue_prompt=False)
    print()
    print("Type 'help' for help.")
    print()
    input("[Enter] - Continue")

    main_loop()

if __name__ == "__main__":
    print("Starting Parashell...")
    setup_config()
    main()
    print("Goodbye")
