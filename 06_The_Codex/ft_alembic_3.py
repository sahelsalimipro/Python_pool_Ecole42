from alchemy import elements


def main() -> None:
    print("=== Alembic 3 ===")
    print("Accessing alchemy/elements.py using: 'from ... import ...'")
    print(f"Testing create_air: {elements.create_air()}")


if __name__ == "__main__":
    main()
