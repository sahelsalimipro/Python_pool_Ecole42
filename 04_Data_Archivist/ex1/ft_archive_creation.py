import sys
from typing import IO


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: ft_archive_creation.py <file>")
        return

    filename: str = sys.argv[1]
    print("=== Cyber Archives Recovery & Preservation ===")
    print(f"Accessing file '{filename}'")

    try:
        file: IO[str] = open(filename)
        content: str = file.read()
    except OSError as e:
        print(f"Error opening file '{filename}': {e}")
        return

    print("---\n")
    print(content, end="")
    print("\n---")
    file.close()
    print(f"File '{filename}' closed.")

    body: str = content[:-1] if content.endswith("\n") else content
    lines = body.split("\n")
    transformed: str = "\n".join(line + "#" for line in lines)

    print("\nTransform data:")
    print("---\n")
    print(transformed)
    print("\n---")
    name: str = input("Enter new file name (or empty): ")
    if name == "":
        print("Not saving data.")
        return

    print(f"Saving data to '{name}'")
    try:
        out: IO[str] = open(name, "w")
        out.write(transformed)
        out.close()
    except OSError as e:
        print(f"Error opening file '{name}': {e}")
        return

    print(f"Data saved in file '{name}'.")


if __name__ == "__main__":
    main()
