import os
from typing import List


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