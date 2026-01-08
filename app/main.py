import sys
import os

class Shell:
    def __init__(self):
        self.builtins = {
            "exit": self.builtin_exit,
            "echo": self.builtin_echo,
            "type": self.builtin_type
        }

    def builtin_exit(self, args):
        return False

    def builtin_echo(self, args):
        string = " ".join(args)
        sys.stdout.write(string + "\n")
        return True    

    def builtin_type(self, args):
        path = os.getenv("PATH").split(":")
        try:
            cmdtest = args[0]
            for cmdlet in args:
                if cmdlet in self.builtins:
                    sys.stdout.write(f"{cmdlet} is a shell builtin\n")
                else:
                    keep_checking = True
                    while keep_checking:
                        for directory in path:
                            try:
                                contents = os.listdir(directory)
                                if cmdlet in contents:
                                    file_path = f"{directory}/{cmdlet}"
                                    if os.access(file_path, os.X_OK):
                                        print(f"{cmdlet} is {file_path}")
                                        keep_checking = False
                            except FileNotFoundError:
                                continue
                        if keep_checking:
                            sys.stdout.write(f"{cmdlet}: not found\n")
                            keep_checking = False
            return True
        except:
            sys.stdout.write(f"Empty argument\n")
            return True

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
                    sys.stdout.write(f"{command}: command not found\n")
            except KeyboardInterrupt:
                print()
                continue


def main():
    shell = Shell()
    shell.run()


if __name__ == "__main__":
    main()
