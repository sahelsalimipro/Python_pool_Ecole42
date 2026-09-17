import sys
from typing import IO


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: ft_stream_management.py <file>")
        return

    filename: str = sys.argv[1]
    print("=== Cyber Archives Recovery & Preservation ===")
    print(f"Accessing file '{filename}'")

    try:
        file: IO[str] = open(filename)
        content: str = file.read()
    except OSError as e:
        msg = f"Error opening file '{filename}': {e}"
        print(f"[STDERR] {msg}", file=sys.stderr)
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

    # instead of : name: str = input("Enter new file name (or empty): ")

    sys.stdout.write("Enter new file name (or empty): ")
    sys.stdout.flush()
    name: str = sys.stdin.readline().rstrip("\n")

    if name == "":
        print("Data not saved.")
        return

    print(f"Saving data to '{name}'")
    try:
        out: IO[str] = open(name, "w")
        out.write(transformed)
        out.close()
    except OSError as e:
        msg = f"Error opening file '{name}': {e}"
        print(f"[STDERR] {msg}", file=sys.stderr)
        print("Data not saved.")
        return

    print(f"Data saved in file '{name}'.")


if __name__ == "__main__":
    main()
