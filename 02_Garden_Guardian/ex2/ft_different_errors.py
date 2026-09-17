#!/usr/bin/env python3

def garden_operations(operation_number: int):
    if operation_number == 0:
        int("abc")
    elif operation_number == 1:
        return 5 / 0
    elif operation_number == 2:
        open("/non/existent/file")
    elif operation_number == 3:
        return "abc" + 2
    # type: ignore
    else:
        return "Operation completed successfully"


def test_error_types() -> None:

    for value in range(5):
        print(f"Testing operation {value}...")
        try:
            res = garden_operations(value)
            print(res)
        except ValueError as error:
            print(f"Caught {type(error).__name__}: {error}")
        except ZeroDivisionError as error:
            print(f"Caught {type(error).__name__}: {error}")
        except FileNotFoundError as error:
            print(f"Caught {type(error).__name__}: {error}")
        except TypeError as error:
            print(f"Caught {type(error).__name__}: {error}")


if __name__ == "__main__":
    print("=== Garden Error Types Demo ===")
    test_error_types()
    print("\nAll error types tested successfully!")
