#!/usr/bin/env python3

import sys
import os

os.environ['SHELL'] = os.path.abspath(sys.argv[0])
version = "v0.9.4"

class Shell:
    def __init__(self, verbose=False):
        self.builtins = {
            "exit": self.builtin_exit,
            "echo": self.builtin_echo,
            "type": self.builtin_type,
            "pwd": self.builtin_pwd,
            "about": self.builtin_about,
            "export": self.builtin_export,
            "cd": self.builtin_cd
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
    
    def parse_input(self, usrinput:str):
        naive_split = usrinput.split(" ")
        command = naive_split[0]
        args = []
        long_arg = False
        for token in naive_split[1:]:
            try:
                if token[0] == "'" and not long_arg:
                    long_parse = token
                    long_arg = True
                    if token[-1] == "'":
                        long_arg = False
                        if len(long_parse) > 2:
                            long_parse = long_parse[1:-1]
                            semantic_object = [long_parse, True]
                            args.append(semantic_object)
                        else:
                            continue
                elif long_arg:
                    long_parse = long_parse + " " + token
                    if token[-1] == "'":
                        long_arg = False
                        if len(long_parse) > 2:
                            long_parse = long_parse[1:-1]
                            semantic_object = [long_parse, True]
                            args.append(semantic_object)
                        else:
                            continue
                else:
                    semantic_object = [token, False]
                    args.append(semantic_object)
            except IndexError:
                if long_arg:
                    long_parse = long_parse + " "
                else:
                    continue
        
        if self.verbose:
            print(f"Command is {command}")
            print(f"args is {args}")
        return command, args

    def builtin_exit(self, args):
        return False

    def builtin_echo(self, args):
        for semantic_object in args:
            if semantic_object[0][0] == "$" and not semantic_object[1]:
                string = semantic_object[0]
                try:
                    content = os.getenv(string[1:]) + " "
                    sys.stdout.write(content)
                except KeyError:
                    sys.stdout.write(string)
            else:
                string = semantic_object[0]
                sys.stdout.write(string + " ")
        print()
        return True

    def builtin_type(self, args):
        try:
            cmdtest = args[0]
            for semantic_cmdlet in args:
                cmdlet = semantic_cmdlet[0]
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
        
    def builtin_pwd(self, args):
        current_directory = os.getcwd()
        print(current_directory)
        return True
    
    def builtin_about(self, args):
        print(f"mkshell {version}")
        print("Developed by Marcus Kotsu")
        print("Based on Codecrafters")
        print("Follow on Bluesky: @kotsu.red")
        print("Follow on GitHub: @Kotsucoder")
        return True
    
    def builtin_export(self, args):
        # TODO: Add support for quotes in environment variables
        if self.verbose:
            print(args)
        for semantic_var_setter in args:
            var_setter = semantic_var_setter[0]
            if self.verbose:
                print(f"Working on {var_setter}")
            var_setter = var_setter.split("=")
            var_name = var_setter[0]
            var_content = var_setter[1]
            if self.verbose:
                print(f"Setting variable {var_name} to {var_content}")
            os.environ[var_name] = var_content
            return True
        
    def builtin_cd(self, args):
        path = args[0][0]
        if path[0] == "~":
            homedir = os.path.expanduser("~")
            path = path.replace("~", homedir)
        if os.path.isdir(path):
            if self.verbose:
                print("Success: Valid Path")
            os.chdir(path)
        else:
            if self.verbose:
                print("Failure: Invalid Path")
            print(f"cd: {path}: No such file or directory")
        return True

    def exec_program(self, command, args):
        set_args = []
        for semantics in args:
            set_args.append(semantics[0])
        if os.path.isfile(command) and os.access(command, os.X_OK):
            exec_path = command
        else:
            exec_path = self.find_exec(command)

        if exec_path:
            pid = os.fork()
            if pid == 0:
                if self.verbose:
                    print(f"Executing {exec_path} with args {full_args}")
                full_args = set_args
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
                request = input()
                command, args = self.parse_input(request)
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
    if "-v" in script_args or "--version" in script_args:
        print(f"mkshell {version}")
        sys.exit(0)
    elif "-d" in script_args:
        shell = Shell(verbose=True)
        shell.run()
    else:
        shell = Shell()
        shell.run()


if __name__ == "__main__":
    main()
