
def secure_archive(filename: str,
                   action: str = "read",
                   content: str | None = None) -> tuple[bool, str]:
    try:
        if action == "read":
            with open(filename, "r") as f:
                data: str = f.read()
            return (True, data)
        elif action == "write":
            with open(filename, "w") as f:
                f.write(content if content is not None else "")
            return (True, "Content successfully written to file")
        else:
            return (False, f"Unknown action '{action}'")
    except OSError as e:
        return (False, str(e))


def main() -> None:
    print("=== Cyber Archives Security ===\n")

    print("Using 'secure_archive' to read from a nonexistent file:")
    print(secure_archive("/not/existing/file"))
    print()

    print("Using 'secure_archive' to read from an inaccessible file:")
    print(secure_archive("/etc/master.passwd"))
    print()

    print("Using 'secure_archive' to read from a regular file:")
    result = secure_archive("ancient_fragment.txt")
    print(result)
    print()

    print("Using 'secure_archive' to write previous content to a new file:")
    if result[0]:
        print(secure_archive("new_vault.txt", "write", result[1]))


if __name__ == "__main__":
    main()
