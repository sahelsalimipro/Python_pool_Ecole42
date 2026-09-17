import sys
from typing import IO


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: ft_ancient_text.py <file>")
        return

    filename: str = sys.argv[1]
    print("=== Cyber Archives Recovery ===")
    print(f"Accessing file '{filename}'")

    try:
        file: IO[str] = open(filename)
        content: str = file.read()
    except OSError as e:
        print(f"Error opening file '{filename}': {e}")
        return

    print("---\n")
    print(content)
    print("---")
    file.close()
    print(f"File '{filename}' closed.")


if __name__ == "__main__":
    main()
