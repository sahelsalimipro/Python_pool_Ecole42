import os
import site
import sys


def is_virtual_env() -> bool:
    """A venv is active when sys.prefix differs from sys.base_prefix."""
    return sys.prefix != sys.base_prefix


def get_site_packages() -> str:
    """Return the first folder where packages get installed."""
    paths = site.getsitepackages()
    return paths[0] if paths else "Unknown"


def show_global() -> None:
    print("MATRIX STATUS: You're still plugged in")
    print()
    print(f"Current Python: {sys.executable}")
    print("Virtual Environment: None detected")
    print()
    print("WARNING: You're in the global environment!")
    print("The machines can see everything you install.")
    print()
    print("Global package installation path:")
    print(get_site_packages())
    print()
    print("To enter the construct, run:")
    print("python -m venv matrix_env")
    print("source matrix_env/bin/activate # On Unix")
    print("matrix_env\\Scripts\\activate # On Windows")
    print()
    print("Then run this program again.")


def show_virtual() -> None:
    env_path = sys.prefix
    env_name = os.path.basename(env_path)

    print("MATRIX STATUS: Welcome to the construct")
    print()
    print(f"Current Python: {sys.executable}")
    print(f"Virtual Environment: {env_name}")
    print(f"Environment Path: {env_path}")
    print()
    print("SUCCESS: You're in an isolated environment!")
    print("Safe to install packages without affecting")
    print("the global system.")
    print()
    print("Package installation path:")
    print(get_site_packages())
    print()
    print(f"(Global Python lives in: {sys.base_prefix})")


def main() -> None:
    if is_virtual_env():
        show_virtual()
    else:
        show_global()


if __name__ == "__main__":
    main()
