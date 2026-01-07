import sys

class Shell:
    def __init__(self):
        self.builtins = {
            "exit": self.builtin_exit,
            "echo": self.builtin_echo,
            "type": self.builtin_type,
        }

    def builtin_exit(self, args):
        return False

    def builtin_echo(self, args):
        string = " ".join(args)
        sys.stdout.write(string + "\n")
        return True

    def builtin_type(self, args):
        try:
            cmdlet = args[0]
            if cmdlet in self.builtins:
                sys.stdout.write(f"{cmdlet} is a shell builtin\n")
                return True
            else:
                sys.stdout.write(f"{cmdlet}: not found\n")
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
