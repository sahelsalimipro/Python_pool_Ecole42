import sys


def ft_command_quest() -> None:

    name: str = sys.argv[0]
    args = sys.argv[1:]
    print(f"program name = {name}")
    nb_len = len(args)
    if nb_len == 0:
        print("No arguments provided!")
    else:
        i: int = 0
        print(f"Arguments received: {len(args)}")
        while (i != len(args)):
            print(f"Argument {i + 1}: {args[i]}")
            i += 1
    print(f"Total arguments: {len(sys.argv)}")


if __name__ == "__main__":
    print("=== Command Quest ===")
    ft_command_quest()


# def main() -> None:
#     print("=== Command Quest ===\n")

#     program_name: str = sys.argv[0]
#     args = sys.argv[1:]
#     print(f"Program name: {program_name}")
#     if len(args) == 0:
#         print("No arguments provided!")
#         print("Total arguments: 1")
#         return
#     print(f"Arguments received: {len(args)}")
#     i: int = 1
#     for arg in args:
#         print(f"Argument {i}: {arg}")
#         i += 1
#     print(f"Total arguments: {len(sys.argv)}")


# if __name__ == "__main__":
#     main()
