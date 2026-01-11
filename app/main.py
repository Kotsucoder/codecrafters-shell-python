#!/usr/bin/env python3.10

import sys
import os
from app import lexer
from app import shell_builtins
from app import executor

os.environ['SHELL'] = os.path.abspath(sys.argv[0])
version = "v0.11"

class Shell:
    def __init__(self, verbose=False):
        self.verbose = verbose

    def run(self):
        builtins = shell_builtins.Builtins()
        keep_running = True
        while keep_running:
            try:
                sys.stdout.write("$ ")
                request = input()
                tokens = lexer.command_lexer(request)
                expanded_commands = lexer.expander(tokens)
                command = expanded_commands[0]
                args = expanded_commands[1:]
                if command in builtins.get_builtins():
                    keep_running = builtins.run_builtin(command, args)
                else:
                    exec_success = executor.exec_program(command, args)
                    if not exec_success:
                        sys.stdout.write(f"{command}: command not found\n")
            except KeyboardInterrupt:
                print()
                continue


def main():
    script_args = sys.argv
    if "-v" in script_args or "--version" in script_args:
        print(f"mkshell {version}")
        sys.exit(0)
    else:
        shell = Shell()
        shell.run()


if __name__ == "__main__":
    main()
