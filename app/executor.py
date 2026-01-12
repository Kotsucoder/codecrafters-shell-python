import sys
import os
from typing import List

output_redirect = ""


def find_exec(command:str) -> str | None:
        path = os.getenv("PATH", "").split(":")
        for directory in path:
            try:
                contents = os.listdir(directory)
                if command in contents:
                    if os.access(f"{directory}/{command}", os.X_OK):
                        return f"{directory}/{command}"
                    else:
                        continue
                else:
                    continue
            except FileNotFoundError:
                continue
        return None

def exec_program(command:str, args:List[str]) -> bool:
    set_args = args
    if os.path.isfile(command) and os.access(command, os.X_OK):
        exec_path = command
    else:
        exec_path = find_exec(command)

    if exec_path:
        pid = os.fork()
        if pid == 0:
            full_args = set_args
            full_args.insert(0, command)
            os.execv(exec_path, full_args)
        else:
            os.waitpid(pid, 0)
            return True
    else:
        return False
    
def create_file():
    global output_redirect
    if output_redirect:
        file = open(output_redirect, 'w')
        file.close()

def write_stdout(content:str):
    global output_redirect
    if output_redirect:
        file = open(output_redirect, 'r')
        current_contents = file.read()
        file.close()
        current_contents = current_contents + content
        file = open(output_redirect, 'w')
        file.write(current_contents)
        file.close()
    else:
        sys.stdout.write(content)

def set_output(path_tokens:List[str]):
    global output_redirect
    output_redirect = " ".join(path_tokens)

def flush_output():
    global output_redirect
    output_redirect = ""