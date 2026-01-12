#!/usr/bin/env python3.10

import sys
import os
from app import lexer
from app import shell_builtins
from app import executor

os.environ['SHELL'] = os.path.abspath(sys.argv[0])
version = "v0.12"

class Shell:
    def __init__(self, verbose=False):
        self.verbose = verbose

    def run(self):
        builtins = shell_builtins.Builtins()
        keep_running = True
        while keep_running:
            try:
                executor.write_stdout("$ ")
                request = input()
                tokens = lexer.command_lexer(request)
                command_tokens, redirect_tokens = lexer.redirect_output_tokens(tokens)
                expanded_commands = lexer.expander(command_tokens)
                expanded_redirects = lexer.expander(redirect_tokens)
                executor.set_output(expanded_redirects)
                executor.create_file()
                command = expanded_commands[0]
                args = expanded_commands[1:]
                if command in builtins.get_builtins():
                    keep_running = builtins.run_builtin(command, args)
                else:
                    exec_success = executor.exec_program(command, args)
                    if not exec_success:
                        executor.write_errout(f"{command}: command not found\n")
                executor.flush_output()
            except KeyboardInterrupt:
                print()
                executor.flush_output()
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
