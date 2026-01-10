#!/usr/bin/env python3

import sys
import os

class Shell:
    def __init__(self, verbose=False):
        self.builtins = {
            "exit": self.builtin_exit,
            "echo": self.builtin_echo,
            "type": self.builtin_type
        }
        self.verbose = verbose

    def find_exec(self, command):
        path = os.getenv("PATH").split(":")
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

    def builtin_exit(self, args):
        return False

    def builtin_echo(self, args):
        string = " ".join(args)
        sys.stdout.write(string + "\n")
        return True    

    def builtin_type(self, args):
        try:
            cmdtest = args[0]
            for cmdlet in args:
                if cmdlet in self.builtins:
                    sys.stdout.write(f"{cmdlet} is a shell builtin\n")
                else:
                    exec_path = self.find_exec(cmdlet)
                    if exec_path:
                        sys.stdout.write(f"{cmdlet} is {exec_path}\n")
                    else:
                        sys.stdout.write(f"{cmdlet}: not found\n")
            return True
        except:
            sys.stdout.write(f"Empty argument\n")
            return True

    def exec_program(self, command, args):
        exec_path = self.find_exec(command)
        if exec_path:
            pid = os.fork()
            if pid == 0:
                if self.verbose:
                    print(f"Executing {exec_path} with args {args}")
                full_args = args
                full_args.insert(0, command)
                os.execv(exec_path, full_args)
            else:
                os.waitpid(pid, 0)
                return True
        else:
            return False

    def run(self):
        keep_running = True
        while keep_running:
            try:
                sys.stdout.write("$ ")
                request = input().split()
                command = request[0]
                args = request[1:]
                if command in self.builtins:
                    keep_running = self.builtins[command](args)
                else:
                    exec_success = self.exec_program(command, args)
                    if not exec_success:
                        sys.stdout.write(f"{command}: command not found\n")
            except KeyboardInterrupt:
                print()
                continue


def main():
    script_args = sys.argv
    if "-v" in script_args:
        shell = Shell(verbose=True)
    else:
        shell = Shell()
    shell.run()


if __name__ == "__main__":
    main()
