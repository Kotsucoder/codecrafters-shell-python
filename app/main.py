import sys


def main():
    # TODO: Uncomment the code below to pass the first stage
    while True:
        sys.stdout.write("$ ")
        request = input().split()
        command = request[0]
        args = request[1:]
        builtins = ["echo", "exit", "type"]
        match command:
            case "exit":
                break
            case "echo":
                string = " ".join(args)
                sys.stdout.write(string + "\n")
            case "type":
                if args[0] in builtins:
                    sys.stdout.write(f"{args[0]} is a shell builtin\n")
                else:
                    sys.stdout.write(f"{args[0]}: not found\n")
            case _:
                sys.stdout.write(f"{command}: command not found\n")


if __name__ == "__main__":
    main()
