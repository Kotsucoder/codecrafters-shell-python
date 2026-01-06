import sys


def main():
    # TODO: Uncomment the code below to pass the first stage
    while True:
        sys.stdout.write("$ ")
        request = input().split()
        command = request[0]
        args = request[1:]
        match command:
            case "exit":
                break
            case "echo":
                string = " ".join(args)
                sys.stdout.write(string + "\n")
            case _:
                sys.stdout.write(f"{command}: command not found\n")


if __name__ == "__main__":
    main()
