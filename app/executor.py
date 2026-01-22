import sys
import os
import subprocess
from typing import List

output_redirect = ""
redirect_to_err = False


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
    global output_redirect
    set_args = args
    if os.path.isfile(command) and os.access(command, os.X_OK):
        exec_path = command
    else:
        exec_path = find_exec(command)

    if exec_path:
        full_args = set_args
        full_args.insert(0, command)
        if output_redirect:
            result = subprocess.run(full_args, capture_output=True, text=True, check=False)
            write_stdout(result.stdout)
            write_errout(result.stderr)
        else:
            subprocess.run(full_args, capture_output=False)
        return True
    else:
        return False
    
def create_file(overwrite:bool=True):
    global output_redirect
    if output_redirect and overwrite:
        file = open(output_redirect, 'w')
        file.close()
    elif output_redirect and not overwrite:
        if not os.path.isfile(output_redirect):
            file = open(output_redirect, 'w')

def write_stdout(content:str):
    global output_redirect
    global redirect_to_err
    if output_redirect and not redirect_to_err:
        file = open(output_redirect, 'r')
        current_contents = file.read()
        file.close()
        current_contents = current_contents + content
        file = open(output_redirect, 'w')
        file.write(current_contents)
        file.close()
    else:
        sys.stdout.write(content)

def write_errout(content:str):
    global output_redirect
    global redirect_to_err
    if output_redirect and redirect_to_err:
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

def set_err():
    global redirect_to_err
    redirect_to_err = True

def flush_output():
    global output_redirect
    global redirect_to_err
    output_redirect = ""
    redirect_to_err = False